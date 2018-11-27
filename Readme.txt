Clean up process of ML-StockAnalysisProject

DataDownloader:
  Utils:
    DataStorage Class: 
      DatabaseUploader: input database  output: dataIntoDatabase
      
  Yahoo:
    CookieCreator: input: null  output Cookie
    UrlBuilder: input: singleTicker(ClassVar) output: Url
    GetData:input: Url, Cookie, Tickers   output: DataStorageObject
  
  Google: ?
  
  Others: ?
  
