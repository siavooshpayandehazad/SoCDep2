# Copyright (C) 2015 Rene Pihlak

import CounterThreshold
import MLTrainingSet as mlp
from ConfigAndPackages import Config
import collections
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier


class MachineLearning():
    
    def __init__(self, fault_threshold, health_threshold, intermittent_threshold):
        # include previous counter_threshold stuff
        self.counter_threshold = CounterThreshold.CounterThreshold(fault_threshold, health_threshold,
                                                                   intermittent_threshold)
        self.machine_learning_buffer = {}
        self.machine_learning_buffer_inter = {}
        
        self.fault_counters = {}
        self.health_counters = {}
        
        self.memory_max = {}
        
        self.fault_threshold = fault_threshold
        self.intermittent_threshold = intermittent_threshold
        self.health_threshold = health_threshold    # +intermittent_threshold
        
        self.dead_components = []
        self.intermittent_components = []
        
        self.ml_methods = {}
        self.training = []
        self.training_val = []
        self.training_names = []
        self.training_dict = {}
        
        self.ml_methods_inter = {}
        self.training_inter = []
        self.training_val_inter = []
        self.training_names_inter = []
        self.training_dict_inter = {}
        
        self.ml_methods["svm"] = svm.SVC(gamma=0.001)
        self.ml_methods["knn"] = KNeighborsClassifier(fault_threshold+1)
        self.ml_methods["dtc"] = DecisionTreeClassifier(max_depth=fault_threshold+2)
        
        self.ml_methods_inter["svm"] = svm.SVC(gamma=0.001)
        self.ml_methods_inter["knn"] = KNeighborsClassifier(intermittent_threshold+1)
        self.ml_methods_inter["dtc"] = DecisionTreeClassifier(max_depth=intermittent_threshold+2)
        
        self.stat_names = 0
        self.stat_names_inter = 0
        
        # TODO: Add status names such as
        # self.stat_names = ["dead", "excellent"]
        
        # Normal faults
        if self.fault_threshold is 4:
            self.stat_names = ["good", "bad", "dying", "dead"]
        my_ml = mlp.MLTrainingSet(self.health_threshold+self.fault_threshold, self.fault_threshold, self.stat_names)
        self.training, self.training_val, self.training_names = my_ml.getLearningSet()
        for i in range(0, len(self.training_val)):
            self.training_dict[self.training_val[i]] = self.training_names[i]
        
        my_tr_dict = {}
        
        for i in self.training_val:
            my_tr_dict[str(i)] = 0

        for i in my_tr_dict.keys():
            my_tr_dict[i] = self.training_val.count(int(i))

        my_tr_max = my_tr_dict.keys()[0]

        for i in my_tr_dict.keys():
            if my_tr_max is not i:
                if my_tr_dict[i] > my_tr_dict[my_tr_max]:
                    my_tr_max = i

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
        
        # Intermittent faults
        if self.intermittent_threshold is 4:
            self.stat_names_inter = ["good", "bad", "becoming intermittent", "intermittent"]
        my_ml_inter = mlp.MLTrainingSet(self.health_threshold+self.intermittent_threshold, self.intermittent_threshold,
                                        self.stat_names_inter)
        self.training_inter, self.training_val_inter, self.training_names_inter = my_ml_inter.getLearningSet()
        for i in range(0, len(self.training_val_inter)):
            self.training_dict_inter[self.training_val_inter[i]] = self.training_names_inter[i]
        
        my_tr_dict_inter = {}
        
        for i in self.training_val_inter:
            my_tr_dict_inter[str(i)] = 0

        for i in my_tr_dict_inter.keys():
            my_tr_dict_inter[i] = self.training_val_inter.count(int(i))

        my_tr_max_inter = my_tr_dict_inter.keys()[0]

        for i in my_tr_dict_inter.keys():
            if my_tr_max_inter is not i:
                if my_tr_dict_inter[i] > my_tr_dict_inter[my_tr_max_inter]:
                    my_tr_max_inter = i

        for i in my_tr_dict_inter.keys():
            if i is my_tr_max_inter:
                continue
            else:
                my_hit_inter = -1
                my_count_inter = my_tr_dict_inter[i]
                while True:
                    k = 0
                    while k < len(self.training_val_inter):
                        if self.training_val_inter[k] == int(i):
                            my_hit_inter = 1
                            my_count_inter += 1
                            self.training_val_inter.append(self.training_val_inter[k])
                            self.training_names_inter.append(self.training_names_inter[k])
                            self.training_inter.append(self.training_inter[k])
                            k += 1
                        elif my_hit_inter == 1:
                            k -= 1
                            my_count_inter += 1
                            self.training_val_inter.append(self.training_val_inter[k])
                            self.training_names_inter.append(self.training_names_inter[k])
                            self.training_inter.append(self.training_inter[k])
                        else:
                            k += 1
                        if my_count_inter == my_tr_dict_inter[my_tr_max_inter]:
                            my_hit_inter = 3
                            break
                    if my_hit_inter == 3:
                        break
        
        self.ml_methods["svm"].fit(self.training, self.training_val)
        self.ml_methods["knn"].fit(self.training, self.training_val)
        self.ml_methods["dtc"].fit(self.training, self.training_val)
        
        self.ml_methods_inter["svm"].fit(self.training_inter, self.training_val_inter)
        self.ml_methods_inter["knn"].fit(self.training_inter, self.training_val_inter)
        self.ml_methods_inter["dtc"].fit(self.training_inter, self.training_val_inter)
        # self.memory_counter = 0
    
    def increase_health_counter(self, location, logging):
        # include previous counter_threshold stuff
        self.counter_threshold.increase_health_counter(location, logging)
        
        this_collection = collections.deque(maxlen=self.fault_threshold+self.health_threshold-1)
        this_collection_inter = collections.deque(maxlen=self.intermittent_threshold+self.health_threshold-1)
        
        this_bufs = {}
        this_global_bufs = {}
        this_bufs['faults'] = this_collection
        this_bufs['intermittent'] = this_collection_inter
        this_global_bufs['faults'] = self.machine_learning_buffer
        this_global_bufs['intermittent'] = self.machine_learning_buffer_inter
        
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
        # if location not in self.fault_counters.keys():
        #    return None
        for cur_buf in this_bufs.keys():
            if location in this_global_bufs[cur_buf].keys():
                this_global_bufs[cur_buf][location].append(0)
                logging.info("VEG: Increasing health in " + cur_buf + "counter at location: "+location)
                logging.info("VEG: "+location+": Buffer: "+str(this_global_bufs[cur_buf][location]))
                for i in range(0, len(this_global_bufs[cur_buf][location])-1):
                    this_bufs[cur_buf].append(list(this_global_bufs[cur_buf][location])[i])
                while True:
                    if this_bufs[cur_buf].count(1) == 0:
                        break
                    elif this_bufs[cur_buf][-1] == 0:
                        this_bufs[cur_buf].appendleft(0)
                    else:
                        this_bufs[cur_buf].appendleft(0)
                        break
