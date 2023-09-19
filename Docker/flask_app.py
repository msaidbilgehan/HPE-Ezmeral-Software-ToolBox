import json
import os

from flask import Flask, jsonify, request, send_from_directory, render_template, Response
from Flask_App.Classes.File_Handler import File_Content_Streamer_Thread
from Flask_App.Classes.Task_Handler import Task_Handler_Class
from Flask_App.Classes.Notification_Handler import Notification_Status

from Flask_App.Libraries.tools import delete_folder, archive_files, archive_directory, get_directory_info, list_dir
from Flask_App.paths import app_path, root_path_archives, root_upload_path, root_log_collection_folder, root_fqdn_folder
from Flask_App.Threads.configurations import cleanup_thread, cleanup_logger_streamer, log_collection_logger_streamer, log_collection_thread, fqdn_thread, fqdn_logger_streamer, backup_restore_thread, backup_restore_logger_streamer, notification_thread
from Flask_App.Libraries.logger_module import global_logger



########################
### GLOBAL VARIABLES ###
########################


app = Flask(__name__, template_folder=f'{app_path}frontend/pages', static_folder=f'{app_path}frontend/static')
app.secret_key = bytes(f'salsaT.reOs01{os.urandom(16)}', encoding='utf-8')

endpoint_thread_mapping: dict[str, Task_Handler_Class] = {
    "cleanup": cleanup_thread,
    "log_collection": log_collection_thread,
    "fqdn": fqdn_thread,
    "backup": backup_restore_thread,
    "restore": backup_restore_thread,
}

endpoint_streamer_mapping: dict[str, File_Content_Streamer_Thread] = {
    "cleanup": cleanup_logger_streamer,
    "log_collection": log_collection_logger_streamer,
    "fqdn": fqdn_logger_streamer,
    "backup": backup_restore_logger_streamer,
    "restore": backup_restore_logger_streamer,
}

endpoint_directory_paths = {
    "cleanup": "",
    "log_collection": log_collection_thread.get_Collected_Log_Folder(),
    "fqdn": fqdn_thread.get_hosts_folder(),
    "backup": "",
    "restore": "",
}

backup_path = "/root/snapshot"
backup_script = "daily_rotation_mapr_snapshot.sh"
backup_script_upload_path="/home/{ssh_username}/"

restore_script = "daily_rotation_mapr_restore.sh"
restore_script_upload_path="/home/{ssh_username}/"



#########################
### GENERAL FUNCTIONS ###
#########################


def parameter_parser_ssh_credentials(args: dict):
    ssh_username_json = args.get('ssh_username', "")
    ssh_password_json = args.get('ssh_password', "")
    
    if ssh_username_json != "":
        ssh_username = json.loads(ssh_username_json)
    else:
        ssh_username = ssh_username_json
        
    if ssh_password_json != "":
        ssh_password = json.loads(ssh_password_json)
    else:
        ssh_password = ssh_password_json
    
    return ssh_username, ssh_password


def parameter_parser_ip_hostname(args: dict, only_ip: bool = False):
    ip_hostname_json = args.get('ip_addresses_hostnames', [{"ip": "", "hostname": ""}])
    
    if ip_hostname_json != []:
        ip_addresses_hostnames = json.loads(ip_hostname_json)
    else:
        ip_addresses_hostnames = ip_hostname_json
    
    if only_ip:
        return [ip_address_hostname["ip"] for ip_address_hostname in ip_addresses_hostnames]
    else:
        return ip_addresses_hostnames



###################
### RESTORE API ###
###################


@app.route('/restore',methods = ['POST', 'GET'])
def restore_page():
    global_logger.info(f'REQUEST INFORMATION > IP: {request.remote_addr}, Route: {request.path}, Params: {request.args.to_dict()}')
    return render_template(
        'restore.html',
        page_id="restore"
    )
    
    
