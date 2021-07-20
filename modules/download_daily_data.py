from datetime import datetime, timedelta
import requests
import time
import os


TWSE_CREDIT_URL = 'https://www.twse.com.tw/fund/TWT44U?response=csv&date='
TWSE_FNBS_URL = 'https://www.twse.com.tw/fund/TWT38U?response=csv&date='
HEADERS = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"}

class DownloadDailyTransactionData:

    def __init__(self, transaction_date, save_folder):

        self._transaction_date = transaction_date
        self.save_folder = os.path.abspath(save_folder)

        if not os.path.exists(self.save_folder):
            os.mkdir(self.save_folder)

        self.download_credit_data()
        self.download_fnbs_data()

    def download_credit_data(self):
        print("-------------------------------------------")
        for i in range(5, -1, -1):
            time.sleep(1)
            print('waiting %s s'%i, end='\r',  flush=True)
        download_path = TWSE_CREDIT_URL + self._transaction_date
        print(download_path)

        try:
            response = requests.get(download_path, headers=HEADERS)
        except (requests.ConnectionError, requests.Timeout) as exception:
            print(exception)
            raise Exception(exception)

        if len(response.content) >10:
            print("Save TWSE_Credit_%s.csv  in %s"%(self._transaction_date, self.save_folder))
            with open(os.path.join(self.save_folder, "TWSE_Credit_%s.csv"%self._transaction_date), "w") as f:  # 開啟資料夾及命名圖片檔
                f.write(response.text)
        response.close()

    def download_fnbs_data(self):
        print("-------------------------------------------")
        for i in range(5, -1, -1):
            time.sleep(1)
            print('waiting %s s'%i, end='\r',  flush=True)
        download_path = TWSE_FNBS_URL + self._transaction_date
        print(download_path)

        try:
            response = requests.get(download_path, headers=HEADERS)
        except (requests.ConnectionError, requests.Timeout) as exception:
            print(exception)
            raise Exception(exception)

        if len(response.content) >10:
            print("Save TWSE_FNBS_%s.csv  in %s"%(self._transaction_date, self.save_folder))
            with open(os.path.join(self.save_folder, "TWSE_FNBS_%s.csv"%self._transaction_date), "w") as f:  # 開啟資料夾及命名圖片檔
                f.write(response.text)
        else:
            print('%s maybe no transction data'%self._transaction_date)
        response.close()

if __name__ == '__main__':
    transaction_date = '20210719'
    folder_path = './save_folder'
    c = DownloadDailyTransactionData(transaction_date, folder_path)
    c.run()

