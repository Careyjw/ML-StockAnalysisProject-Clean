This project utilizes machine learning to predict the movement of a list of stocks.

Required packages:
	MySQL python Connector
	Numpy
	
How to use:
	First use StockDataDownloadMain.py which downloads the information needed to train the models
		python StockDataDownloadMain.py -dp={dp}
		-dp = Password for database access, can be passed in or typed at prompt that will appear
	Next use ModelTraining.py which trains an RNN using volumetric data to predict price movement
		python ModelTraining.py -modelID={id} -p={p}
		-modelID = the ID of the model you wish to train
		-p = password for database access, can be passed in or typed at prompt that will appear	
	Finally use EPMain.py to either evaluate the model or predict the price movement
		python EPMain.py -e={evaluate mode} -dp={dp} -ep={ep}
		-e is a boolean value (True or False) 
			if true the program will evaluate its accuracy 
			if false the program will predict the next day
		-dp= password for database access, can be passed in or typed at prompt that will appear
		-ep= password for email system, can be passed in or typed at prompt that will appear
	
Team:
Jim Carey 
Colton Freitas 