@app.route('/restore_endpoint',methods = ['POST', 'GET'])
def restore_endpoint():
    global_logger.info(f'REQUEST INFORMATION > IP: {request.remote_addr}, Route: {request.path}, Params: {request.args.to_dict()}')
            
    ssh_username, ssh_password = parameter_parser_ssh_credentials(request.args)
    ip_address_hostnames = parameter_parser_ip_hostname(request.args, only_ip=True)
    restore_number_json = request.args.get('restore_number', "0")
    
    if ip_address_hostnames != []:
        if not backup_restore_thread.safe_task_lock.locked():
            with backup_restore_thread.safe_task_lock:

                script_upload_path=restore_script_upload_path.format(ssh_username=ssh_username)
                script_path = root_upload_path + restore_script
                
                backup_restore_thread.set_Parameters(
                    ssh_username=ssh_username,
                    ssh_password=ssh_password,
                    ip_addresses=ip_address_hostnames,
                    script_path=script_path,
                    script_upload_path=script_upload_path,
                    script_run_command=f"sudo chmod +x {script_upload_path + restore_script} &&", # One-Shot Run Command
                    add_to_cron=False, # Cron Parameters
                    cron_parameters="", # Cron Parameters
                    script_parameters=restore_number_json,
                )
                
                if not backup_restore_thread.is_Running():
                    backup_restore_thread.start_Task()
                else:
                    backup_restore_thread.stop_Task()
                    backup_restore_thread.wait_To_Stop_Once_Task()
                    backup_restore_thread.start_Task()
        else:
            return jsonify(
                message="Restore task already running"
            )
        
        return jsonify(
            message="Restore task queued"
        )
    else:
        return jsonify(
            message="Parameters missing!"
        )
    
    
@app.route('/restore_control_endpoint',methods = ['POST', 'GET'])
def restore_control_endpoint():
    global_logger.info(f'REQUEST INFORMATION > IP: {request.remote_addr}, Route: {request.path}, Params: {request.args.to_dict()}')
    
    ssh_username, ssh_password = parameter_parser_ssh_credentials(request.args)
    ip_address_hostnames = parameter_parser_ip_hostname(request.args, only_ip=True)
    
    if ip_address_hostnames != []:
        if not backup_restore_thread.safe_task_lock.locked():
            with backup_restore_thread.safe_task_lock:
                
                # response = backup_restore_thread.restore_control(
                #     ssh_username=ssh_username,
                #     ssh_password=ssh_password,
                #     ip_addresses=ip_address_hostnames,
                # )
                
                responses = backup_restore_thread.get_backup_information(
                    ssh_username=ssh_username,
                    ssh_password=ssh_password,
                    ip_addresses=ip_address_hostnames,
                    backup_dir=backup_path,
                )
                
                # temp_response["ip_address"] = ip_address
                # temp_response["response"] = str(response)
                # temp_response["check"] = str(True if stout else False)
                # temp_response["message"] = stout
                
                response_to_client: dict[str, dict] = dict()
                for response in responses:
                    response_to_client[response["ip_address"]] = dict()
                    response_to_client[response["ip_address"]]["backup_information"] = list()
                    response_to_client[response["ip_address"]]["response"] = response["response"]
                    response_to_client[response["ip_address"]]["check"] = response["check"]
                    response_to_client[response["ip_address"]]["message"] = response["message"]
                    
                    lines = response["message"].split("\n")
                    if "" in lines:
                        lines.remove("")

                    for line in lines:
                        parts = line.rsplit(' ')
                        if "" in parts:
                            parts.remove("")
                            
                        if len(parts) == 5:
                            path, date, timestamp, ownership, size = parts
                            response_to_client[response["ip_address"]]["backup_information"].append(
                                {
                                    "path": path,
                                    "date": date,
                                    "timestamp": timestamp,
                                    "ownership": ownership,
                                    "size": size
                                }
                            )
                        else:
                            response_to_client[response["ip_address"]]["backup_information"].append(parts)

                notification_thread.queue_add("Restore Control Finished", Notification_Status.INFO)

                return jsonify(
                    message=response_to_client,
                )
        else:
            return jsonify(
                message="Restore Control task already running"
            )
    else:
        return jsonify(
            message="Parameters missing!"
        )



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
    
    ssh_username, ssh_password = parameter_parser_ssh_credentials(request.args)
    ip_address_hostnames = parameter_parser_ip_hostname(request.args, only_ip=True)
    
    if ip_address_hostnames != []:
        if not backup_restore_thread.safe_task_lock.locked():
            with backup_restore_thread.safe_task_lock:

                script_upload_path = backup_script_upload_path.format(ssh_username=ssh_username)
                script_path = root_upload_path + backup_script

                backup_restore_thread.set_Parameters(
                    ssh_username=ssh_username,
                    ssh_password=ssh_password,
                    ip_addresses=ip_address_hostnames,
                    script_path=script_path,
                    script_upload_path=script_upload_path,
                    script_run_command=f"sudo chmod +x {script_upload_path + backup_script} && sudo", # One-Shot Run Command
                    add_to_cron=True, # Cron Parameters
                    cron_parameters="", # Cron Parameters
                    script_parameters="",
                )
                if not backup_restore_thread.is_Running():
                    backup_restore_thread.start_Task()
                    backup_restore_thread.wait_To_Stop_Once_Task()
                    
                else:
                    backup_restore_thread.stop_Task()
                    backup_restore_thread.wait_To_Stop_Once_Task()
                    backup_restore_thread.start_Task()
        else:
            return jsonify(
                message="Backup task already running"
            )
    else:
        return jsonify(
            message="Parameters missing!"
        )
    
    return jsonify(
        message="Backup task queued"
    )
    
    
