from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import json
import os
import glob
import time
import datetime


def get_temp():
    temp = check_output(["vcgencmd","measure_temp"]).decode("UTF-8")
    return(findall("\d+\.\d+",temp)[0])

# Messaging setup
host = "a21qqqcnjf3ujn-ats.iot.us-east-2.amazonaws.com"		# this should be the address of your hostname at AWS
certPath = "/home/pi/certs/"		# wherever your certificates are located
clientId = "raspi"		# your AWS IoT device name
topic = "temperature"			# the name of the topic your messages will be written to

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
myAWSIoTMQTTClient.configureEndpoint(host, 8883)
myAWSIoTMQTTClient.configureCredentials(
	"{}AmazonRootCA1.pem".format(certPath), 
	"{}90ef350a84-private.pem.key".format(certPath), 
	"{}90ef350a84-certificate.pem.crt".format(certPath))

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
myAWSIoTMQTTClient.connect()

# Publish to the same topic in a loop forever
while True:
    message = {}
    message['timestamp'] = str(datetime.datetime.now())
    message['temperature'] = get_temp()
    messageJson = json.dumps(message)
    myAWSIoTMQTTClient.publish(topic, messageJson, 1)
    #print('Published topic %s: %s\n' % (topic, messageJson))
    time.sleep(10)	# Sleep 10 seconds between loops
myAWSIoTMQTTClient.disconnect()