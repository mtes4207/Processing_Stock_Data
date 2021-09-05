from modules.download_daily_data import DownloadDailyTransactionData
from modules.processing_tansection_data import ProcessingTransectionData
import time


if __name__ == '__main__':
    output_path = './example'
    DownloadDailyTransactionData('20210902', output_path)
    DownloadDailyTransactionData('20210903', output_path)
    time.sleep(2)
    ProcessingTransectionData(output_path)


