#! /usr/bin/env python3

import requests
import random

class Agent:

    # the last http cookie
    session = None

    # username and password
    username = ''
    password = ''
    personUri = ''

    # the URI of the node
    nodeUri = 'http://localhost/xodx/'

    # The person URI of the currently logged in User
    personUri = ''

    # The probability of a reply
    # Value between 0 and 1
    updateprobability = .5

    # The probability of a reply
    # Value between 0 and 1
    responsivity = .5

    # The probability to generate a new post
    # Value between 0 and 1
    productivity = .5

    activities = []

    debug = False

    def __init__ (self, nodeUri, username, password, updateprobability = .5, responsivity = .5, productivity = .5):
        self.nodeUri = nodeUri
        self.username = username
        self.password = password
        self.responsivity = responsivity
        self.productivity = productivity

    def prepare (self):
        self.resetModel()
        self.signup()
        self.login()

    # This method is called if a new round starts
    def round (self):
        u = random.random()
        p = random.random()
        if (u < self.updateprobability) :
            # check for updates
            self.getActivities()
            # iterate over the updates
            for a in self.activities:
                r = random.random()
                if (r < self.responsivity) :
                    self.reply(a)
        if (p < self.productivity) :
            self.post()

    def addFriend (self, uri):
        r = self.http(
            self.nodeUri,
            get = {'c': 'person', 'a': 'addfriend'},
            post = {'person': self.personUri, 'friend': uri}
        )
        if (self.debug):
            print(r.content)

    def post (self):
        r = self.http(
            self.nodeUri,
            get = {'c': 'activity', 'a': 'addactivity'},
            post = {'content': 'new message', 'type': 'note'}
        )
        if (self.debug):
            print(r.content)

    def reply (self, activity):
        r = self.http(
            self.nodeUri,
            get = {'c': 'activity', 'a': 'addactivity'},
            post = {'content': 'new reply', 'type': 'comment', 'reply': activity}
        )
        if (self.debug):
            print(r.content)

    def getActivities (self):
        r = self.http(
            self.nodeUri,
            get = {'c': 'user', 'a': 'getactivitystream', 'num': '5', 'own': 'false'},
        )
        self.activities = r.text.split()

    def signup (self):
        r = self.http(
            self.nodeUri,
            get = {'c': 'application', 'a': 'newuser'},
            post = {'username': self.username, 'password': self.password, 'passwordVerify': self.password}
        )
        if (self.debug):
            print(r.content)

    def login (self):
        r = self.http(
            self.nodeUri,
            get = {'c': 'application', 'a': 'login'},
            post = {'username': self.username, 'password': self.password}
        )
        if (self.debug):
            print(r.content)
        r = self.http(
            self.nodeUri,
            get = {'c': 'user', 'a': 'getpersonuri'}
        )
        self.personUri = r.text

    def resetModel (self):
        r = self.http(
            self.nodeUri,
            get = {'c': 'setup', 'a': 'cleardatabase'},
        )
        if (self.debug):
            print(r.content)

    def http (self, uri, get = [], post = []):
        # execute the http request, send the cookie
        # store the cookie

        if (self.session == None) :
            self.session = requests.Session()

        uri+= '?'

        for key in get:
            uri+= key + '=' + get[key] + '&'

        if (self.debug):
            print(uri)

        r = self.session.post(uri, post, headers={'Accept': 'text/json'})

        return r
