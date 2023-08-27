import logging

from Classes.FQDN_Class import FQDN_Class
from Classes.Cleanup_Class import Cleanup_Class
from Classes.Log_Collection_Class import Log_Collection_Class
from Classes.File_Handler import File_Content_Streamer_Thread

from Libraries.logger_module import root_path_log_collection_logs, root_path_cleanup_logs, root_path_fqdn_logs #, log_collection_logger

from paths import root_path_log_collection_logs, root_log_collection_folder, root_fqdn_folder


# Log Collection Thread
log_collection_thread = Log_Collection_Class(
    name="Log Collection Thread",
    download_path=root_log_collection_folder,
    logger=None,
    logger_level_stdo=logging.DEBUG,
    logger_level_file=logging.DEBUG,
    logger_file_path=root_path_log_collection_logs,
    mode="a", 
    maxBytes=128*1024, 
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
    maxBytes=128*1024, 
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
    maxBytes=128*1024, 
    backupCount=2
)
fqdn_thread.start_Thread()

fqdn_logger_streamer = File_Content_Streamer_Thread(
    path=root_path_fqdn_logs,
    # wait_thread=log_collection_thread,
    is_yield=True
)
    