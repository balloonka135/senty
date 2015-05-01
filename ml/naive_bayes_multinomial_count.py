# encoding: UTF-8

import machine_learning

from sklearn.cross_validation import LeaveOneLabelOut
from sklearn.naive_bayes import MultinomialNB

class NaiveBayesMultinomial(machine_learning.MachineLearning):        
    def __init__(self, training_data_path):
        machine_learning.MachineLearning.__init__(self, training_data_path)
        import os
        self.input_files = filter(lambda x: not x.endswith('~'), os.listdir(self.training_data_path))

    '''
    def fit(self):
        self.gnb.fit(self.data_for_fit[0], self.data_for_fit[1])               
    '''
    def predict(self, block_size_in_ratio):
        self.data_for_fit = machine_learning.MachineLearning.fit_data_count(self)
        
        N = len(self.data_for_fit[0])
        n = block_size_in_ratio * float(len(self.data_for_fit[0]))
        n = int(n)
        
        result = []
        totalTrue = 0
        cur_first_index = 0
        while cur_first_index < N:
            print cur_first_index
            alone = []
            alone_target = []
            num = 0
            while num < n and num + cur_first_index < N:    
                alone.append(self.data_for_fit[0][0])
                alone_target.append(self.data_for_fit[1][0])
                self.data_for_fit[0].remove(self.data_for_fit[0][0])
                self.data_for_fit[1].remove(self.data_for_fit[1][0])
                num += 1
            
            self.gnb = MultinomialNB()
            self.gnb.fit(self.data_for_fit[0], self.data_for_fit[1])
            
            alone_size = len(alone)
            for iter_num in range(0, alone_size):
                gnb_result = self.gnb.predict(alone[iter_num])
                if alone_target[iter_num] == gnb_result:
                    totalTrue += 1
                result.append((self.input_files[cur_first_index + iter_num], gnb_result[0], alone_target[iter_num]))  
            
            
            for iter_num in range(0, alone_size):               
                self.data_for_fit[0].append(alone[iter_num])
                self.data_for_fit[1].append(alone_target[iter_num])
            
            cur_first_index += n
        
        print 'Multinomial NB with count: ' + str(100. * float(totalTrue) / N) + ' %'
        return result    
        
#DEBUG = True
DEBUG = False

if DEBUG:
    nbm = NaiveBayesMultinomial("../data/extractor_data/")        
    nbm.predict(0.05)
