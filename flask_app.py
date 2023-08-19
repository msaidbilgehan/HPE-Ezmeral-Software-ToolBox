import json

from flask import Flask, Response
from flask import render_template
from flask import Flask, jsonify, request

# from flask_commands import log_collection
from Pools.thread_to_task_pool import log_collection_logger_streamer, log_collection_thread


app = Flask(__name__, template_folder='frontend/pages', static_folder='frontend/static')


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
    

@app.route('/log_collection_API',methods = ['POST', 'GET'])
def log_collection_API():

    # ssh_credentials_json = request.args.get('ssh_credentials')
    ip_addresses_json = request.args.get('ip_addresses')
    if ip_addresses_json is not None:
        ip_addresses = json.loads(ip_addresses_json)
    else:
        ip_addresses = []
        
    parameters = {
        "ssh_username": "mapr",
        "ssh_password": "mapr",
        "ip_addresses": ip_addresses
    }
        
    log_collection_thread.set_Parameters(
        parameters=parameters
    )
        
    if not log_collection_thread.is_alive():
        log_collection_thread.start()
    else:
        # log_collection_thread.stop_Thread()
        # log_collection_thread.start()
        jsonify(
            message="Log collection is already running"
        )


    return Response(
        log_collection_logger_streamer.read_file_continues(
            is_yield=True,
            sleep_time=1
        ), 
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'X-Accel-Buffering': 'no' # Disable buffering
        }
    )


@app.route('/log_collection_buffered_API',methods = ['POST', 'GET'])
def log_collection_buffered_API():
    return Response(
        log_collection_logger_streamer.read_file_continues(
            is_yield=True,
            sleep_time=0# 0.3
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