import json
import os

from flask import Flask, jsonify, request, send_from_directory, render_template, Response
from Flask_App.Classes.File_Handler import File_Content_Streamer_Thread
from Flask_App.Classes.Task_Handler import Task_Handler_Class
from Flask_App.Libraries.network_tools import ssh_execute_command

from Flask_App.Libraries.tools import delete_folder, archive_files, archive_directory, get_directory_info, list_dir
from Flask_App.paths import app_path, root_path_archives, root_upload_path, root_log_collection_folder, root_fqdn_folder
from Flask_App.Threads.configurations import cleanup_thread, cleanup_logger_streamer, log_collection_logger_streamer, log_collection_thread, fqdn_thread, fqdn_logger_streamer, backup_thread, backup_logger_streamer
from Flask_App.Libraries.logger_module import global_logger



app = Flask(__name__, template_folder=f'{app_path}frontend/pages', static_folder=f'{app_path}frontend/static')

endpoint_thread_mapping: dict[str, Task_Handler_Class] = {
    "cleanup": cleanup_thread,
    "log_collection": log_collection_thread,
    "fqdn": fqdn_thread,
    "backup": backup_thread,
}

endpoint_streamer_mapping: dict[str, File_Content_Streamer_Thread] = {
    "cleanup": cleanup_logger_streamer,
    "log_collection": log_collection_logger_streamer,
    "fqdn": fqdn_logger_streamer,
    "backup": backup_logger_streamer,
}



##################
### BACKUP API ###
##################


@app.route('/backup',methods = ['POST', 'GET'])
def backup_page():
    global_logger.info(f'REQUEST INFORMATION > IP: {request.remote_addr}, Route: {request.path}, Params: {request.args.to_dict()}')
    return render_template(
        'backup.html',
        page_id="backup"
    )
    
@app.route('/backup_endpoint',methods = ['POST', 'GET'])
def backup_endpoint():
    global_logger.info(f'REQUEST INFORMATION > IP: {request.remote_addr}, Route: {request.path}, Params: {request.args.to_dict()}')
    
    if not backup_thread.safe_task_lock.locked():
        with backup_thread.safe_task_lock:
            ssh_username_json = request.args.get('ssh_username')
            ssh_password_json = request.args.get('ssh_password')
            ip_addresses_json = request.args.get('ip_addresses_hostnames')
            backup_type_json = request.args.get('backup_type', "differential")
            
            if ssh_username_json is not None:
                ssh_username = json.loads(ssh_username_json)
            else:
                ssh_username = ""
                
            if ssh_password_json is not None:
                ssh_password = json.loads(ssh_password_json)
            else:
                ssh_password = ""
            
            if ip_addresses_json is not None:
                ip_addresses = json.loads(ip_addresses_json)
            else:
                ip_addresses = []
            
            if backup_type_json == "differential":
                backup_script = "daily_backup_mapr_differential.sh"
            elif backup_type_json == "partition":
                backup_script = "daily_backup_mapr_partition.sh"
            elif backup_type_json == "incremental":
                backup_script = "daily_backup_mapr_incremental.sh"
            else:
                # Default Differential
                backup_script = "daily_backup_mapr_differential.sh"
            
            backup_thread.set_Parameters(
                ssh_username=ssh_username,
                ssh_password=ssh_password,
                ip_addresses=ip_addresses,
                script_path=root_upload_path + backup_script,
                script_upload_path="/home/mapr",
                script_run_command="sudo chmod +x /home/mapr/daily_backup_mapr_differential.sh &&", # One-Shot Run Command
                add_to_cron=True, # Cron Parameters
                cron_parameters="", # Cron Parameters
                script_parameters="",
            )
            
            if not backup_thread.is_Running():
                backup_thread.start_Task()
            else:
                backup_thread.stop_Task()
                backup_thread.wait_To_Stop_Once_Task()
                backup_thread.start_Task()
    else:
        return jsonify(
            message="Backup task already running"
        )
    
    return jsonify(
        message="Backup task queued"
    )
    
