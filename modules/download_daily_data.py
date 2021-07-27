from datetime import datetime, timedelta
import requests
import time
import os


TWSE_CREDIT_URL = 'https://www.twse.com.tw/fund/TWT44U?response=csv&date='
TWSE_FNBS_URL = 'https://www.twse.com.tw/fund/TWT38U?response=csv&date='
HEADERS = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"}

class DownloadDailyTransactionData:

    def __init__(self, transaction_date, output_path):

        self._transaction_date = transaction_date
        output_path = os.path.abspath(output_path)
        self.origin_data_path = os.path.join(output_path, 'Origin data')
        if not os.path.exists(self.origin_data_path):
            os.makedirs(self.origin_data_path)

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
            print("Save TWSE_Credit_%s.csv  in %s"%(self._transaction_date, self.origin_data_path))
            with open(os.path.join(self.origin_data_path, "TWSE_Credit_%s.csv"%self._transaction_date), "w") as f:  # 開啟資料夾及命名圖片檔
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
            print("Save TWSE_FNBS_%s.csv  in %s"%(self._transaction_date, self.origin_data_path))
            with open(os.path.join(self.origin_data_path, "TWSE_FNBS_%s.csv"%self._transaction_date), "w") as f:  # 開啟資料夾及命名圖片檔
                f.write(response.text)
        else:
            print('%s maybe no transction data'%self._transaction_date)
        response.close()

if __name__ == '__main__':
    transaction_date = '20210719'
    folder_path = './origin_data_path'
    c = DownloadDailyTransactionData(transaction_date, folder_path)
    c.run()

