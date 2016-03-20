# Copyright (C) 2015 Siavoosh Payandeh Azad

import networkx
import hashlib
import copy
import re
from Mapper import Mapping_Functions
import SHMU_Functions
from ConfigAndPackages import Config
import random


class SystemHealthMonitoringUnit:
    def __init__(self):
        self.SHM = networkx.DiGraph()   # System Health Map
        self.SnapShot = None
        self.MPM = {}                     # Most Probable Mapping Lib
        self.signal_reconfiguration = False
        self.system_degradation = 0

    def check_for_reconfiguration(self):
        degradation = self.calculate_system_degradation()
        # print degradation, self.system_degradation
        # todo: this should not be a fix number! system should check if the conditions are ok or not
        if degradation > self.system_degradation * 1.02:
            self.system_degradation = degradation
            self.signal_reconfiguration = True
        else:
            pass

    def calculate_system_degradation(self):
        broken_components = 0
        for node in self.SHM.nodes():
            if not self.SHM.node[node]['NodeHealth']:
                broken_components += 1
            for turn in self.SHM.node[node]['TurnsHealth']:
                if not self.SHM.node[node]['TurnsHealth'][turn]:
                    broken_components += 1
        for link in self.SHM.edges():
            if not self.SHM.edge[link[0]][link[1]]['LinkHealth']:
                broken_components += 1
        total_components = len(self.SHM.nodes())*(1+len(self.SHM.node[0]['TurnsHealth'])) + len(self.SHM.edges())
        degradation = float(broken_components)/total_components
        return degradation

    def setup_noc_shm(self, ag, turns_health, report):
        if report:
            print ("===========================================")
            print ("PREPARING SYSTEM HEALTH MAP...")
        if not Config.SetRoutingFromFile:
            for node in ag.nodes():
                self.SHM.add_node(node, TurnsHealth=copy.deepcopy(turns_health), NodeHealth=True, NodeSpeed=100,
                                  RouterTemp=10, NodeTemp=random.randint(0, Config.MaxTemp))
        else:
            try:
                routing_file = open(Config.RoutingFilePath, 'r')
            except IOError:
                print ('CAN NOT OPEN', Config.RoutingFilePath)

            while True:
                line = routing_file.readline()
                if "Ports" in line:
                    ports = routing_file.readline()
                    port_list = ports.split()
                    print ("port_list:", port_list)
                if "Node" in line:
                    node_id = int(re.search(r'\d+', line).group())
                    node_turns_health = copy.deepcopy(turns_health)
                    line = routing_file.readline()
                    turns_list = line.split()
                    for turn in node_turns_health.keys():
                        if turn not in turns_list:
                            node_turns_health[turn] = False
                    self.SHM.add_node(node_id, TurnsHealth=copy.deepcopy(node_turns_health), NodeHealth=True,
                                      NodeSpeed=100, RouterTemp=0, NodeTemp=0)
                if line == '':
                    break
            for node in ag.nodes():
                if node not in self.SHM.nodes():
                    self.SHM.add_node(node, TurnsHealth=copy.deepcopy(turns_health), NodeHealth=True,
                                      NodeSpeed=100, RouterTemp=0, NodeTemp=0)
        for link in ag.edges():
            self.SHM.add_edge(link[0], link[1], LinkHealth=True)

        self.system_degradation = self.calculate_system_degradation()
        if report:
            print ("SYSTEM HEALTH MAP CREATED...")

    ##################################################
    def break_link(self, link, report):
        if report:
            print ("===========================================")
            print ("\033[33mSHM::\033[0m BREAKING LINK: "+str(link))
        self.SHM.edge[link[0]][link[1]]['LinkHealth'] = False

    def restore_broken_link(self, link, report):
        if report:
            print ("===========================================")
            print ("\033[33mSHM::\033[0m LINK: "+str(link)+" RESTORED...")
        self.SHM.edge[link[0]][link[1]]['LinkHealth'] = True

    ##################################################
    def break_turn(self, node, turn, report):
        if report:
            print ("===========================================")
            print ("\033[33mSHM::\033[0m BREAKING TURN: "+str(turn)+" IN NODE "+str(node))
        self.SHM.node[node]['TurnsHealth'][turn] = False

    def restore_broken_turn(self, node, turn, report):
        if report:
            print ("===========================================")
            print ("\033[33mSHM::\033[0m TURN:"+str(turn)+" IN NODE"+str(node)+" RESTORED")
        self.SHM.node[node]['TurnsHealth'][turn] = True

    ##################################################
    def introduce_aging(self, node, speed_down, report):
        if report:
            print ("===========================================")
        self.SHM.node[node]['NodeSpeed'] *= 1-speed_down
        if report:
            print ("\033[33mSHM::\033[0m AGEING NODE:"+str(node)+" ... SPEED DROPPED TO: " +
                   str(self.SHM.node[node]['NodeSpeed'])+" %")
        if self.SHM.node[node]['NodeSpeed'] == 0:
            self.break_node(node, True)

    ##################################################
    def break_node(self, node, report):
        if report:
            print ("===========================================")
        self.SHM.node[node]['NodeHealth'] = False
        if report:
            print ("\033[33mSHM::\033[0m NODE "+str(node)+" IS BROKEN...")

    def restore_broken_node(self, node, report):
        if report:
            print ("===========================================")
        self.SHM.node[node]['NodeHealth'] = True
        if report:
            print ("\033[33mSHM::\033[0m NODE "+str(node)+" IS RESTORED...")

    ##################################################
    def take_snapshot_of_shm(self):
        self.SnapShot = copy.deepcopy(self.SHM)
        print ("A SNAPSHOT OF SYSTEM HEALTH HAS BEEN STORED...")
        return None

    ##################################################
    def restore_previous_snapshot(self):
        self.SHM = copy.deepcopy(self.SnapShot)
        print ("SYSTEM HEALTH MAP HAS BEEN RESTORED TO PREVIOUS SNAPSHOT...")
        self.SnapShot = None
        return None

    ##################################################
    def add_current_mapping_to_mpm(self, tg):
        """
        Adds a mapping (Extracted from TG) under a fault configuration to MPM.
        The dictionary key would be the hash of fault config
        :param tg: Task Graph
        :return: None
        """
        mapping_string = Mapping_Functions.mapping_into_string(tg)
        self.MPM[hashlib.md5(SHMU_Functions.generate_fault_config(self)).hexdigest()] = mapping_string
        return None

    ##################################################
    def clean_mpm(self):
        self.MPM = {}
        return None

    def update_node_temp(self, node, temp):
        """
        Will update a Node's temperature.
        :param node: Node ID Number
        :param temp: Temperature in centigrade
        :return: True if Node is healthy and temp update is successful and False if Not!
        """
        if self.SHM.node[node]['NodeHealth']:
            self.SHM.node[node]['NodeTemp'] = temp
            return True
        else:
            return False

    def update_router_temp(self, node, temp):
        """
        Will update a Router's temperature.
        :param node: Node ID Number
        :param temp: Temperature in centigrade
        :return: None
        """
        self.SHM.node[node]['RouterTemp'] = temp
        return None
