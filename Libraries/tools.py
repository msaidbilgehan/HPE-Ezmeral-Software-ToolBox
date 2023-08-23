import os
import time
import shutil
import zipfile


def read_log_file(path, wait_thread=None):
    with open(path, 'r') as file:
        while True:
            line = file.readline().strip()
            if line:
                # print(line)
                yield f"data: {line}\n\n"  # Format for SSE (data: at the start and 2 new line characters at the end)
            
            time.sleep(1)  # Wait for new content
            
            if wait_thread is not None:
                if not wait_thread.is_alive():
                    break


def list_dir(path):
    return os.listdir(path)

                
def delete_folder(path):
    response = "Deleted"
    
    if os.path.exists(path):
        try:
            shutil.rmtree(path)
        except OSError as e:
            response = f"Error: {e.filename} - {e.strerror}."
    else:
        response = "No Log Collection Folder Found!"
    
    return response


def archive_directory(directory_to_compress:str, output_directory:str, archive_name:str, delete_exist:bool=True):
    output_archive_path = os.path.join(output_directory, archive_name)
    if delete_exist and os.path.exists(output_archive_path + ".zip"):
        os.remove(output_archive_path + ".zip")
        
    print(f"Creating ZIP File: {output_archive_path}.zip to compress {directory_to_compress}")
    return shutil.make_archive(
        base_name=output_archive_path,
        format='zip', 
        root_dir=directory_to_compress
    )


def archive_files(files:list[str], output_archive_path:str, delete_exist:bool=True):
    if delete_exist and os.path.exists(output_archive_path):
        os.remove(output_archive_path)
    
    # print(f"Creating ZIP File: {output_archive_path}")
    
    # Create ZIP
    with zipfile.ZipFile(output_archive_path, 'w') as zipper:
        for file in files:
            # print(f"Adding File: {file}")
            zipper.write(file)
            
    # print(f"ZIP File Created: {output_archive_path}")
    return output_archive_path