@app.route('/backup_control_endpoint',methods = ['POST', 'GET'])
def backup_control_endpoint():
    global_logger.info(f'REQUEST INFORMATION > IP: {request.remote_addr}, Route: {request.path}, Params: {request.args.to_dict()}')
    
    if not backup_thread.safe_task_lock.locked():
        with backup_thread.safe_task_lock:
            ssh_username_json = request.args.get('ssh_username')
            ssh_password_json = request.args.get('ssh_password')
            ip_addresses_json = request.args.get('ip_addresses_hostnames')
            
            if ssh_username_json is not None:
                ssh_username = json.loads(ssh_username_json)
            else:
                ssh_username = ""
                
            if ssh_password_json is not None:
                ssh_password = json.loads(ssh_password_json)
            else:
                ssh_password = ""
            
            if ip_addresses_json is not None:
                ip_addresses = json.loads(ip_addresses_json)
            else:
                ip_addresses = []
            print("ip_addresses", ip_addresses)
            
            ip_response_list: list[dict[str, str]] = list()
            response_structure: dict[str, str] = {
                "ip_address": "",
                "message": "",
            }
            for ip_address in ip_addresses:
                
                response, output = ssh_execute_command(
                    ssh_client=ip_address, 
                    username=ssh_username, 
                    password=ssh_password, 
                    command="crontab -l | awk '/daily_backup_mapr.*\\.sh/ {print $1, $2, $3, $4, $5}'",
                    reboot=False,
                    logger_hook=backup_thread.logger
                )
                if response:
                    print(f"{ip_address} -> {output}")
                    
                    temp_response = response_structure.copy()
                    temp_response["ip_address"] = ip_address
                    temp_response["message"] = output
                    
                    ip_response_list.append(
                        temp_response
                    )
            return jsonify(
                message=ip_response_list,
            )
    else:
        return jsonify(
            message="Backup Control task already running"
        )
    
    return jsonify(
        message="Backup Control task queued"
    )


###################
###################
###################



######################
### FQDN SETUP API ###
######################


@app.route('/fqdn',methods = ['POST', 'GET'])
def fqdn_page():
    return render_template(
        'fqdn.html',
        page_id="fqdn"
    )


@app.route('/fqdn_endpoint',methods = ['POST', 'GET'])
def fqdn_endpoint():
    global_logger.info(f'REQUEST INFORMATION > IP: {request.remote_addr}, Route: {request.path}, Params: {request.args.to_dict()}')
    
    if not fqdn_thread.safe_task_lock.locked():
        with fqdn_thread.safe_task_lock:
            ssh_username_json = request.args.get('ssh_username')
            ssh_password_json = request.args.get('ssh_password')
            ip_address_hostnames_list_json = request.args.get('ip_addresses_hostnames')
            
            if ssh_username_json is not None:
                ssh_username = json.loads(ssh_username_json)
            else:
                ssh_username = ""
                
            if ssh_password_json is not None:
                ssh_password = json.loads(ssh_password_json)
            else:
                ssh_password = ""
            
            if ip_address_hostnames_list_json is not None:
                ip_address_hostnames_list = json.loads(ip_address_hostnames_list_json)
            else:
                ip_address_hostnames_list = []
            
            fqdn_thread.set_Parameters(
                ssh_username=ssh_username,
                ssh_password=ssh_password,
                ip_address_hostnames_list=ip_address_hostnames_list
            )
            
            if not fqdn_thread.is_Running():
                fqdn_thread.start_Task()
            else:
                fqdn_thread.stop_Task()
                fqdn_thread.wait_To_Stop_Once_Task()
                fqdn_thread.start_Task()
    else:
        return jsonify(
            message="FQDN task already running"
        )
    
    return jsonify(
        message="FQDN task queued"
    )
    

######################
######################
######################


###################
### CLEANUP API ###
###################


@app.route('/cleanup',methods = ['POST', 'GET'])
def cleanup_page():
    global_logger.info(f'REQUEST INFORMATION > IP: {request.remote_addr}, Route: {request.path}, Params: {request.args.to_dict()}')
    return render_template(
        'cleanup.html',
        page_id="cleanup"
    )
    
