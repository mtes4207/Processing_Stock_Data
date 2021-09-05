# Processing Stock Data

## Example
# 
1. Setup two continuous transection days and run command to download data.
```
    output_path = './example'
    DownloadDailyTransactionData('20210902', output_path)
    DownloadDailyTransactionData('20210903', output_path)
```
2. Run below command to processing transection data.
```
    ProcessingTransectionData(output_path)
```

3. Get output excel file

![This is a alt text.](https://github.com/mtes4207/Processing_Stock_Data/master/picture/Credit.jpg "投信買賣資料")

![This is a alt text.](https://github.com/mtes4207/Processing_Stock_Data/master/picture/FNBS.jpg "外資買賣資料")