@app.route('/backup_control_endpoint',methods = ['POST', 'GET'])
def backup_control_endpoint():
    global_logger.info(f'REQUEST INFORMATION > IP: {request.remote_addr}, Route: {request.path}, Params: {request.args.to_dict()}')
    
    ssh_username, ssh_password = parameter_parser_ssh_credentials(request.args)
    ip_address_hostnames = parameter_parser_ip_hostname(request.args, only_ip=True)
    
    if ip_address_hostnames != []:
        if not backup_restore_thread.safe_task_lock.locked():
            with backup_restore_thread.safe_task_lock:
                
                response = backup_restore_thread.backup_cron_control(
                    ssh_username=ssh_username,
                    ssh_password=ssh_password,
                    ip_addresses=ip_address_hostnames,
                    script_name=backup_script.split(".")[0],
                )
                notification_thread.queue_add("Backup Control Finished", Notification_Status.INFO)
                    
                return jsonify(
                    message=response,
                )
        else:
            return jsonify(
                message="Backup Control task already running"
            )
    else:
        return jsonify(
            message="Parameters missing!"
        )



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
    
            
    ssh_username, ssh_password = parameter_parser_ssh_credentials(request.args)
    ip_address_hostnames = parameter_parser_ip_hostname(request.args, only_ip=False)
    
    if ip_address_hostnames != []:
        if not fqdn_thread.safe_task_lock.locked():
            with fqdn_thread.safe_task_lock:
                
                fqdn_thread.set_Parameters(
                    ssh_username=ssh_username,
                    ssh_password=ssh_password,
                    ip_address_hostnames_list=ip_address_hostnames
                )
                
                if not fqdn_thread.is_Running():
                    fqdn_thread.start_Task()
                    fqdn_thread.wait_To_Stop_Once_Task()
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
    else:
        return jsonify(
            message="Parameters missing!"
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
    
                
    ssh_username, ssh_password = parameter_parser_ssh_credentials(request.args)
    ip_address_hostnames = parameter_parser_ip_hostname(request.args, only_ip=True)
    
    if ip_address_hostnames != []:
        if not cleanup_thread.safe_task_lock.locked():
            with cleanup_thread.safe_task_lock:
                
                
                cleanup_thread.set_Parameters(
                    ssh_username=ssh_username,
                    ssh_password=ssh_password,
                    ip_addresses=ip_address_hostnames,
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
    else:
        return jsonify(
            message="Parameters missing!"
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
            
    ssh_username, ssh_password = parameter_parser_ssh_credentials(request.args)
    ip_address_hostnames = parameter_parser_ip_hostname(request.args, only_ip=True)
    
    if ip_address_hostnames != []:
        if not log_collection_thread.safe_task_lock.locked():
            with log_collection_thread.safe_task_lock:
                
                log_collection_thread.set_Parameters(
                    ssh_username=ssh_username,
                    ssh_password=ssh_password,
                    ip_addresses=ip_address_hostnames
                )
                
                if not log_collection_thread.is_Running():
                    log_collection_thread.start_Task()
                    log_collection_thread.wait_To_Stop_Once_Task()
                else:
                    log_collection_thread.stop_Task()
                    log_collection_thread.wait_To_Stop_Once_Task()
                    log_collection_thread.start_Task()
        else:
            notification_thread.queue_add("Log collection task already running", Notification_Status.WARNING)
            return jsonify(
                message="Log collection task already running"
            )
            
        notification_thread.queue_add("Log collection task queued", Notification_Status.INFO)
        return jsonify(
            message="Log collection task queued"
        )
    else:
        notification_thread.queue_add("Parameters missing!", Notification_Status.WARNING)
        return jsonify(
            message="Parameters missing!"
        )
    
    
##########################
##########################
##########################


#################
### ENDPOINTS ###
#################


@app.route('/notification_endpoint/',methods = ['POST', 'GET'])
def notification_endpoint():
    global_logger.info(f'REQUEST INFORMATION > IP: {request.remote_addr}, Route: {request.path}, Params: {request.args.to_dict()}')
    return Response(
        notification_thread.streamer(), 
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'X-Accel-Buffering': 'no' # Disable buffering
        }
    )


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
    
    if endpoint in endpoint_directory_paths.keys():
        folder_info = get_directory_info(endpoint_directory_paths[endpoint])
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
                "message": "No endpoint found for folder info",
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