@app.route('/cleanup_endpoint',methods = ['POST', 'GET'])
def cleanup_endpoint():
    global_logger.info(f'REQUEST INFORMATION > IP: {request.remote_addr}, Route: {request.path}, Params: {request.args.to_dict()}')
    
    if not cleanup_thread.safe_task_lock.locked():
        with cleanup_thread.safe_task_lock:
            ssh_username_json = request.args.get('ssh_username')
            ssh_password_json = request.args.get('ssh_password')
            ip_addresses_json = request.args.get('ip_addresses_hostnames')
            
            
            if ssh_username_json is not None:
                ssh_username = json.loads(ssh_username_json)
            else:
                ssh_username = ""
                
            if ssh_password_json is not None:
                ssh_password = json.loads(ssh_password_json)
            else:
                ssh_password = ""
            
            if ip_addresses_json is not None:
                ip_addresses = json.loads(ip_addresses_json)
            else:
                ip_addresses = []
            
            
            cleanup_thread.set_Parameters(
                ssh_username=ssh_username,
                ssh_password=ssh_password,
                ip_addresses=ip_addresses,
                script_path=root_upload_path + "cleanup.py"
            )
            
            if not cleanup_thread.is_Running():
                cleanup_thread.start_Task()
            else:
                cleanup_thread.stop_Task()
                cleanup_thread.wait_To_Stop_Once_Task()
                cleanup_thread.start_Task()
    else:
        return jsonify(
            message="Cleanup task already running"
        )
    
    return jsonify(
        message="Cleanup task queued"
    )


###################
###################
###################


##########################
### LOG COLLECTION API ###
##########################


@app.route('/log_collection',methods = ['POST', 'GET'])
def log_collection_page():
    global_logger.info(f'REQUEST INFORMATION > IP: {request.remote_addr}, Route: {request.path}, Params: {request.args.to_dict()}')
    return render_template(
        'log_collection.html',
        page_id="log_collection"
    )
    

@app.route('/log_collection_endpoint',methods = ['POST', 'GET'])
def log_collection_endpoint():
    global_logger.info(f'REQUEST INFORMATION > IP: {request.remote_addr}, Route: {request.path}, Params: {request.args.to_dict()}')
    
    if not log_collection_thread.safe_task_lock.locked():
        with log_collection_thread.safe_task_lock:
            ssh_username_json = request.args.get('ssh_username')
            ssh_password_json = request.args.get('ssh_password')
            ip_addresses_json = request.args.get('ip_addresses_hostnames')
            
            
            if ssh_username_json is not None:
                ssh_username = json.loads(ssh_username_json)
            else:
                ssh_username = ""
                
            if ssh_password_json is not None:
                ssh_password = json.loads(ssh_password_json)
            else:
                ssh_password = ""
            
            if ip_addresses_json is not None:
                ip_addresses = json.loads(ip_addresses_json)
            else:
                ip_addresses = []
            
            
            log_collection_thread.set_Parameters(
                ssh_username=ssh_username,
                ssh_password=ssh_password,
                ip_addresses=ip_addresses
            )
            
            if not log_collection_thread.is_Running():
                log_collection_thread.start_Task()
            else:
                log_collection_thread.stop_Task()
                log_collection_thread.wait_To_Stop_Once_Task()
                log_collection_thread.start_Task()
    else:
        return jsonify(
            message="Log collection task already running"
        )
    
    return jsonify(
        message="Log collection task queued"
    )
    
    
##########################
##########################
##########################


#################
### ENDPOINTS ###
#################


@app.route('/terminal_endpoint/<endpoint>',methods = ['POST', 'GET'])
def terminal_endpoint(endpoint):
    global_logger.info(f'REQUEST INFORMATION > IP: {request.remote_addr}, Route: {request.path}, Params: {request.args.to_dict()}')
    return Response(
        endpoint_streamer_mapping[endpoint].read_file_continues(
            is_yield=True,
            sleep_time=0.05, # 0.3
            new_sleep_time=0.07,
            content_control=False
        ), 
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'X-Accel-Buffering': 'no' # Disable buffering
        }
    )


@app.route('/download_terminal_log/<endpoint>')
def download_terminal_log(endpoint):
    global_logger.info(f'REQUEST INFORMATION > IP: {request.remote_addr}, Route: {request.path}, Params: {request.args.to_dict()}')
    archive_path = root_path_archives + f"{endpoint}_terminal_logs.zip"
    
    archive_files(
        endpoint_thread_mapping[endpoint].get_Logs(), 
        archive_path
    )
    return send_from_directory(
        path=f"{endpoint}_terminal_logs.zip",
        directory=root_path_archives,
        as_attachment=True,
        download_name=f"{endpoint}_terminal_logs.zip"
    )
    

@app.route('/endpoint_stop/<endpoint>',methods = ['POST', 'GET'])
def endpoint_stop(endpoint):
    global_logger.info(f'REQUEST INFORMATION > IP: {request.remote_addr}, Route: {request.path}, Params: {request.args.to_dict()}')
    
    if not endpoint_thread_mapping[endpoint].task_stop_lock.locked():
        with endpoint_thread_mapping[endpoint].task_stop_lock:
            endpoint_thread_mapping[endpoint].stop_Task()
            endpoint_thread_mapping[endpoint].wait_To_Stop_Task()
    else:
        return jsonify(
            message=f"{endpoint} task stop already running"
        )
    
    return jsonify(
        message=f"{endpoint} tasks stopped"
    )

    
