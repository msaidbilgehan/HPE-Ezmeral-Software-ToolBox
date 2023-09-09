from datetime import datetime
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


def get_directory_info(directory_path, round_in_gb=3):
    if os.path.exists(directory_path) == False:
        return []
    # Belirtilen dizindeki tüm klasörleri listeleyelim
    all_items = os.listdir(directory_path)
    dirs = [item for item in all_items if os.path.isdir(os.path.join(directory_path, item))]

    dir_info = []

    for dir_name in dirs:
        full_path = os.path.join(directory_path, dir_name)

        # Klasörün boyutunu hesaplayalım (alt klasörler ve dosyalar dahil)
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(full_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp) 
        total_size = round(total_size * 10**-9, round_in_gb)
        
        # Oluşturma tarihini alalım
        creation_timestamp = os.path.getctime(full_path)
        creation_date = datetime.fromtimestamp(creation_timestamp).strftime('%Y-%m-%d %H:%M:%S')

        dir_info.append({
            'name': dir_name,
            'size': total_size,
            'creation_date': creation_date
        })

    # Klasör bilgilerini tarih bilgisine göre sıralayalım
    sorted_dir_info = sorted(dir_info, key=lambda x: x['creation_date'], reverse=True)
    
    return sorted_dir_info



def list_dir(path):
    return os.listdir(path)

                
def delete_folder(path):
    response = "Deleted"
    
    if os.path.exists(path):
        try:
            shutil.rmtree(path)
        except OSError as e:
            response = f"Can not delete folder: {e.filename} - {e.strerror}."
    else:
        response = "No Log Collection Folder Found!"
    
    return response


def archive_directory(directory_to_compress:str, output_directory:str, archive_name:str, delete_exist:bool=True):
    output_archive_path = os.path.join(output_directory, archive_name)
    if delete_exist and os.path.exists(output_archive_path + ".zip"):
        os.remove(output_archive_path + ".zip")
        
    # print(f"Creating ZIP File: {output_archive_path}.zip to compress {directory_to_compress}")
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
            file_name_only = os.path.basename(file)
            zipper.write(file, arcname=file_name_only)
            
    # print(f"ZIP File Created: {output_archive_path}")
    return output_archive_path
