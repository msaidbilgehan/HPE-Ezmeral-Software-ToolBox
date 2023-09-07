import os
from Flask_App.paths import root_files_path, root_path_archives, root_log_collection_folder, root_fqdn_folder

if not os.path.exists(root_files_path):
    os.makedirs(root_files_path)
    
if not os.path.exists(root_path_archives):
    os.makedirs(root_path_archives)
    
if not os.path.exists(root_log_collection_folder):
    os.makedirs(root_log_collection_folder)
    
if not os.path.exists(root_fqdn_folder):
    os.makedirs(root_fqdn_folder)