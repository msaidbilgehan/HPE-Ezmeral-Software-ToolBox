
from Classes.File_Handler import File_Content_Streamer_Thread
from Classes.Log_Collection_Class import Log_Collection_Class
from Libraries.logger_module import log_collection_logger, root_path_log_collection_logs #, root_path_cleanup_logs, root_path_fqdn_logs
import logging


# Log Collection Thread
log_collection_thread = Log_Collection_Class(
    name="Log Collection Thread",
    logger=None, # log_collection_logger
    logger_level_stdo=logging.DEBUG,
    logger_level_file=logging.DEBUG,
    logger_file_path=root_path_log_collection_logs,
)
# log_collection_thread.set_Parameters(
#     ssh_username="mapr",
#     ssh_password="mapr",
#     ip_addresses=[]
# )
log_collection_thread.start_Thread()

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

    