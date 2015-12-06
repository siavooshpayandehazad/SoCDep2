# Copyright (C) 2015 Siavoosh Payandeh Azad


class CounterThreshold():

    def __init__(self, threshold):
        self.counters = {}
        self.threshold = threshold
        self.dead_components = []

    def increase_counter(self, location, logging):
        if type(location) is dict:
            # print location, str(location.keys()[0])+str(location[location.keys()[0]])
            location = "R"+str(location.keys()[0])
        elif type(location) is tuple:
            # print location, location[0], location[1]
            location = str(location[0])+str(location[1])
        elif type(location) is int:
            # print location
            location = str(location)
        else:
            print location, type(location)
            raise ValueError("location type is wrong!")

        if location in self.counters.keys():
            self.counters[location] += 1
        else:
            self.counters[location] = 1
        logging.info("Increasing counter at location: "+location+" Counter: "+str(self.counters[location]))
        if self.counters[location] == self.threshold:
            logging.info("Declaring component: "+location+" dead!")
            self.dead_components.append(location)
        return None

    def decrease_counter(self, location, logging):
        if type(location) is dict:
            # print location, str(location.keys()[0])+str(location[location.keys()[0]])
            location = str(location.keys()[0])+str(location[location.keys()[0]])
        elif type(location) is tuple:
            # print location, location[0], location[1]
            location = str(location[0])+str(location[1])
        elif type(location) is int:
            # print location
            location = str(location)

        if location in self.counters.keys():
            self.counters[location] -= 1
            logging.info("Decreasing counter at location: "+location+" Counter: "+str(self.counters[location]))
            if self.counters[location] == 0:
                del self.counters[location]
                logging.info("Freeing counter at location: "+location)
        else:
            pass
        return None

    def reset_counter(self, location):
        if location in self.counters.keys():
            del self.counters[location]
        else:
            pass
        return None