#! /usr/bin/env python3

import csv
import agent

# The testbed class models a testsetup of agents
class Testbed:

    # A collection of agents which are simulated
    agentsNotInit = []
    agents = {}

    # friendship relations (the key is the source of the relation, the value the target)
    friendships = {}

    def __init__ (self, agentConfigs, friendships):
        # read the agent configurations
        print("reading agent configurations …")
        with open(agentConfigs, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for row in reader:
                if (row[0][:1] == '#'):
                    row = reader.__next__()
                a = agent.Agent(row[0], row[1], row[2], row[3], row[4], row[5])
                self.agentsNotInit.append(a)
        # prepare the agents
        print("preparing agents …")
        for a in self.agentsNotInit:
            a.prepare()
            print ("\tAdd Agent: " + a.personUri + " to list")
            self.agents[a.personUri] = a
        # read friendship relations file
        print("reading friendship relations …")
        with open(friendships, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for row in reader:
                if (row[0][:1] == '#'):
                    row = reader.__next__()
                self.friendships[row[0]] = row[1]
        # build frienships
        print("establishing friendship relations …")
        for a in self.friendships.keys():
            b = self.friendships[a]
            self.agents[a].addFriend(b)
            print("\t" + a + " -> " + self.friendships[a])

    def start (self):
        # start the simulation
        print()

    def stats (self):
        # calculate the stats
        # amount of triples per node
        # amount of incomming friendships (maybe based on the force-feedback-graph)
        # responsivity and co
        print()
