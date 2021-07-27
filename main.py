from modules.download_daily_data import DownloadDailyTransactionData
from modules.processing_tansection_data import ProcessingTransectionData
import time


if __name__ == '__main__':
    output_path = './20210726'
    DownloadDailyTransactionData('20210727', output_path)
    DownloadDailyTransactionData('20210726', output_path)
    time.sleep(2)
    ProcessingTransectionData(output_path)


