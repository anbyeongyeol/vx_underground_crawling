from crawling import SampleDownloader

if __name__ == "__main__":
    downloader = SampleDownloader()
    driver = downloader.driver_setting()
    downloader.start(driver)
