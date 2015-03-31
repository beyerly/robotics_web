# This Python class provides integration with 'Lucy', the Artifical Intelligence
# web service provided by Martin Triplett at 
# http://droids.homeip.net/RoboticsWeb/Forms/Default.aspx
#
# The class provides an API to access the web-service, and mapping of Lucy commands and services
# to your local robot platform. The main class' main function brainAPI gets called with
# a string containing natural language (e.g. obtained from a Speech Regognition engine), and returns
# a list of local robot commands that can be executed on your local robot platform.
# The mapping of Lucy commands and your local robot platform commands is done through a CSV file that
# needs to get customized for every unique robot platform. For example:
#
# ID,Atom Name,serviceID,commandID,local Command,Voice cmd example,Description
# 22267,SpeechAgent,SpeechAgent,,<text2speech>,n/a,Command for text-to-speech
# 16896,Drive.Stop,2,1,move -1,<stop>,Stop robot locomotion
# 16897,Drive.Forward,2,2,<drive forward $data2>,drive forward 1 second,Drive Forward. $data2 contains numer of ms
# ...
#
# Usage: 
#
# from robotics_web import roboticsWebClass
#
# robotKey = 'xxxxx'  # Your robot Key at droids.homeip.net/RoboticsWeb
# debug = 0           
# csvFile = 'roboticsWebCmdMap.csv'
#
# roboticsWeb = roboticsWebClass(robotKey, debug, cvsFile)
# for localRobotCommand in roboticsWeb.brainAPI('<string>'):
#    <execute localRobotCommand>

import sys
import re
import time
import requests
import csv
import xml.etree.ElementTree as ET
import os

roboticsWebCmdMap = '../data/roboticsWebCmdMap.csv'

class roboticsWebClass:
   def __init__(self, robotKey, debug = 0, cmdMapCsv=roboticsWebCmdMap):
      self.robotKey = robotKey   # Robot Key on BrainTrust
      self.debug = debug
      self.cmdList = []
      self.cmdMap = self.parseCmdMap(cmdMapCsv)
      self.printCmdMap()
      
   # Print current command map, for debug only
   def printCmdMap(self):
      print "Current roboticsWeb to local command map:"
      for key in self.cmdMap:
         print key + " : " + self.cmdMap[key]

   # Parse the command map CSV file, which contains a mapping between
   # robotics_web commands and services and local robot platform commands
   # Returns a hash table with local commands keyed with a concatenation
   # of robotics_web commandID and serviceID
   def parseCmdMap(self, cmdMapCsv):
      cmdMap = {}
      if os.path.isfile(cmdMapCsv): 
         statusDump = open(cmdMapCsv, 'r')
      else:
         print "Can't open " + cmdMapCsv + "exiting..."
      csvfile = csv.reader(statusDump)
      for item in csvfile:
         if (re.match('[0-9]+', item[2]+item[3])):
            if (re.match('[a-z]+', item[4])):
               cmdMap[item[2]+item[3]] = item[4]
      return cmdMap

   # Returns a list of strings representing local robot commands.
   # 'text' is a string containing natural language
   def brainAPI(self, text):
      apiString = re.sub(' ', '%20', text)
      url = 'http://droids.homeip.net/RoboticsWeb/SimpleAPI.aspx?API.Key=29c7e1f3-23cf-496a-abd6-34e92e8d670f&Session.Key=New&Robot.Key=' + self.robotKey + '&Speech.Input=' + apiString
      self.cmdList = []
      if(self.debug):
         print url
         tree = ET.parse('robotweb.xml')
         root = tree.getroot()
      else:
         r = requests.get(url)
         if r:
            # parse query XML file returned by ANNA
            print r.content
            root = ET.fromstring(r.content)
      respSpeech = root.findall('Response.Speech')
      if respSpeech:
         for el in respSpeech:
            self.cmdList.append(self.cmdMap['00'] + ' ' + el.text)
      respCommandID = root.find('Response.Command.ID')
      respServiceID = root.find('Response.Service.ID')
      if (respCommandID != None):
         cmdKey = respServiceID.text + respCommandID.text
         if cmdKey in self.cmdMap: 
            localCmd = self.cmdMap[cmdKey]
            for x in range(1, 3):
               respData = root.find('Response.Command.Data.' + str(x))
               if respData!=None:
                  localCmd = re.sub('\$data' + str(x), respData.text, localCmd)
            self.cmdList.append(localCmd)
      if (len(self.cmdList) == 0):
         return ['Sorry, could not get any response from roboticsWeb']
      else:
         return self.cmdList

