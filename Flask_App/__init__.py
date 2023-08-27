import os
from Flask_App.paths import root_path

if not os.path.exists(root_path):
    os.makedirs(root_path)