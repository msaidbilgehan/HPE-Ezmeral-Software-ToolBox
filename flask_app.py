import json

from flask import Flask, Response
from flask import render_template
from flask import Flask, jsonify, request

from Threads.configurations import log_collection_logger_streamer, log_collection_thread
from threading import Lock

app = Flask(__name__, template_folder='frontend/pages', static_folder='frontend/static')


__log_collection_endpoint_lock = Lock()
__log_collection_stop_endpoint_lock = Lock()


@app.route('/',methods = ['POST', 'GET'])
def index():
    return render_template('index.html')


###################
### CLEANUP API ###
###################


@app.route('/cleanup',methods = ['POST', 'GET'])
def cleanup_page():
    return render_template('cleanup.html')

###################
###################
###################

######################
### FQDN SETUP API ###
######################

@app.route('/fqdn',methods = ['POST', 'GET'])
def fqdn_page():
    return render_template('fqdn.html')

######################
######################
######################

##########################
### LOG COLLECTION API ###
##########################

@app.route('/log_collection',methods = ['POST', 'GET'])
def log_collection_page():
    return render_template(
        'log_collection.html'
    )
    

@app.route('/log_collection_endpoint',methods = ['POST', 'GET'])
def log_collection_endpoint():
    
    global __log_collection_endpoint_lock
    
    if not __log_collection_endpoint_lock.locked():
        with __log_collection_endpoint_lock:
            ssh_username_json = request.args.get('ssh_username')
            ssh_password_json = request.args.get('ssh_password')
            ip_addresses_json = request.args.get('ip_addresses')
            
            
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


@app.route('/log_collection_log_endpoint',methods = ['POST', 'GET'])
def log_collection_log_endpoint():
    return Response(
        log_collection_logger_streamer.read_file_continues(
            is_yield=True,
            sleep_time=0, # 0.3
            new_sleep_time=1,
            content_control=False
        ), 
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'X-Accel-Buffering': 'no' # Disable buffering
        }
    )
    

@app.route('/clear_Log_Collection_Log_Files',methods = ['POST', 'GET'])
def clear_Log_Collection_Log_Files():
    log_collection_logger_streamer.clear_File_Content()
    
    return jsonify(
        message="Log contents are cleared"
    )
    

@app.route('/clear_Log_Buffer',methods = ['POST', 'GET'])
def clear_Log_Buffer():
    log_collection_logger_streamer.clear_Buffer()
    
    return jsonify(
        message="Log buffer cleared"
    )
    

@app.route('/log_collection_log_stop_endpoint',methods = ['POST', 'GET'])
def log_collection_stop_endpoint():
    global __log_collection_stop_endpoint_lock
    
    if not __log_collection_stop_endpoint_lock.locked():
        with __log_collection_stop_endpoint_lock:
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


@app.route('/about',methods = ['POST', 'GET'])
def about():
    return render_template('about.html')


@app.route('/404',methods = ['POST', 'GET'])
def not_found():
    return render_template('404.html')



if __name__ == '__main__':
   app.run(debug = True)