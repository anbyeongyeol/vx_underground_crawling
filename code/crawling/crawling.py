from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import shutil
import time
import os
import re



class SampleDownloader:
    def __init__(self):
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
        self.chrome_driver_path = 'Chrome Driver Path'
        self.download_path = 'Download Path'
        self.target_url = 'https://vx-underground.org/'
        self.target_category = 'Samples/Families'
        self.url_path = f"{self.target_url}{self.target_category}"
        # Path Validation
        if not os.path.isdir(self.download_path):
            print(f"[+] {self.download_path} Directory Generation")
            os.mkdir(self.download_path)
        else:
            print(f"[+] {self.download_path} Directory already exists!")

    def driver_setting(self):    
        # Option Setting
        options = Options()
        
        # Detail Option
        options.add_argument('user-agent=' + self.user_agent)
        # Avoid unnecessary errors
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_experimental_option('prefs', {
            "download.default_directory" : self.download_path,
            "download.prompt_for_download" : False,
            "download.directory_upgrade" : True
            # "safebrowsing.enabled" : True
        })    
        
        # Driver Load
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(10)
        
        # Chrome View Maximize
        driver.maximize_window()
        
        return driver
    
    # 저장되는 파일을 패밀리별 디렉토리로 옮기기
    def move_download_file(self, source_dir, target_dir):
        for file_list in os.listdir(source_dir):
            source_file = os.path.join(source_dir, file_list)
            
            if os.path.isfile(source_file):
                target_file = os.path.join(target_dir, file_list)
                
                shutil.move(source_file, target_file)
    
    def clear_sample_dic(self, target_dic):
        for file_list in os.listdir(target_dic):
            file_path = os.path.join(target_dic, file_list)
            
            if os.path.isfile(file_path):
                os.remove(file_path)
    
    def start(self, driver):
        # URL Setting
        url = self.url_path
        
        driver.get(url)
        time.sleep(5)
        
        # Folder and File Count
        folder_file_info = driver.find_element(By.CSS_SELECTOR, 'div.text-center p.text-gray-600.text-xs')
        folder_file_info_text = folder_file_info.text
        # 숫자 1번 이상에 대한 그룹화 정규식
        matches = re.findall(r'(\d+) folders, (\d+) files', folder_file_info_text)

        if matches: 
            folder_count, files_count = matches[0]
            folder_count, files_count = int(folder_count), int(files_count)
            print(f"[+] Crawling Start! Malware Family : {folder_count}")
        
        # Malware Family per Crawling Start
        for i in range (364, folder_count+1):
            # Initialization
            try:
                driver.get(url)
                time.sleep(3)

                # Malware Family Name Parsing
                malware_family = (driver.find_element(By.CSS_SELECTOR, f'#file-display > div:nth-child({i}) > p').text)
                
                #Android Filttering
                if "Android" in malware_family:
                    continue
                else:
                    print(f"[+] {i} : {malware_family} Enter!")
                    driver.find_element(By.XPATH, f'//*[@id="file-display"]/div[{i}]').click()
                    time.sleep(3)

                    # Malware Family Dicrectory Generation
                    if not os.path.isdir(f"{self.download_path}\\{malware_family}"):
                        os.mkdir(f"{self.download_path}\\{malware_family}")
                        print(f"[+] {malware_family} Directory Generation")
                    else:
                        print(f"[+] {malware_family} Directory already exists")
                        
                        
                    # 패밀리별 파일 개수 
                    family_folder_file_info = driver.find_element(By.CSS_SELECTOR, 'div.text-center p.text-gray-600.text-xs')
                    family_folder_file_info_text = family_folder_file_info.text
                    
                    # 패밀리별 파일 파싱
                    matches = re.findall(r'(\d+) folders, (\d+) files', family_folder_file_info_text)
                    if matches: 
                        family_folder_count, family_files_count = matches[0]
                        family_folder_count, family_files_count = int(family_folder_count), int(family_files_count)
                        
                        # Sample 폴더가 존재할 경우
                        if family_folder_count != 0:
                            driver.find_element(By.XPATH, '//*[@id="file-display"]/div[2]').click()
                            time.sleep(3)
            
                            # Sample 파일 내 샘플 개수 파악
                            file_count_in_sample = driver.find_element(By.CSS_SELECTOR, 'div.text-center p.text-gray-600.text-xs')
                            file_count_in_sample_text = file_count_in_sample.text
                            matches = re.findall(r'(\d+) folders, (\d+) files', file_count_in_sample_text)
                            
                            if matches: 
                                _, sample_file_count = matches[0]
                                sample_file_count = int(sample_file_count)
                                
                                print(f"[+] {malware_family} Sample Count : {sample_file_count}")
                                for k in range(1, sample_file_count+1):
                                    driver.find_element(By.XPATH, f'//*[@id="file-display"]/div[{k}]/div/a').click()
                                    time.sleep(2)

                        else:
                            # 패밀리별 샘플에 대해 다운로드 실행
                            print(f"[+] {malware_family} Sample Count : {family_files_count}")
                            for k in range(1, family_files_count+1):
                                driver.find_element(By.XPATH, f'//*[@id="file-display"]/div[{k}]/div/a').click()
                                time.sleep(5)
                        
                    # 패밀리별 디렉토리로 파일 옮기기
                    time.sleep(5)
                    self.move_download_file(self.download_path, f"{self.download_path}\\{malware_family}")
                    print(f"[+] {malware_family} : File Move Finish")
            except Exception as e:
                with open('exception.txt', 'a') as file:
                    file.write(f"{malware_family}\n")
                self.clear_sample_dic(self.download_path)
                print(f"[!] Error processing {malware_family}, logged to exception.txt")
        
