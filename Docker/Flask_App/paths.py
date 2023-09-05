import os

app_path = os.path.dirname(__file__) + "/"

# Folder for all Thread/Endpoint files
root_path = app_path + "Files/"

# Log Download Path
root_log_collection_folder = root_path + "log_collection/"
root_fqdn_folder = root_path + "fqdn/"

# Files will be sent to Client 
root_path_archives = root_path + "archives/"

# Logger Paths
root_path_log = app_path + "app_logs/"
root_path_logs = root_path_log + "logs.log"
root_path_global_logs = root_path_log + "global.log"
root_path_fqdn_logs = root_path_log + "fqdn.log"
root_path_cleanup_logs = root_path_log + "cleanup.log"
root_path_log_collection_logs = root_path_log + "log_collection.log"
root_path_backup_logs = root_path_log + "backup.log"