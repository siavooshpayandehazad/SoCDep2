# Copyright (C) 2015 Rene Pihlak

import CounterThreshold
import MLTrainingSet as mlp

import collections

from sklearn            import svm
from sklearn.neighbors  import KNeighborsClassifier
from sklearn.tree       import DecisionTreeClassifier

class MachineLearning():
    
    def __init__(self, fault_threshold, health_threshold):#, intermittent_threshold):
        #include previous counter_threshold stuff
        #self.counter_threshold = CounterThreshold.CounterThreshold(fault_threshold, health_threshold)
        self.machine_learning_buffer        = {}
        self.machine_learning_counter       = {}
        self.machine_learning_counter_total = 0
        self.fault_counters         = {}
        self.health_counters        = {}
        self.fault_threshold        = fault_threshold
        #self.intermittent_threshold = intermittent_threshold
        self.health_threshold       = health_threshold#+intermittent_threshold
        self.dead_components    = []
        self.ml_methods         = {}
        self.training           = []
        self.training_val       = []
        self.training_names     = []
        self.training_dict      = {}
        self.ml_methods["svm"]  = svm.SVC(gamma=0.001)
        self.ml_methods["knn"]  = KNeighborsClassifier(5)
        self.ml_methods["dtc"]  = DecisionTreeClassifier(max_depth=6) 
        #TODO: Add status names such as
        #self.stat_names = ["dead", "excellent"]
        self.stat_names = 0
        if self.fault_threshold is 4:
            self.stat_names = ["good", "bad", "dying", "dead"]
        my_ml = mlp.MLTrainingSet(fault_threshold+health_threshold, fault_threshold, self.stat_names)
        self.training, self.training_val, self.training_names = my_ml.getLearningSet()
        for i in range(0, len(self.training_val)):
            self.training_dict[self.training_val[i]] = self.training_names[i]
        
        my_tr_dict = {}
        
        for i in self.training_val:
            my_tr_dict[str(i)] = 0

        for i in my_tr_dict.keys():
            my_tr_dict[i] = self.training_val.count(int(i))
            #print i

        my_tr_max = my_tr_dict.keys()[0]

        for i in my_tr_dict.keys():
            if my_tr_max is not i:
                if my_tr_dict[i] > my_tr_dict[my_tr_max]:
                    my_tr_max = i
        #print my_tr_max + ": " + str(my_tr_dict[my_tr_max])
        #print str(my_tr_dict)

        for i in my_tr_dict.keys():
            if i is my_tr_max:
                continue
            else:
                my_hit = -1
                my_count = my_tr_dict[i]
                while True:
                    k = 0
                    while k < len(self.training_val):
                        if self.training_val[k] == int(i):
                            my_hit = 1
                            my_count += 1
                            self.training_val.append(self.training_val[k])
                            self.training_names.append(self.training_names[k])
                            self.training.append(self.training[k])
                            k += 1
                        elif my_hit == 1:
                            k -= 1
                            my_count += 1
                            self.training_val.append(self.training_val[k])
                            self.training_names.append(self.training_names[k])
                            self.training.append(self.training[k])
                        else:
                            k += 1
                        if my_count == my_tr_dict[my_tr_max]:
                            my_hit = 3
                            break
                    if my_hit == 3:
                        break
        
        self.ml_methods["svm"].fit(self.training, self.training_val)
        self.ml_methods["knn"].fit(self.training, self.training_val)
        self.ml_methods["dtc"].fit(self.training, self.training_val)
        #self.memory_counter = 0
    
    def increase_health_counter(self, location, logging):
        #include previous counter_threshold stuff
        #self.counter_threshold.increase_health_counter(location, logging)
        
        this_collection = collections.deque(maxlen=self.fault_threshold+self.health_threshold-1)
        
        self.machine_learning_counter_total += 1
        
        if type(location) is dict:
            # print location, str(location.keys()[0])+str(location[location.keys()[0]])
            location = "R"+str(location.keys()[0])
        elif type(location) is tuple:
            # print location, location[0], location[1]
            location = "L"+str(location[0])+str(location[1])
        elif type(location) is int:
            # print location
            location = str(location)
        else:
            print location, type(location)
            raise ValueError("VEG: location type is wrong!")

        if location in self.dead_components:
            return None
        #if location not in self.fault_counters.keys():
        #    return None
        
        if location in self.machine_learning_counter.keys():
            self.machine_learning_counter[location] += 1
        else:
            self.machine_learning_counter[location] = 1

        if location in self.machine_learning_buffer.keys():
            self.machine_learning_buffer[location].append(0)# += 1
            logging.info("VEG: Increasing health counter at location: "+location)
            logging.info("VEG: "+location+": Buffer: "+str(self.machine_learning_buffer[location]))
            for i in range(0, len(self.machine_learning_buffer[location])-1):
                this_collection.append(list(self.machine_learning_buffer[location])[i])
            #this_collection.append(self.machine_learning_buffer[location][:-1])
            
            while True:
                if this_collection.count(1) == 0:
                    break
                elif this_collection[-1] == 0:
                    this_collection.appendleft(0)
                else:
                    this_collection.appendleft(0)
                    break
            
            #while this_collection[-1] == 0:
                #this_collection.appendleft(0)
            
            #this_collection.appendleft(0)
            
            logging.info("VEG: ML TODO: healthy part")
            logging.info("VEG: ML TODO: "+str(this_collection))
            for i in self.ml_methods.keys():
                #logging.info("VEG: ML TODO: "+str(this_collection))
                ml_value = self.ml_methods[i].predict(this_collection)
                logging.info("VEG: ML("+str(i)+") "+location+" -> "+str(ml_value))
            
            #for i in self.ml_methods.keys():
                #logging.info("VEG: ML TODO: healthy part")
                #logging.info("VEG: ML TODO: "+str(this_collection))
                #ml_value = self.ml_methods[i].predict(this_collection)
                #logging.info("VEG: ML("+str(i)+") -> "+str(ml_value))
                #ml_value = self.ml_methods[i].predict(self.machine_learning_buffer[location])
                #logging.info("VEG: ML("+i+") -> "+ml_value+" : "+self.training_dict[ml_value])
            if self.machine_learning_buffer[location].count(1) == 0:
                del self.machine_learning_buffer[location]
                logging.info("VEG: Deleted health counter at location: "+location)
                logging.info("VEG: ML("+location+") -> perfect")
        else:
            logging.info("VEG: Ignored health counter at location: "+location)
            logging.info("VEG: ML("+location+") -> perfect")
            #self.machine_learning_buffer[location] = collections.deque(maxlen=self.fault_threshold+self.health_threshold)
            #for i in range(0, self.fault_threshold+self.health_threshold):
            #    self.machine_learning_buffer[location].append(0)
        
        #logging.info("VEG: "+location+" Buffer: "+str(self.machine_learning_buffer[location]))
        #if self.health_counters[location] == self.health_threshold:
        #    logging.info("resetting component: "+location+" counters")
        #    self.reset_counters(location)

        #current_memory_usage = self.return_allocated_memory()
        #if current_memory_usage > self.memory_counter:
        #    self.memory_counter = current_memory_usage
        return None

    def increase_fault_counter(self, location, logging):
        #include previous counter_threshold stuff
        #self.counter_threshold.increase_fault_counter(location, logging)
        
        this_collection = collections.deque(maxlen=self.fault_threshold+self.health_threshold-1)
        
        self.machine_learning_counter_total += 1
        
        if type(location) is dict:
            # print location, str(location.keys()[0])+str(location[location.keys()[0]])
            location = "R"+str(location.keys()[0])
        elif type(location) is tuple:
            # print location, location[0], location[1]
            location = "L"+str(location[0])+str(location[1])
        elif type(location) is int:
            # print location
            location = str(location)
        else:
            print location, type(location)
            raise ValueError("VEG: location type is wrong!")
        if location in self.dead_components:
            return None
        
        if location in self.dead_components:
            return None
        
        if location in self.machine_learning_counter.keys():
            self.machine_learning_counter[location] += 1
        else:
            self.machine_learning_counter[location] = 1
        
        if location in self.machine_learning_buffer.keys():
            self.machine_learning_buffer[location].append(1)# += 1
            #if self.machine_learning_buffer[location].count(1) == self.fault_threshold:
                #logging.info("VEG: ML: Declaring component: "+location+" dead!")
                #self.dead_components.append(location)
                #return None
        else:
            self.machine_learning_buffer[location] = collections.deque(maxlen=self.fault_threshold+self.health_threshold)
            for i in range(0, self.fault_threshold+self.health_threshold):
                self.machine_learning_buffer[location].append(0)
            self.machine_learning_buffer[location].append(1)
        logging.info("VEG: Increasing fault counter at location: "+location)
        logging.info("VEG: "+location+": Buffer: "+str(self.machine_learning_buffer[location]))
        this_collection.append(list(self.machine_learning_buffer[location])[:-1])
        #this_collection = list(self.machine_learning_buffer[location])[:-1]
        logging.info("VEG: ML TODO: "+str(this_collection))
        for i in self.ml_methods.keys():
            ml_value = self.ml_methods[i].predict(this_collection)
            logging.info("VEG: ML("+str(i)+") "+location+" -> "+str(ml_value))#+" : "+str(self.training_dict[str(ml_value)]))
            if ml_value == self.fault_threshold:
                logging.info("VEG: ML: Declaring component: "+location+" dead!")
                if location not in self.dead_components:
                    self.dead_components.append(location)
                #return None
        
        #if self.fault_counters[location] == self.fault_threshold:
        #    logging.info("Declaring component: "+location+" dead!")
        #    self.dead_components.append(location)
        #    self.reset_counters(location)

        #current_memory_usage = self.return_allocated_memory()
        #if current_memory_usage > self.memory_counter:
        #    self.memory_counter = current_memory_usage
        return None
    
    def increase_intermittent_counter(self, location, logging):
        self.increase_fault_counter(location, logging)
        return None

    def reset_counters(self, location):
        #if location in self.fault_counters.keys():
        #    del self.fault_counters[location]
        #else:
        #    pass
        #if location in self.health_counters.keys():
        #    del self.health_counters[location]
        #else:
        #    pass
        return None

    #def return_allocated_memory(self):
    #    return len(self.health_counters) + len(self.fault_counters)

    def report(self, number_of_nodes):
        print "VEG: ==========================================="
        print "VEG:         MACHINE LEARNING REPORT"
        print "VEG: ==========================================="
        print "VEG: TODO"
        print "VEG: Total number of healthy/faulty events: " +str(self.machine_learning_counter_total)
        for i in self.machine_learning_counter.keys():
            print "VEG: " +i+ ": " + str(self.machine_learning_counter[i])
        print "DEAD Components:", self.dead_components
        #print "MAX MEMORY USAGE:", self.memory_counter
        #print "AVERAGE COUNTER PER Node: ", float(self.memory_counter)/number_of_nodes
        return None
