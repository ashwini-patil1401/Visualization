import pandas
import preprocess
import topicmodel
import sys

def getTopics(data, modelName, numTopics, numWords, filename):
	'''
	:param data: the data, 
	:param modelName: the topic modeling algorithm LDA
	:param numTopics: number of topics, 
	:param numWords: number of words to be returned for each topic
	:param filename: name of file containing data
	:return: returns numWords number of words for numTopics number of topics
	'''
	return topicmodel.runLDA(data, numTopics, numWords, filename)

def getEmotionPercentage(df, filename):
	'''
	:param df: DataFrame containing preprocessed data 
	:param filename: name of file containing data
	:return: Does not return anything. Saves percentage wise distribution of emotions (joy, sadness, anger, fear, disgust, guilt) for tweets in a file with filename-emotions.csv
	'''
	result = df["emotion"].value_counts(sort=True, ascending=False, dropna=True)
	result = (result/sum(result))*100.0
	result.columns = ["Emotion", "Percentage"]
	
	with open(filename.split(".")[0] + "-emotions.csv", 'w') as nfh:
		result.to_csv(nfh)
	print("Emotion analysis stored in: "+filename.split(".")[0]+"-emotions.csv")
	

if __name__ == "__main__":

	filename = "data/conservative_new.csv"
	#filename = "data/gap.csv"
	#filename = "data/impact.csv"
	#filename = "data/leader.csv"
	#filename = "data/marriage.csv"
	#filename = "data/maternity.csv"
	#filename = "data/politicians.csv"
	#filename = "data/talkpay.csv"
	#filename = "data/merged.csv"
	df = preprocess.create_preprocessed_file(filename)

	getEmotionPercentage(df, filename)

	modelName = "LDA"
	numTopics = 3
	numWords = 10

	numTopics = raw_input("Choose number of topics K:")
	numWords = raw_input("Choose number of top words to display for each topic:")
	
	getTopics(df, modelName, int(numTopics), int(numWords), filename)
	
	
	
