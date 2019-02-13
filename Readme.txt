This project utilizes machine learning to predict the movement of a list of stocks.

Required packages:
	MySQL
	Numpy
	
How to use (values given are the default cases):
	To train using Volume:
		python VolumeRNNTraining.py -max_processes=cpu_count() -clustering_processes=-1 -training_processes=-1 -max_training_tickers=4 -min_similarity=.6 -num_days_per_example=14 -rnn_hidden_state_size=200 -rnn_backpropagation_truncation_amount=5 -rnn_learning_rate=.1 -rnn_loss_eval=5 -rnn_num_epochs=1500 -evaluationTraining=False -data_mode="LNC"
	To train using Adjusted Close:
		python VolumeRNNTraining.py -max_processes=cpu_count() -clustering_processes=-1 -training_processes=-1 -max_training_tickers=4 -min_similarity=.6 -num_days_per_example=14 -rnn_hidden_state_size=200 -rnn_backpropagation_truncation_amount=5 -rnn_learning_rate=.1 -rnn_loss_eval=5 -rnn_num_epochs=1500 -evaluationTraining=False -data_mode="MD"

Team:
Jim Carey 
Colton Freitas 
