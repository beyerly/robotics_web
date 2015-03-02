
robotics_web

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