#                 logging.info("VEG: ML TODO: " + cur_buf + " buffer: "+str(this_bufs[cur_buf]))
                if this_global_bufs[cur_buf][location].count(1) == 0:
                    del this_global_bufs[cur_buf][location]
                    logging.info("VEG: Deleted health counter at location: "+location)
                    logging.info("VEG: " + cur_buf + " buffer: ML("+location+") -> perfect")
                else:
                    for i in self.ml_methods.keys():
                        ml_value = self.ml_methods[i].predict(this_bufs[cur_buf])
                        logging.info("VEG: fault buffer: ML("+str(i)+") "+location+" -> "+str(ml_value))
            else:
                logging.info("VEG: Ignored " + cur_buf + " health counter at location: "+location)
                logging.info("VEG: ML("+location+") -> perfect")
                    
#         if location in self.machine_learning_buffer.keys():
#             logging.info("VEG: ML TODO: healthy part")
#             self.machine_learning_buffer[location].append(0)# += 1
#             logging.info("VEG: Increasing health in fault counter at location: "+location)
#             logging.info("VEG: "+location+": Buffer: "+str(self.machine_learning_buffer[location]))
#             for i in range(0, len(self.machine_learning_buffer[location])-1):
#                 this_collection.append(list(self.machine_learning_buffer[location])[i])
#             #this_collection.append(self.machine_learning_buffer[location][:-1])
#             while True:
#                 if this_collection.count(1) == 0:
#                     break
#                 elif this_collection[-1] == 0:
#                     this_collection.appendleft(0)
#                 else:
#                     this_collection.appendleft(0)
#                     break
#             logging.info("VEG: ML TODO: fault buffer: "+str(this_collection))
#             
#             if self.machine_learning_buffer[location].count(1) == 0:
#                 del self.machine_learning_buffer[location]
#                 logging.info("VEG: Deleted health counter at location: "+location)
#                 logging.info("VEG: fault buffer: ML("+location+") -> perfect")
#             else:
#                 for i in self.ml_methods.keys():
#                     ml_value = self.ml_methods[i].predict(this_collection)
#                     logging.info("VEG: fault buffer: ML("+str(i)+") "+location+" -> "+str(ml_value))
#         else:
#             logging.info("VEG: Ignored fault health counter at location: "+location)
#             logging.info("VEG: ML("+location+") -> perfect")
#             
#         if location in self.machine_learning_buffer_inter.keys():
#             logging.info("VEG: ML TODO: healthy part")
#             self.machine_learning_buffer_inter[location].append(0)# += 1
#             logging.info("VEG: Increasing health in intermittent counter at location: "+location)
#             logging.info("VEG: "+location+": Buffer: "+str(self.machine_learning_buffer_inter[location]))
#             for i in range(0, len(self.machine_learning_buffer_inter[location])-1):
#                 this_collection_inter.append(list(self.machine_learning_buffer_inter[location])[i])
#             while True:
#                 if this_collection_inter.count(1) == 0:
#                     break
#                 elif this_collection_inter[-1] == 0:
#                     this_collection_inter.appendleft(0)
#                 else:
#                     this_collection_inter.appendleft(0)
#                     break
#             logging.info("VEG: ML TODO: intermittent buffer: "+str(this_collection_inter))
#             if self.machine_learning_buffer_inter[location].count(1) == 0:
#                 del self.machine_learning_buffer_inter[location]
#                 logging.info("VEG: Deleted health counter at location: "+location)
#                 logging.info("VEG: intermittent buffer: ML("+location+") -> perfect")
#             else:
#                 for i in self.ml_methods_inter.keys():
#                     ml_value = self.ml_methods_inter[i].predict(this_collection_inter)
#                     logging.info("VEG: intermittent buffer: ML("+str(i)+") "+location+" -> "+str(ml_value))
#         else:
#             logging.info("VEG: Ignored intermittent health counter at location: "+location)
#             logging.info("VEG: ML("+location+") -> perfect")
        return None

    def increase_fault_counter(self, location, logging):
        # include previous counter_threshold stuff
        self.counter_threshold.increase_fault_counter(location, logging)
        
        this_collection = collections.deque(maxlen=self.fault_threshold+self.health_threshold-1)
        
        if type(location) is dict:
            # location is a router: {node_1: [turn]}
            # print location, str(location.keys()[0])+str(location[location.keys()[0]])
            if Config.enable_router_counters:
                location = "R"+str(location.keys()[0])
            else:
                return None
        elif type(location) is tuple:
            # location is a link: (node1, node 2)
            # print location, location[0], location[1]
            if Config.enable_link_counters:
                location = "L"+str(location[0])+str(location[1])
            else:
                return None
        elif type(location) is int:
            # location is a node
            # print location
            if Config.enable_pe_counters:
                location = str(location)
            else:
                return None
        else:
            print location, type(location)
            raise ValueError("location type is wrong!")
        if location in self.dead_components:
            return None
        
        if location in self.dead_components:
            return None
        
        if location in self.machine_learning_buffer.keys():
            self.machine_learning_buffer[location].append(1)    # += 1
            # if self.machine_learning_buffer[location].count(1) == self.fault_threshold:
            #     logging.info("VEG: ML: Declaring component: "+location+" dead!")
            #     self.dead_components.append(location)
            #     return None
        else:
            self.machine_learning_buffer[location] = collections.deque(maxlen=self.fault_threshold+self.health_threshold)
            for i in range(0, self.fault_threshold+self.health_threshold):
                self.machine_learning_buffer[location].append(0)
            self.machine_learning_buffer[location].append(1)
        logging.info("VEG: Increasing fault counter at location: "+location)
        logging.info("VEG: "+location+": Buffer: "+str(self.machine_learning_buffer[location]))
        for i in range(0, len(self.machine_learning_buffer[location])-1):
                this_collection.append(list(self.machine_learning_buffer[location])[i])
        # this_collection.append(list(self.machine_learning_buffer[location])[:-1])
        # this_collection = list(self.machine_learning_buffer[location])[:-1]
