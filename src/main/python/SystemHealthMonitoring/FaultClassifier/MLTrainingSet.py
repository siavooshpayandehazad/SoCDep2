# Copyright (C) 2015 Rene Pihlak

import collections
# import numpy as np
# import itertools as itools

class MLTrainingSet():
    
    def __init__(self, buf_size, error_size, ml_names): # error_size counts 0 too, thus 001 has buf_size of 3 and error_size of 2 because 001 and 000
        self.buf_size = buf_size
        self.error_size = error_size
        self.ml_names = []
        if type(ml_names) is list:
            self.ml_names += ml_names
        else:
            for i in range(0, error_size):
                self.ml_names.append(i+1) 
    
    def getLearningSet(self):
        training = []
        training_val = []
        training_names = []
        a = 0
        b = 1
        
        tmp = collections.deque(maxlen=self.buf_size-1)
        tmpf = collections.deque(maxlen=self.buf_size-1)
        # cur_set = ""
        for i in range(0, self.error_size):
            # print "the i: "+str(i+1)
            for j in range(0, self.buf_size):
                tmp.append(a)
            for j in range(0, i):
                tmp.append(b)
            tmpf = tmp
            for k in range(0, self.buf_size):
                
                if i != 0:
                    if k > 0:
                        # tmpf[-k] = a
                        tmpf.append(a)
                else:
                    # print str(tmpf)
                    training.append(list(tmpf))
                    training_val.append(i+1)
                    training_names.append(self.ml_names[i])
                    break
                # if (k != i) or (k == 0):
                if tmpf.count(1) == i:
                    # print str(tmpf)
                    training.append(list(tmpf))
                    training_val.append(i+1)
                    training_names.append(self.ml_names[i])
        return training, training_val, training_names
