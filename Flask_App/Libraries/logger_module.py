import logging
import os
import sys
from Flask_App.paths import root_path_logs, root_path_log, root_path_global_logs 





# if os.path.exists("logs.log"):
#     os.remove("logs.log")

if not os.path.exists(root_path_log):
    os.mkdir(root_path_log)



# Logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

logger_stdout_formatter = logging.Formatter('%(levelname)s | %(message)s')
logger_file_formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', '%m-%d-%Y %H:%M:%S')

logger_stdout_handler = logging.StreamHandler(sys.stdout)
logger_stdout_handler.setLevel(logging.DEBUG)
logger_stdout_handler.setFormatter(logger_stdout_formatter)

logger_file_handler = logging.FileHandler(root_path_logs)
logger_file_handler.setLevel(logging.DEBUG)
logger_file_handler.setFormatter(logger_file_formatter)

logger.addHandler(logger_file_handler)
logger.addHandler(logger_stdout_handler)



# Global Logger
global_logger = logging.getLogger("Global Logger")
global_logger.setLevel(logging.INFO)

global_logger_stdout_formatter = logging.Formatter('%(levelname)s | %(message)s')
global_logger_file_formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', '%m-%d-%Y %H:%M:%S')

global_logger_stdout_handler = logging.StreamHandler(sys.stdout)
global_logger_stdout_handler.setLevel(logging.DEBUG)
global_logger_stdout_handler.setFormatter(global_logger_stdout_formatter)

global_logger_file_handler = logging.FileHandler(root_path_global_logs)
global_logger_file_handler.setLevel(logging.DEBUG)
global_logger_file_handler.setFormatter(global_logger_file_formatter)

global_logger.addHandler(global_logger_file_handler)
global_logger.addHandler(global_logger_stdout_handler)



# # FQDN Logger
# fqdn_logger = logging.getLogger("FQDN Logger")
# fqdn_logger.setLevel(logging.INFO)

# fqdn_logger_stdout_formatter = logging.Formatter('%(levelname)s | %(message)s')
# fqdn_logger_file_formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', '%m-%d-%Y %H:%M:%S')

# fqdn_logger_stdout_handler = logging.StreamHandler(sys.stdout)
# fqdn_logger_stdout_handler.setLevel(logging.DEBUG)
# fqdn_logger_stdout_handler.setFormatter(fqdn_logger_stdout_formatter)

# fqdn_logger_file_handler = logging.FileHandler(root_path_fqdn_logs)
# fqdn_logger_file_handler.setLevel(logging.DEBUG)
# fqdn_logger_file_handler.setFormatter(fqdn_logger_file_formatter)

# fqdn_logger.addHandler(fqdn_logger_file_handler)
# fqdn_logger.addHandler(fqdn_logger_stdout_handler)



# # Cleanup Logger
# cleanup_logger = logging.getLogger("Cleanup Logger")
# cleanup_logger.setLevel(logging.INFO)

# cleanup_logger_stdout_formatter = logging.Formatter('%(levelname)s | %(message)s')
# cleanup_logger_file_formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', '%m-%d-%Y %H:%M:%S')

# cleanup_logger_stdout_handler = logging.StreamHandler(sys.stdout)
# cleanup_logger_stdout_handler.setLevel(logging.DEBUG)
# cleanup_logger_stdout_handler.setFormatter(cleanup_logger_stdout_formatter)

# cleanup_logger_file_handler = logging.FileHandler(root_path_cleanup_logs)
# cleanup_logger_file_handler.setLevel(logging.DEBUG)
# cleanup_logger_file_handler.setFormatter(cleanup_logger_file_formatter)

# cleanup_logger.addHandler(cleanup_logger_file_handler)
# cleanup_logger.addHandler(cleanup_logger_stdout_handler)



# # Log Collection Logger
# log_collection_logger = logging.getLogger("Log Collection Logger")
# log_collection_logger.setLevel(logging.DEBUG)

# log_collection_logger_stdout_formatter = logging.Formatter('%(levelname)s | %(message)s')
# log_collection_logger_file_formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', '%m-%d-%Y %H:%M:%S')

# log_collection_logger_stdout_handler = logging.StreamHandler(sys.stdout)
# log_collection_logger_stdout_handler.setLevel(logging.DEBUG)
# log_collection_logger_stdout_handler.setFormatter(log_collection_logger_stdout_formatter)

# log_collection_logger_file_handler = logging.FileHandler(root_path_log_collection_logs)
# log_collection_logger_file_handler.setLevel(logging.DEBUG)
# log_collection_logger_file_handler.setFormatter(log_collection_logger_file_formatter)

# log_collection_logger.addHandler(log_collection_logger_file_handler)
# log_collection_logger.addHandler(log_collection_logger_stdout_handler)