#         logging.info("VEG: ML TODO: "+str(this_collection))
        # #######
        for i in self.ml_methods.keys():
            ml_value = self.ml_methods[i].predict(this_collection)
            logging.info("VEG: ML("+str(i)+") "+location+" -> "+str(ml_value))  # +" : "+str(self.training_dict[str(ml_value)]))
            if ml_value == self.fault_threshold:
                logging.info("VEG: ML: Declaring component: "+location+" dead!")
                if location not in self.dead_components:
                    self.dead_components.append(location)
                    del self.machine_learning_buffer[location]
        # #####
        
        # if self.fault_counters[location] == self.fault_threshold:
        #    logging.info("Declaring component: "+location+" dead!")
        #    self.dead_components.append(location)
        #    self.reset_counters(location)

        # current_memory_usage = self.return_allocated_memory()
        # if current_memory_usage > self.memory_counter:
        #    self.memory_counter = current_memory_usage
        
        self.check_max_memory('fault')
        
        return None
    
    def increase_intermittent_counter(self, location, logging):
        # include previous counter_threshold stuff
        self.counter_threshold.increase_intermittent_counter(location, logging)
        
        this_collection = collections.deque(maxlen=self.intermittent_threshold+self.health_threshold-1)
        
        if type(location) is dict:
            # location is a router: {node_1: [turn]}
            # print location, str(location.keys()[0])+str(location[location.keys()[0]])
            if Config.enable_router_counters:
                location = "R"+str(location.keys()[0])
            else:
                return None
        elif type(location) is tuple:
            # location is a link: (node1, node 2)
            # print location, location[0], location[1]
            if Config.enable_link_counters:
                location = "L"+str(location[0])+str(location[1])
            else:
                return None
        elif type(location) is int:
            # location is a node
            # print location
            if Config.enable_pe_counters:
                location = str(location)
            else:
                return None
        else:
            print location, type(location)
            raise ValueError("location type is wrong!")
        
        if location in self.intermittent_components:
            return None
        
        if location in self.intermittent_components:
            return None
        
        if location in self.machine_learning_buffer_inter.keys():
            self.machine_learning_buffer_inter[location].append(1)  # += 1
            # if self.machine_learning_buffer[location].count(1) == self.fault_threshold:
            #     logging.info("VEG: ML: Declaring component: "+location+" dead!")
            #     self.dead_components.append(location)
            #     return None
        else:
            self.machine_learning_buffer_inter[location] = collections.deque(maxlen=self.intermittent_threshold+self.health_threshold)
            for i in range(0, self.intermittent_threshold+self.health_threshold):
                self.machine_learning_buffer_inter[location].append(0)
            self.machine_learning_buffer_inter[location].append(1)
        logging.info("VEG: Increasing intermittent fault counter at location: "+location)
        logging.info("VEG: "+location+": Buffer: "+str(self.machine_learning_buffer_inter[location]))
        # print self.intermittent_threshold+self.health_threshold-1
        # print len(self.machine_learning_buffer_inter[location])-1
        for i in range(0, len(self.machine_learning_buffer_inter[location])-1):
                this_collection.append(list(self.machine_learning_buffer_inter[location])[i])
        # this_collection.append(list(self.machine_learning_buffer_inter[location])[:-1])
        # this_collection = list(self.machine_learning_buffer[location])[:-1]
