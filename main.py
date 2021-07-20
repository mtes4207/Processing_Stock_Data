from modules.download_daily_data import DownloadDailyTransactionData
from modules.processing_tansection_data import ProcessingTransectionData
import time


if __name__ == '__main__':
    folder_path = './save_folder'
    output_path = './'
    DownloadDailyTransactionData('20210719', folder_path)
    DownloadDailyTransactionData('20210720', folder_path)
    time.sleep(2)
    ProcessingTransectionData(folder_path, output_path)

