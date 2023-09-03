import logging

from Flask_App.Classes.FQDN_Class import FQDN_Class
from Flask_App.Classes.Cleanup_Class import Cleanup_Class
from Flask_App.Classes.Log_Collection_Class import Log_Collection_Class
from Flask_App.Classes.File_Handler import File_Content_Streamer_Thread

from Flask_App.paths import root_path_log_collection_logs, root_log_collection_folder, root_fqdn_folder, root_path_cleanup_logs, root_path_fqdn_logs


maxBytes = 64*1024


# Log Collection Thread
log_collection_thread = Log_Collection_Class(
    name="Log Collection Thread",
    download_path=root_log_collection_folder,
    logger=None,
    logger_level_stdo=logging.DEBUG,
    logger_level_file=logging.DEBUG,
    logger_file_path=root_path_log_collection_logs,
    mode="a", 
    maxBytes=maxBytes, 
    backupCount=2
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
cleanup_thread = Cleanup_Class(
    name="Cleanup Thread",
    logger=None,
    logger_level_stdo=logging.DEBUG,
    logger_level_file=logging.DEBUG,
    logger_file_path=root_path_cleanup_logs,
    mode="a", 
    maxBytes=maxBytes, 
    backupCount=2
)
cleanup_thread.start_Thread()

cleanup_logger_streamer = File_Content_Streamer_Thread(
    path=root_path_cleanup_logs,
    # wait_thread=log_collection_thread,
    is_yield=True
)



# FQDN Thread
fqdn_thread = FQDN_Class(
    name="FQDN Thread",
    hosts_folder=root_fqdn_folder,
    logger=None,
    logger_level_stdo=logging.DEBUG,
    logger_level_file=logging.DEBUG,
    logger_file_path=root_path_fqdn_logs,
    mode="a", 
    maxBytes=maxBytes, 
    backupCount=2
)
fqdn_thread.start_Thread()

fqdn_logger_streamer = File_Content_Streamer_Thread(
    path=root_path_fqdn_logs,
    # wait_thread=log_collection_thread,
    is_yield=True
)
    