@app.route('/clear_action_files/<endpoint>',methods = ['POST', 'GET'])
def clear_action_files(endpoint):
    global_logger.info(f'REQUEST INFORMATION > IP: {request.remote_addr}, Route: {request.path}, Params: {request.args.to_dict()}')
    
    if endpoint == "fqdn":
        folder_path = root_fqdn_folder
    elif endpoint == "cleanup":
        folder_path= "not-found"
    elif endpoint == "log_collection":
        folder_path = root_log_collection_folder
    elif endpoint == "backup":
        folder_path = "not-found"
    else:
        return jsonify(
            message=f"Endpoint {endpoint} not found"
        )
    
    response = delete_folder(folder_path)
    
    return jsonify(
        message=f"Clear Action Files Response: {response}"
    )


@app.route('/file_table_download/<endpoint>/<foldername>',methods = ['POST', 'GET'])
def file_table_download(endpoint, foldername):
    global_logger.info(f'REQUEST INFORMATION > IP: {request.remote_addr}, Route: {request.path}, Params: {request.args.to_dict()}')

    if endpoint == "fqdn":
        folder_path = fqdn_thread.get_hosts_folder()
    elif endpoint == "cleanup":
        folder_path= ""
    elif endpoint == "log_collection":
        folder_path = log_collection_thread.get_Collected_Log_Folder()
    elif endpoint == "backup":
        folder_path = ""
    else:
        return jsonify(
            message=f"Endpoint {endpoint} not found"
        )
    
    folders = list_dir(folder_path)
    
    if foldername in folders:
        archive_name = f"{endpoint}_files"
        archive_directory(
            archive_name=archive_name,
            directory_to_compress=folder_path + foldername,
            output_directory=root_path_archives,
        )
        return send_from_directory(
            path=f"{archive_name}.zip",
            directory=root_path_archives,
            as_attachment=True,
            download_name=f"{endpoint}_files_{foldername}.zip"
        )
    else:
        return jsonify(
            message=f"File {foldername} not found"
        )


@app.route('/folder_info/<endpoint>',methods = ['POST', 'GET'])
def folder_info(endpoint):
    global_logger.info(f'REQUEST INFORMATION > IP: {request.remote_addr}, Route: {request.path}, Params: {request.args.to_dict()}')
    directory_paths = {
        "log_collection": log_collection_thread.get_Collected_Log_Folder(),
        "fqdn": fqdn_thread.get_hosts_folder(),
        "cleanup": "",
        "backup": "",
    }
    
    if endpoint in directory_paths.keys():
        folder_info = get_directory_info(directory_paths[endpoint])
        # for dir_info in folder_info:
        #     print(dir_info)
        if folder_info == []:
            folder_info = [
                {
                    # "message": "No content in folder found",
                    "size": "0",
                    "name": "-",
                    "creation_date": "-",
                }
            ]
        return jsonify(folder_info)
    else:
        folder_info = [
            {
                "message": "No endpoint found",
                "size": "0",
                "name": "-",
                "creation_date": "-",
            }
        ]
        return jsonify(folder_info)

#################
#################
#################


#############
### PAGES ###
#############


@app.route('/',methods = ['POST', 'GET'])
def index():
    global_logger.info(f'REQUEST INFORMATION > IP: {request.remote_addr}, Route: {request.path}, Params: {request.args.to_dict()}')
    return render_template(
        'index.html',
        page_id="index"
    )


@app.route('/about',methods = ['POST', 'GET'])
def about():
    global_logger.info(f'REQUEST INFORMATION > IP: {request.remote_addr}, Route: {request.path}, Params: {request.args.to_dict()}')
    return render_template(
        'about.html',
        page_id="about"
    )


@app.route('/404',methods = ['POST', 'GET'])
def not_found():
    global_logger.info(f'REQUEST INFORMATION > IP: {request.remote_addr}, Route: {request.path}, Params: {request.args.to_dict()}')
    return render_template(
        '404.html',
        page_id="404"
    )


if __name__ == '__main__':
    app.run(
        host=os.getenv("HOST", "0.0.0.0"), 
        port=int(os.getenv("PORT", 5005)), 
        debug = True
    )