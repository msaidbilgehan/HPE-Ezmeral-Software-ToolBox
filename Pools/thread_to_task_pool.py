
from Classes.File_Handler import File_Content_Streamer_Thread
from Classes.Task_Handler import Task_Handler_Thread
from Libraries.logger_module import root_path_log_collection_logs #, root_path_cleanup_logs, root_path_fqdn_logs
from flask_commands import log_collection #, cleanup, fqdn_setup


# Log Collection Thread
log_collection_thread = Task_Handler_Thread(
    task=log_collection,
    parameters=[
        "mapr",
        "mapr",
        ["10.34.2.122"]
    ]
)
log_collection_logger_streamer = File_Content_Streamer_Thread(
    path=root_path_log_collection_logs,
    # wait_thread=log_collection_thread,
    is_yield=True
)
# log_collection_logger_thread.start()


# Cleanup Thread
# cleanup_thread = Task_Handler_Thread(
#     task=cleanup,
#     parameters=[]
# )
# cleanup_logger_thread = File_Content_Streamer_Thread(root_path_cleanup_logs)
# log_collection_logger_thread.start()



# FQDN Thread
# fqdn_setup_thread = Task_Handler_Thread(
#     task=fqdn_setup,
#     parameters=[]
# )
    
# fqdn_logger_thread = File_Content_Streamer_Thread(root_path_fqdn_logs)
# log_collection_logger_thread.start()


# Global Log Streamer Thread
# global_logger_thread = File_Content_Streamer_Thread(root_path_global_logs)
# log_collection_logger_thread.start()


# Main Log Streamer Thread
# logger_thread = File_Content_Streamer_Thread(root_path_logs)
# log_collection_logger_thread.start()

    