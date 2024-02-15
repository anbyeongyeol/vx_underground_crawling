import os
import py7zr

"""
악성코드 샘플 압축 해제 및 PE 파일 필터링
1. 악성코드 샘플 압축 해제(2중일 경우 반복하여 진행)
2. PE 파일이 아닐 경우 필터링 진행
2. 20개 
"""

SAMPLE_PATH = 'APT_Sample'
UNZIP_PATH = f"{SAMPLE_PATH}_unzip"
ZIP_EXTENSION_LIST = ['.zip', '.7z', '.tar', '.rar']
ZIP_PASSWORD = 'infected'

def unzip_7z_file(filename, password, target_dic_path):
    try:
        with py7zr.SevenZipFile(filename, mode='r', password=password) as archive:
            print(f"[+] {filename} Unzip Start!")
            archive.extractall(path = target_dic_path)
            print(f"[+] {filename} Unzip Success!")
            
    except Exception as e:
        print(f"[-] File Unzip Error: {e}")
        
def sample_unzip_start():
    apt_group_list = os.listdir(SAMPLE_PATH)
    # 그룹별 접근
    for i in apt_group_list:
        temp_apt_group = os.path.join(SAMPLE_PATH, i)
        # 그룹별 샘플에 접근
        for k in os.listdir(temp_apt_group):
            sample_pull_path = os.path.join(temp_apt_group, k)
            extension = os.path.splitext(sample_pull_path)
            dst_unzip_path = os.path.join(UNZIP_PATH, i)
            
            if not os.path.isdir(dst_unzip_path):
                os.mkdir(dst_unzip_path)
                
            if extension[1] in ZIP_EXTENSION_LIST:
                unzip_7z_file(sample_pull_path, ZIP_PASSWORD, dst_unzip_path)
                os.remove(sample_pull_path)
                print(f"[+] File({sample_pull_path}) Original File Remove Success!")
            else:
                continue


if __name__ == "__main__":
    if not os.path.isdir(UNZIP_PATH):
        os.mkdir(UNZIP_PATH)
    sample_unzip_start()
