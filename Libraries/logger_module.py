import logging
import os
import sys




root_path_log = "./app_logs/"
root_path_logs = root_path_log + "logs.log"
root_path_global_logs = root_path_log + "global.log"
root_path_fqdn_logs = root_path_log + "fqdn.log"
root_path_cleanup_logs = root_path_log + "cleanup.log"
root_path_log_collection_logs = root_path_log + "log_collection.log"



# if os.path.exists("logs.log"):
#     os.remove("logs.log")

if not os.path.exists(root_path_log):
    os.mkdir(root_path_log)



# Logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

stdout_formatter = logging.Formatter('%(levelname)s | %(message)s')
file_formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', '%m-%d-%Y %H:%M:%S')

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(stdout_formatter)

file_handler = logging.FileHandler(root_path_logs)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(file_formatter)

logger.addHandler(file_handler)
logger.addHandler(stdout_handler)



# Global Logger
global_logger = logging.getLogger("Global Logger")
global_logger.setLevel(logging.INFO)

stdout_formatter = logging.Formatter('%(levelname)s | %(message)s')
file_formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', '%m-%d-%Y %H:%M:%S')

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(stdout_formatter)

file_handler = logging.FileHandler(root_path_global_logs)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(file_formatter)

global_logger.addHandler(file_handler)
global_logger.addHandler(stdout_handler)



# FQDN Logger
fqdn_logger = logging.getLogger("FQDN Logger")
fqdn_logger.setLevel(logging.INFO)

stdout_formatter = logging.Formatter('%(levelname)s | %(message)s')
file_formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', '%m-%d-%Y %H:%M:%S')

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(stdout_formatter)

file_handler = logging.FileHandler(root_path_fqdn_logs)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(file_formatter)

fqdn_logger.addHandler(file_handler)
fqdn_logger.addHandler(stdout_handler)



# Cleanup Logger
cleanup_logger = logging.getLogger("Cleanup Logger")
cleanup_logger.setLevel(logging.INFO)

stdout_formatter = logging.Formatter('%(levelname)s | %(message)s')
file_formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', '%m-%d-%Y %H:%M:%S')

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(stdout_formatter)

file_handler = logging.FileHandler(root_path_cleanup_logs)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(file_formatter)

cleanup_logger.addHandler(file_handler)
cleanup_logger.addHandler(stdout_handler)



# Log Collection Logger
log_collection_logger = logging.getLogger("Log Collection Logger")
log_collection_logger.setLevel(logging.DEBUG)

stdout_formatter = logging.Formatter('%(levelname)s | %(message)s')
file_formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', '%m-%d-%Y %H:%M:%S')

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(stdout_formatter)

file_handler = logging.FileHandler(root_path_log_collection_logs)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(file_formatter)

log_collection_logger.addHandler(file_handler)
log_collection_logger.addHandler(stdout_handler)