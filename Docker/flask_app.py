import json
import os

from flask import Flask, jsonify, request, send_from_directory, render_template, Response

from Flask_App.Libraries.tools import delete_folder, archive_files, archive_directory, get_directory_info, list_dir
from Flask_App.paths import app_path, root_path_archives, root_log_collection_folder
from Flask_App.Threads.configurations import cleanup_thread, cleanup_logger_streamer, log_collection_logger_streamer, log_collection_thread, fqdn_thread, fqdn_logger_streamer
from Flask_App.Libraries.logger_module import global_logger



app = Flask(__name__, template_folder=f'{app_path}frontend/pages', static_folder=f'{app_path}frontend/static')



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
            message="fqdn task already running"
        )
    
    return jsonify(
        message="fqdn task queued"
    )


@app.route('/fqdn_terminal_endpoint',methods = ['POST', 'GET'])
def fqdn_terminal_endpoint():
    global_logger.info(f'REQUEST INFORMATION > IP: {request.remote_addr}, Route: {request.path}, Params: {request.args.to_dict()}')
    return Response(
        fqdn_logger_streamer.read_file_continues(
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


@app.route('/fqdn_download_terminal_log_endpoint')
def fqdn_download_terminal_log_endpoint():
    global_logger.info(f'REQUEST INFORMATION > IP: {request.remote_addr}, Route: {request.path}, Params: {request.args.to_dict()}')
    archive_path = root_path_archives + "fqdn_terminal_logs.zip"
    archive_files(
        fqdn_thread.get_Logs(), 
        archive_path
    )
    return send_from_directory(
        path="fqdn_terminal_logs.zip",
        directory=root_path_archives,
        as_attachment=True,
        download_name="fqdn_terminal_logs.zip"
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
                script_path="./cleanup.py"
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


@app.route('/cleanup_terminal_endpoint',methods = ['POST', 'GET'])
def cleanup_terminal_endpoint():
    global_logger.info(f'REQUEST INFORMATION > IP: {request.remote_addr}, Route: {request.path}, Params: {request.args.to_dict()}')
    return Response(
        cleanup_logger_streamer.read_file_continues(
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


@app.route('/cleanup_download_terminal_log_endpoint')
def cleanup_download_terminal_log_endpoint():
    global_logger.info(f'REQUEST INFORMATION > IP: {request.remote_addr}, Route: {request.path}, Params: {request.args.to_dict()}')
    archive_path = root_path_archives + "cleanup_terminal_logs.zip"
    archive_files(
        cleanup_thread.get_Logs(), 
        archive_path
    )
    return send_from_directory(
        path="cleanup_terminal_logs.zip",
        directory=root_path_archives,
        as_attachment=True,
        download_name="cleanup_terminal_logs.zip"
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


@app.route('/log_collection_terminal_endpoint',methods = ['POST', 'GET'])
def log_collection_terminal_endpoint():
    global_logger.info(f'REQUEST INFORMATION > IP: {request.remote_addr}, Route: {request.path}, Params: {request.args.to_dict()}')
    return Response(
        log_collection_logger_streamer.read_file_continues(
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


@app.route('/log_collection_list_collected_endpoint',methods = ['POST', 'GET'])
def log_collection_list_collected_endpoint():
    global_logger.info(f'REQUEST INFORMATION > IP: {request.remote_addr}, Route: {request.path}, Params: {request.args.to_dict()}')
    return jsonify(
        message=log_collection_thread.get_Collected_Log_Folder()
    )


@app.route('/log_collection_download_collected_endpoint')
def log_collection_download_collected_endpoint():
    global_logger.info(f'REQUEST INFORMATION > IP: {request.remote_addr}, Route: {request.path}, Params: {request.args.to_dict()}')
    archive_name = "collected_logs"
    # archive_path = root_path_archives + archive_name + ".zip"
    
    archive_directory(
        archive_name=archive_name,
        directory_to_compress=log_collection_thread.get_Collected_Log_Folder(),
        output_directory=root_path_archives,
    )
    return send_from_directory(
        path="collected_logs.zip",
        directory=root_path_archives,
        as_attachment=True,
        download_name="collected_logs.zip"
    )


@app.route('/log_collection_download_terminal_log_endpoint')
def log_collection_download_terminal_log_endpoint():
    global_logger.info(f'REQUEST INFORMATION > IP: {request.remote_addr}, Route: {request.path}, Params: {request.args.to_dict()}')
    archive_path = root_path_archives + "log_collection_terminal_logs.zip"
    archive_files(
        log_collection_thread.get_Logs(), 
        archive_path
    )
    return send_from_directory(
        path="log_collection_terminal_logs.zip",
        directory=root_path_archives,
        as_attachment=True,
        download_name="log_collection_terminal_logs.zip"
    )

    
@app.route('/clear_Collected_Log_Files',methods = ['POST', 'GET'])
def clear_Collected_Log_Files():
    global_logger.info(f'REQUEST INFORMATION > IP: {request.remote_addr}, Route: {request.path}, Params: {request.args.to_dict()}')
    response = delete_folder(root_log_collection_folder)
    
    return jsonify(
        message=f"Collected Log Files Response: {response}"
    )
    

@app.route('/clear_Log_Collection_Log_Files',methods = ['POST', 'GET'])
def clear_Log_Collection_Log_Files():
    global_logger.info(f'REQUEST INFORMATION > IP: {request.remote_addr}, Route: {request.path}, Params: {request.args.to_dict()}')
    log_collection_logger_streamer.clear_File_Content()
    
    return jsonify(
        message="Log contents are cleared"
    )
    

@app.route('/clear_Log_Buffer',methods = ['POST', 'GET'])
def clear_Log_Buffer():
    global_logger.info(f'REQUEST INFORMATION > IP: {request.remote_addr}, Route: {request.path}, Params: {request.args.to_dict()}')
    log_collection_logger_streamer.clear_Buffer()
    
    return jsonify(
        message="Log buffer cleared"
    )
    

@app.route('/log_collection_log_stop_endpoint',methods = ['POST', 'GET'])
def log_collection_stop_endpoint():
    global_logger.info(f'REQUEST INFORMATION > IP: {request.remote_addr}, Route: {request.path}, Params: {request.args.to_dict()}')
    if not log_collection_thread.task_stop_lock.locked():
        with log_collection_thread.task_stop_lock:
            log_collection_thread.stop_Task()
            log_collection_thread.wait_To_Stop_Task()
    else:
        return jsonify(
            message="Log collection task stop already running"
        )
    
    return jsonify(
        message="Log collection tasks stopped"
    )
    
    
##########################
##########################
##########################


#################
### ENDPOINTS ###
#################


@app.route('/file_table_download/<endpoint>/<foldername>',methods = ['POST', 'GET'])
def file_table_download(endpoint, foldername):
    global_logger.info(f'REQUEST INFORMATION > IP: {request.remote_addr}, Route: {request.path}, Params: {request.args.to_dict()}')

    if endpoint == "fqdn":
        folder_path = fqdn_thread.get_hosts_folder()
    elif endpoint == "cleanup":
        folder_path= ""
    elif endpoint == "log_collection":
        folder_path = log_collection_thread.get_Collected_Log_Folder()
    else:
        return jsonify(
            message=f"Endpoint {endpoint} not found"
        )

    folders = list_dir(folder_path)
    
    
    if foldername in folders:
        archive_directory(
            archive_name="collected_logs",
            directory_to_compress=folder_path + foldername,
            output_directory=root_path_archives,
        )
        
        return send_from_directory(
            path="collected_logs.zip",
            directory=root_path_archives,
            as_attachment=True,
            download_name="collected_logs.zip"
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