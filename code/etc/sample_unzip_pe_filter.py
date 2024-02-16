import os
import py7zr
import shutil
"""
악성코드 샘플 압축 해제 및 PE 파일 필터링
1. 악성코드 샘플 압축 해제(2중일 경우 반복하여 진행)
2. PE 파일이 아닐 경우 필터링 진행
2. 20개 
"""

SAMPLE_PATH = 'APT_Sample'
UNZIP_PATH = f"{SAMPLE_PATH}_unzip"
ZIP_EXTENSION_LIST = ['.zip', '.7z', '.tar', '.rar']
PE_APT_DIC_PATH = 'APT_unzip_pe'
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

def pe_check():
    # PE 필터링 디렉토리 생성
    if not os.path.isdir(PE_APT_DIC_PATH):
        os.mkdir(PE_APT_DIC_PATH)
    
    # 압축해제한 그룹별 접근
    apt_group_unzip_list = os.listdir(UNZIP_PATH)
    for i in apt_group_unzip_list:
        pe_filter_target_path = os.path.join(PE_APT_DIC_PATH, i)
        # PE 필터링 파일 저장할 Dicrectory 생성
        if not os.path.isdir(pe_filter_target_path):
            os.mkdir(pe_filter_target_path)
        
        temp_apt_group_unzip_list = os.path.join(UNZIP_PATH, i)
         
        # 그룹별 샘플에 접근
        for k in os.listdir(temp_apt_group_unzip_list):
            unzip_sample_full_path = os.path.join(temp_apt_group_unzip_list, k)
            pe_filter_file = os.path.join(pe_filter_target_path, k)
            # 파일 시그니처 반단(PE)
            with open(unzip_sample_full_path, 'rb') as f:
                magic = f.read(2)
                if magic == b'MZ':
                    shutil.copy(unzip_sample_full_path, pe_filter_file)
                    print(f"[+] {unzip_sample_full_path} --> {pe_filter_file} Copy Finish !!")
                    
                    

if __name__ == "__main__":
    # sample_unzip_start()
    pe_check()
