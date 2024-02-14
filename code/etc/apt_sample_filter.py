import os
import shutil

"""
악성코드 패밀리가 아닌 APT Malware에 대한 샘플 필터링
1. APT Malware별 개수 파악
2. 20개 미만일 경우 제외
"""

TARGET_DIC_PATH = 'Sample'
DST_DIC_PATH = 'APT_Sample'

for i in os.listdir(TARGET_DIC_PATH):
    sample_pull_path = os.path.join(TARGET_DIC_PATH, i)
    
    if len(os.listdir(sample_pull_path)) <= 20:
        continue
    else:
        src_copy_path = sample_pull_path
        dst_copy_path = os.path.join(DST_DIC_PATH, i)
        
        shutil.copytree(src_copy_path, dst_copy_path)
        print(f"[+] {src_copy_path} --> {dst_copy_path} Copy Finish !")
