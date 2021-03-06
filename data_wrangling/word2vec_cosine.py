import numpy as np
import nltk
import string
from nltk.corpus import stopwords
import gensim
import os
from sklearn.metrics.pairwise import cosine_similarity
import operator

stops = set(stopwords.words("english"))
punct = set(string.punctuation)

class Word2vecExtractor:

    def __init__(self, w2vecmodel):
        self.w2vecmodel=gensim.models.Word2Vec.load_word2vec_format(w2vecmodel,binary=True)
        self.emotions_dict = {"anger":self.word2v("anger"), "disgust":self.word2v("disgust"), "fear":self.word2v("fear"), "guilt":self.word2v("guilt"), "joy":self.word2v("joy"), "sadness":self.word2v("sadness")}
    
    def sent2vec(self,sentence):    
        words = [word for word in nltk.word_tokenize(sentence) if word not in stops and word not in punct]
        res = np.zeros(self.w2vecmodel.vector_size)
        count = 0
        for word in words:
            if word in self.w2vecmodel:
                count += 1
                res += self.w2vecmodel[word]

        if count != 0:
            res /= count

        return res 

    def word2v(self, word):
        res = np.zeros(self.w2vecmodel.vector_size)
        if word in self.w2vecmodel:
                res += self.w2vecmodel[word]
        return res

    
    '''def features_todict(self,concatvector):    
        number_w2vec=concatvector.size   
          
        columnnames=["Word2VecfeatureGoogle_"+ str(i) for i in range(0, number_w2vec)]  
        feature_dict=dict(zip(columnnames,concatvector)) 
        return feature_dict
    '''
    
    '''def extract(self,sentence1):
        v1=self.sen2vec(sentence1)
        #v2=self.sen2vec(sentence2)
        #concatvector=np.concatenate([v1, v2])
        w2vec_dict=self.features_todict(v1)
        return w2vec_dict
     '''           


if __name__ == '__main__':

    W2loc = os.path.join("resources","GoogleNews-vectors-negative300.bin")
    #W2loc = "/home/geet/dialogue_systems/data/GoogleNews-vectors-negative300.bin"
    W2vecextractor=Word2vecExtractor(W2loc)     
    sentence = "Will the lack of females choosing STEM related careers create a new gender disparity for Gen-Z or is this set to change?"
    vec_rep=W2vecextractor.sent2vec(sentence)
    scores_dict = {}


    for item in W2vecextractor.emotions_dict.keys():
    	scores_dict.update({item:cosine_similarity(vec_rep, W2vecextractor.emotions_dict[item])})

    sorted_dict = sorted(scores_dict.items(), key=operator.itemgetter(1))
    print(sorted_dict[0][0])




 