#         logging.info("VEG: ML TODO: "+str(this_collection))
        for i in self.ml_methods_inter.keys():
            ml_value = self.ml_methods_inter[i].predict(this_collection)
            logging.info("VEG: ML("+str(i)+") "+location+" -> "+str(ml_value))  # +" : "+str(self.training_dict[str(ml_value)]))
            if ml_value == self.intermittent_threshold:
                logging.info("VEG: ML: Declaring component: "+location+" intermittent!")
                if location not in self.intermittent_components:
                    self.intermittent_components.append(location)
                    del self.machine_learning_buffer_inter[location]

        self.check_max_memory('intermittent')      
        
        return None

    def reset_counters(self, location):
        # if location in self.fault_counters.keys():
        #    del self.fault_counters[location]
        # else:
        #    pass
        # if location in self.health_counters.keys():
        #    del self.health_counters[location]
        # else:
        #    pass
        return None
    
    def return_allocated_memory(self, mem):
        memsize = 0
        memlen = 0
        
        this_global_bufs = {}
        this_global_bufs['fault'] = self.machine_learning_buffer
        this_global_bufs['intermittent'] = self.machine_learning_buffer_inter
        
        for buf in this_global_bufs.keys():
            if mem == buf:
                memlen = len(this_global_bufs[buf])
                if memlen is not 0:
                    for curKey in this_global_bufs[buf].keys():
                        memsize = this_global_bufs[buf][curKey].maxlen
                        break
                break
        
#         if mem == 'intermittent':
#             memlen = len(self.machine_learning_buffer_inter)
#             if memlen is not 0:
#                 for curKey in self.machine_learning_buffer_inter.keys():
#                     memsize = self.machine_learning_buffer_inter[curKey].maxlen
#                     break
#         elif mem == 'fault':
#             memlen = len(self.machine_learning_buffer)
#             if memlen is not 0:
#                 for curKey in self.machine_learning_buffer.keys():
#                     memsize = self.machine_learning_buffer[curKey].maxlen
#                     break
        if memsize is not 0:
            return memsize*memlen
        else:
            return -1   # error
    
    def check_max_memory(self, mem):
        if mem in self.memory_max.keys():
            if self.memory_max[mem] < self.return_allocated_memory(mem):
                self.memory_max[mem] = self.return_allocated_memory(mem)
        else:
            self.memory_max[mem] = self.return_allocated_memory(mem)
        return None

    # def return_allocated_memory(self):
    #    return len(self.health_counters) + len(self.fault_counters)

    def report(self, number_of_nodes, number_of_links):
        print "VEG: ==========================================="
        print "VEG:         MACHINE LEARNING REPORT"
        print "VEG: ==========================================="
        print "VEG: TODO"
        print "VEG: DEAD Components:", self.dead_components
        print "VEG: INTERMITTENT Components:", self.intermittent_components
        for mem in self.memory_max.keys():
            if self.memory_max[mem] is not -1:
                print "VEG: MAX memory (in bits) use of", mem, "::", self.memory_max[mem]
        for mem in {'intermediate', 'fault'}:
            if self.return_allocated_memory(mem) is not -1:
                print "VEG: END memory (in bits) use of", mem, "::", self.return_allocated_memory(mem)
        # print "MAX MEMORY USAGE:", self.memory_counter
        # print "AVERAGE COUNTER PER Node: ", float(self.memory_counter)/number_of_nodes
        return None
