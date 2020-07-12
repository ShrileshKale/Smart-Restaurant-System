# /***************************
#  *  controller.py
#  * Version Number	: 1.0
#  * Configuration Identifier: 
#  * Modified by:  Shrilesh Kale and Pushkar Kulkarni       
#  * Modified Date:  12/07/2020       
#  * Description: Source code for backend operations for smart lighting operations
#  **************************/

# -*- coding: utf-8 -*-
from app import app
from flask import Response, request, render_template,redirect,url_for
import json
import math
import webbrowser
import ast
from bson import json_util
import RPi.GPIO as GPIO
import time
import sys
import os
import threading
import grovepi
import boto3
from botocore.exceptions import ClientError
import multiprocessing
from multiprocessing import Pool,Process
from constants import *
import paho.mqtt.client as mqtt

# Check for  Command line argument 
try: 
	if sys.argv[1] != ( 0  or ''):
		print 'Ip address given is:-'+str(sys.argv[1])
		ipAddr = sys.argv[1]

except Exception, e:
	print 'Please provide IP address of Broker as a parameter like e.g. python server.py 192.168.0.101'
	print ("Error:{}".format(e))
	raise e
	

# *******************************************************************************
  # Function    : on_connect
  # Description : Function for MQTT connect ,triggrs when connection established
  #               
  # Input       : mqtt object ,rc flag 
  # Output      : NA
  # Return      : NA
# *******************************************************************************/

def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))
    print('Connected')

# *******************************************************************************
  # Function    : on_message
  # Description : This function (callback) for actions to be performed after receiving data
  #               
  # Input       : mqttc object,payload
  # Output      : NA
  # Return      : NA
# *******************************************************************************/

def on_message(mqttc, obj, msg):
    # print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    print(msg.payload)
    if (msg.payload == 'ON'):
    	print 'Inside ON'
    	time.sleep(10)
    	publish_data()
    else:
    	return
 
# *******************************************************************************
  # Function    : on_subscribe
  # Description : This function triggers when system subscibes to a perticular topic
  #               
  # Input       : mqttc ,obj, mid, granted_qos
  # Output      : NA
  # Return      : NA
# *******************************************************************************/

def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))
    return


# *******************************************************************************
  # Function    : publish_data
  # Description : Function to publish data
  #               
  # Input       : NA
  # Output      : NA
  # Return      : NA
# *******************************************************************************/

# Fucntion to publish data
def publish_data():
	mqttc = mqtt.Client("client-id")
	mqttc = mqtt.Client()
	mqttc.connect(ipAddr, 1883, 60)
	print 'inside publish'

	Data = {
	'Appliance': 'OFF'
	}
	print 'after inside publish'
	print(Data)
	mqttc.publish('lighting_control/central/appliance/Rpi',json.dumps(Data))
	print("Data Published")
	time.sleep(1)


# *******************************************************************************
  # Function    : mqttData
  # Description : Function to initialize MQTT connection
  #               
  # Input       : NA
  # Output      : NA
  # Return      : NA
# *******************************************************************************/
def mqttData():
	mqttc = mqtt.Client("client-id")
	mqttc = mqtt.Client()
	mqttc.on_message = on_message
	mqttc.on_connect = on_connect
	mqttc.on_subscribe = on_subscribe
	mqttc.connect(ipAddr, 1883, 60)
	mqttc.subscribe("lighting_control/central/appliance/esp8266", 1)
	mqttc.loop_forever()


# *******************************************************************************
  # Function    : emailNotification
  # Description : Function to send Email Notification using Amazon SES service
  #               
  # Input       : NA
  # Output      : NA
  # Return      : NA
# *******************************************************************************/

def emailNotification(emailNotificationContent):
	# Inspired from Amazon SDK tutorial for Simple Email Service
	global listForperDayCost,listForWeekCost,billEmailnotification
	if (emailNotificationContent == billEmailnotification):
		billEmailnotification = billEmailnotification+str(listForWeekCost[0])+str(',')
		if listForWeekCost[0] != 0:
			del listForWeekCost[:]
		emailNotificationContent = billEmailnotification

	SENDER = "Smart Restaurant Manager <shrileshkale22222@gmail.com>"
	RECIPIENT = "pushkarvk@gmail.com"
	AWS_REGION = "eu-central-1"
	# The subject line for the email.
	SUBJECT = "Energy Usage Alert"
	# The email body for recipients with non-HTML email clients.
	BODY_TEXT = ("Amazon SES Test (Python)\r\n"
	             "Total bill for this day is"
	            
	            )         
	# The HTML body of the email.
	BODY_HTML = """<html>
	<head>  </head>
	<body>
	  <h1>Total bill for this day is: {{ var }} </h1>
	  
	</body>
	</html>"""            
	# The character encoding for the email.
	CHARSET = "UTF-8"
	# Create a new SES resource and specify a region.
	client = boto3.client('ses',region_name=AWS_REGION)
	# Try to send the email.
	try:
	    #Provide the contents of the email.
	    response = client.send_email(
	        Destination={
	            'ToAddresses': [
	                RECIPIENT,
	            ],
	        },
	        Message={
	            'Body': {
	                'Html': {
	                    'Charset': CHARSET,
	                    'Data':emailNotificationContent ,
	                },
	                'Text': {
	                    'Charset': CHARSET,
	                    'Data': BODY_TEXT ,
	                },
	            },
	            'Subject': {
	                'Charset': CHARSET,
	                'Data': SUBJECT,
	            },
	        },
	        Source=SENDER,
	    )
	# Display an error if something goes wrong.	
	except ClientError as e:
	    print(e.response['Error']['Message'])
	else:
	    print("Email sent! Message ID:"),
	    print(response['MessageId'])


# *******************************************************************************
  # Function    : panicNotification
  # Description : Function to send SMS using Amazon SNS service
  #               
  # Input       : text to be sent to user (e.g HelloWorld)
  # Output      : Text message
  # Return      : NA
# *******************************************************************************/

def panicNotification(notification):
	print 'inside panicNotification'
	# Create an SNS client
	client = boto3.client(
	    "sns",
	    aws_access_key_id="XXXXX",
	    aws_secret_access_key="XXXXX",
	    region_name="us-east-1"
	)
	# Send your sms message.
	client.publish(
	    PhoneNumber="+491123456789",
	    Message= notification,
	    MessageAttributes = {'AWS.SNS.SMS.SenderID':
				 { 'DataType': 'String', 'StringValue': 'TestSender' },
	    			'AWS.SNS.SMS.SMSType': { 'DataType': 'String', 'StringValue': 'Transactional'} }
				)
	print 'SMS sent'

# *******************************************************************************
  # Function    : dimmingPositive()
  # Description : Function for dimming a light(0 to 100)
  #               
  # Input       : NA
  # Output      : brightness control
  # Return      : dimming value (Percentage)
# *******************************************************************************/
@app.route('/dimmingpositive-mode')
def dimmingPositive():
	print 'Positive Dimming'
	global value,brightness
	try:
		brightness = brightness*2
		if brightness >= 100:
			brightness = 100
		breathingEffect.ChangeDutyCycle(brightness)
		print "New Brightness is: ",brightness 
		time.sleep(0.05)
		
	except:
		print 'Error'

	return str(brightness)
	
# *******************************************************************************
  # Function    : dimmingNegative()
  # Description : Function for Dimming of a light (100 to 0)
  #               
  # Input       : NA
  # Output      : brightness control
  # Return      : dimming value (Percentage)
# *******************************************************************************/

@app.route('/dimmingnegative-mode')
def dimmingNegative():

	global brightness
	print 'Negative Dimming'
	brightness = brightness/2
	if brightness > 0:
		breathingEffect.ChangeDutyCycle(brightness)
		print "New Brightness is: ",brightness #Notify User of Brightness
		time.sleep(0.05)
	else:
		print 'Duty cycle value exceeded and Duty cycle reseted to 100%'
		brightness = 100
	print ' Duty Value is:-',str(brightness)

	return str(brightness)


# *******************************************************************************
  # Function    : panicPanel()
  # Description : Function to send SMS and Email in panic situation
  #               
  # Input       : NA
  # Output      : NA
  # Return      : 1
# *******************************************************************************/


# Route for Panic function ( panicNotification()
@app.route('/panic-mode')
def panicPanel():
	global panicEmailNotification
	print 'before panic'
	# panicNotification()
	panicNotification("In emergency!")
	emailNotification(panicEmailNotification)
	time.sleep(3)
	print 'after panic'
	return str(1)

# *******************************************************************************
  # Function    : LightSenseDetect()
  # Description : Function for lighing using light sensor
  #               
  # Input       : Light (imaginary)
  # Output      : sensor value 
  # Return      : NA
# *******************************************************************************/

def LightSenseDetect():

	try: 
		while True:
			# Get sensor value
			print 'inside automaticlighting-mode'
			sensor_value = grovepi.analogRead(light_sensor)
			# Calculate resistance of sensor in K
			resistance = (float)(1023 - sensor_value) * 10 / sensor_value
			if resistance > threshold:
				grovepi.digitalWrite(normalLightLed,1)
			elif resistance < threshold:
				grovepi.digitalWrite(normalLightLed,0)
			print("sensor_value = %d resistance = %.2f" %(sensor_value,  resistance))
			time.sleep(.5)

	except IOError:
		print ("Error")


# *******************************************************************************
  # Function    : process()
  # Description : Function to deploy automatic lighting function(LightSenseDetect) as a process
  #               
  # Input       : NA
  # Output      : Deployes a process
  # Return      : Json Reponse (Success/Failure)
# *******************************************************************************/

# Route for deploying LightSenseDetect() function as a process when user clicks on Automatic light button
@app.route('/automaticlighting-mode', methods=["POST"])
def process():
	global p1,startTimeOfAutomaticLight

	try:
		response = request.get_json(force=True)
		if response['status']:
			p1 = multiprocessing.Process(target=LightSenseDetect)
			p1.daemon=True 
			p1.start()
			startTimeOfAutomaticLight = int(time.time())
			print 'Recorded Start time of Automatic light',str(startTimeOfAutomaticLight)
			print 'p1 id:'+str(p1.pid)
		elif response['status'] == False:
			if (response['status'] == False ) and (p1 == 0):
				print 'Prcess is not started correctly'
			p1.terminate()
			print 'p1 terminated:'+str(p1.pid)
			grovepi.digitalWrite(normalLightLed,0)

		return Response(json.dumps({
			"status": "success",
			"message": "Data received successfully"
		}, default=json_util.default), mimetype="application/json")


	except Exception, e:
		print ("Error:{}".format(e))
		raise e
		return Response(json.dumps({
			"status": "failure",
			"message": "Invalid request: %s" %e
		}, default=json_util.default), mimetype="application/json")


# *******************************************************************************
  # Function    : normalLight()
  # Description : Function for lighing using humann control
  #               
  # Input       : NA
  # Output      : light ON/OFF
  # Return      : Json object ( Successfull or Failure)
# *******************************************************************************/
	
@app.route('/normalLight-mode', methods=["POST"])
def normalLight():
	global p1,startTime
	try:
		grovepi.digitalWrite(normalLightLed,0)
		response = request.get_json(force=True)
		if response['status']:
			grovepi.digitalWrite(normalLightLed,1)
			startTime = int(time.time())
			print 'Start time is',str(startTime)
			if p1 != 0:
				p1.terminate()
				print 'p1 terminated:'+str(p1.pid)
			else:
				print 'Automatic lighting Process is not started'

		elif response['status'] == False:
			grovepi.digitalWrite(normalLightLed,0)

		return Response(json.dumps({
				"status": "success",
				"message": "Data received successfully"
			}, default=json_util.default), mimetype="application/json")

	except Exception, e:
		return Response(json.dumps({
			"status": "failure",
			"message": "Invalid request: %s" %e
		}, default=json_util.default), mimetype="application/json")


# *******************************************************************************
  # Function    : allLightsoff()
  # Description : Function to switch off lights
  #               
  # Input       : NA
  # Output      : light OFF and calculation of bill 
  # Return      : Total Energy Consumption and Anverage Energy Consumption per day
# *******************************************************************************/
	
@app.route('/lightsOff-mode')
def allLightsoff():
	global energyConsumptionChartData,avgEnergyConsumptionPerDay,listForWeekCost,energyConsumptionChartDataPerDay,totalCostForaWeek,billEmailnotification
	global startTime,p1,startTimeOfAutomaticLight,totalTimeNormalLight,totalTimeAutomaticLight
	print 'Start time of Automatic light',str(startTimeOfAutomaticLight)
	print 'Start time of Normal light',str(startTime)

	print 'inside light off'
	grovepi.digitalWrite(normalLightLed,0)
	# Calculation for time 
	try:
		if p1 !=0:
			p1.terminate()
			print 'p1 terminated:'+str(p1.pid)
			
		if (startTime or startTimeOfAutomaticLight)!= 0:
			stopTime = int(time.time())
			print 'Stop time is',str(stopTime)
			if startTime !=0:
				totalTimeNormalLight = stopTime - startTime
				print ('Total Normal light time',str(totalTimeNormalLight))

			if startTimeOfAutomaticLight !=0:
				totalTimeAutomaticLight = stopTime - startTimeOfAutomaticLight
				print ('Total Automatic light time',str(totalTimeAutomaticLight))

			totalTime = totalTimeNormalLight + totalTimeAutomaticLight
			print 'Total time is',str(totalTime)
			# so that total bill count shoud not get previous values of totalTimeAutomaticLight ,totalTimeNormalLight
			totalTimeAutomaticLight = 0
			totalTimeNormalLight = 0
			enegyBillCalculation , kwattHourEnergy ,totalProduct , avgEnergyConsumptionPerDay  = energyConsumption(totalTime)
			avgEnergyConsumptionPerDayData.append(avgEnergyConsumptionPerDay)

			#Chart Data
			energyConsumptionChartData.append(enegyBillCalculation)
			energyConsumptionChartDataPerDay.append(enegyBillCalculation)

			# For getting weekly Cost , get the list(array) of string (costCalc) , convert it into array of float
			# and take the sum
			sumOfBillForWeekList = [float(i) for i in energyConsumptionChartData]

			print 'Array of sumOfBillForWeekList',str(sumOfBillForWeekList)
			sumOfBillForWeek = sum(sumOfBillForWeekList)
			print 'Sum of Bill for Week',str(sumOfBillForWeek)

			# appending sumofBill in a list so that bar graph could show it
			if len(energyConsumptionChartData) == 3:
				print 'Data appended after 3 vals'
				listForWeekCost.append(sumOfBillForWeek)
				del sumOfBillForWeekList[:]
				sumOfBillForWeek = 0
				print'Sum of Bill after Deleting',str(sumOfBillForWeekList)
				listForperDayCost.append(listForWeekCost[0])

				# Send notification to user 
				emailNotification(billEmailnotification)
				panicNotification("Bill has been generated!")

				del energyConsumptionChartData[:]
				# Deleting sum of cost values present in listForWeekCost list so that I can get new values for new day of a week
				del listForWeekCost[:]
				print 'After delete:',str(energyConsumptionChartData)
				# print 'List per Day cost:',str(listForperDayCost)
				print 'Data of  energyConsumptionChartData array is',str(energyConsumptionChartData)
				print 'Length of energyConsumptionChartData  array is',str(len(energyConsumptionChartData))

				# For showing the total cost per day on weekly report graph.
				totalCostForaWeek = [float(i) for i in listForperDayCost]
				totalCostForaWeek = sum(totalCostForaWeek)
				totalCostForaWeek = round(totalCostForaWeek,3)

			startTime = 0 # if user click a button more than 1 times then totaltime should be zero
			stopTime =  0
			startTimeOfAutomaticLight = 0
			if (startTime and stopTime and startTimeOfAutomaticLight) == 0:
				print "Thank you"

		else:
			print 'Start times are not detected'

		return str(energyConsumption), str(avgEnergyConsumptionPerDay)

	except KeyboardInterrupt:
		emailNotification(billEmailnotification)

# *******************************************************************************
  # Function    : energyConsumption()
  # Description : Function to switch off lights
  #               
  # Input       : total time for which light was on
  # Output      : NA
  # Return      : costCalc, kwattHour,totalProduct,avgEnergyConsumptionPerDay
# *******************************************************************************/

def energyConsumption(time):
	global billEmailnotification
	result={}
	totalTime = time
	try:
		deviceWattage = 50
		basePrice = 8.80 # base price in germany
		eurosPerKwattHour = 0.30 # 0.30 euros per kwhr
		hoursUsedPerDay = float(float(totalTime)/float(3600))
		wattHour = deviceWattage * hoursUsedPerDay
		kwattHour = float(float(wattHour) / float(1000))
		kwattHour = round(kwattHour,5)
		# Average Engery Consumption Calculation
		# get instance of data in a list , convert it into dictionary (key and value pairs)
		kwattHourEnergyConsumedData.append(kwattHour)
		temp=set(kwattHourEnergyConsumedData)

		# below code gives the count of specific number repeated in a list in a key,value form e.g 5 repeated 2 time ('5': '2')
		for i in temp:
			result[i] = kwattHourEnergyConsumedData.count(i)
		# Interate through all the key and values and take the product of key*value uisng inbuilt sum function
		for key, value in result.iteritems():
			print 'key is',str(key)
			print 'value is' ,str(value)

		# product of instance number with energy values and get the sum
		totalProduct = sum([float(key) * float(value) for key, value in result.iteritems()])

		print float(totalProduct)/float(len(result))

		#average of Energy Data
		avgEnergyConsumptionPerDay = float(totalProduct)/float(len(result))

		avgEnergyConsumptionPerDayForCostCalc = round(avgEnergyConsumptionPerDay, 5)

		avgEnergyConsumptionPerDay  = avgEnergyConsumptionPerDay * 10000

		# roundedkwattHour =  round(kwattHour,5)
		costCalc = basePrice + (avgEnergyConsumptionPerDayForCostCalc*eurosPerKwattHour) 
		# print "Total cost is : - ",str(costCalc)
		roundedcostCalc = round(costCalc,5)
		# print "Total rounded cost is : - ",str(roundedcostCalc)

		return str(costCalc), str(kwattHour),str(totalProduct), str(avgEnergyConsumptionPerDay)

	except KeyboardInterrupt:
		emailNotification(billEmailnotification)
		print 'Error in energyConsumption Calculation'

# *******************************************************************************
  # Function    : controlPanel()
  # Description : Function which calls mqtt process and renders main control panel page
  #               
  # Input       : NA
  # Output      : NA
  # Return      : NA
# *******************************************************************************/

# Main control panel route for UI 
@app.route('/control-panel', methods=["GET"])
def controlPanel():
	try:
		global mqttProcess
		if mqttProcess != 0:
			mqttProcess.terminate()
			print 'MQTT terminated:'+str(mqttProcess.pid)

		mqttProcess = multiprocessing.Process(target=mqttData)
		mqttProcess.daemon=True 
		mqttProcess.start()
		print 'mqttData process id:'+str(mqttProcess.pid)
		return render_template('index.html')
	except:
		print ("Error:{}".format(e))
		raise e

# *******************************************************************************
  # Function    : energyPanel()
  # Description : Function which renders energy panel page
  #               
  # Input       : NA
  # Output      : NA
  # Return      : chart html web page
# *******************************************************************************/

# Energy Panel for Daily Energy Monitoring
@app.route('/energy-Panel' , methods=["GET"])
def energyPanel():
	global energyConsumptionChartData,avgEnergyConsumptionPerDay,avgEnergyConsumptionPerDayData,energyConsumptionChartDataPerDay,billEmailnotification
	global mqttProcess
	try:
		
		if request.method == 'GET':
			labels_for_day_energy_chart = labels
			line_values =  avgEnergyConsumptionPerDayData
			labels_for_week_energy_chart = labels_week
			lables_week_values = energyConsumptionChartDataPerDay

			# If length becomes 14 then reset the list (writng this just because we are considering only 14 samples/day)
			if len(avgEnergyConsumptionPerDayData) == 15:
				del avgEnergyConsumptionPerDayData[:]

			# If length becomes 14 then reset the list (writng this just because we are considering only 14 samples/day)
			if len(energyConsumptionChartDataPerDay) == 15:
				del energyConsumptionChartDataPerDay[:]

			return render_template('chart.html', title='Live Energy Consumption', max=10, labels=labels_for_day_energy_chart, values=line_values , labels_week =labels_for_week_energy_chart, lables_week_values = energyConsumptionChartDataPerDay )
	
	except KeyboardInterrupt:
		emailNotification(billEmailnotification)
		pass

# *******************************************************************************
  # Function    : ligntingControl()
  # Description : Function for manual table lighting
  #               
  # Input       : NA
  # Output      : NA
  # Return      : Json object (Success or Failure)
# *******************************************************************************/


@app.route('/device/lignting', methods=["POST"])
def ligntingControl():

	try:
		response = request.get_json(force=True)
		avoidUnicode = json.dumps(response)
		if response['light'] == '1' and response['status']:
			print response['light']
			print 'inside light 1'
			grovepi.digitalWrite(tableLightled,1)
			time.sleep(2)
			print 'after light 1 sleep'

		elif response['status'] == False and response['light'] == '1':
			print 'else of 1'
			grovepi.digitalWrite(tableLightled,0)

		if response['light'] == '2' and response['status']:
			print response['light']
			grovepi.digitalWrite(tableLightled,1)
			time.sleep(1)
			print 'after light 2 sleep'

		elif response['status'] == False and response['light'] == '2':
			print 'else of 2'
			grovepi.digitalWrite(tableLightled,0)

		if response['light'] == '3' and response['status']:
			print response['light']
			grovepi.digitalWrite(tableLightled,1)
			time.sleep(2)
			print 'after light 3 sleep'

		elif response['status'] == False and response['light'] == '3':
			print 'else of 3'
			grovepi.digitalWrite(tableLightled,0)

		return Response(json.dumps({
			"status": "success",
			"message": "Data received successfully"
		}, default=json_util.default), mimetype="application/json")

	except Exception, e:
		return Response(json.dumps({
			"status": "failure",
			"message": "Invalid request: %s" %e
		}, default=json_util.default), mimetype="application/json")

# *******************************************************************************
  # Function    : reset()
  # Description : Function to reset energy monitoring data
  #               
  # Input       : NA
  # Output      : NA
  # Return      : chart webpage 
# *******************************************************************************/


# Function for reseting daily energy monitoring
@app.route('/reset-mode', methods=["GET"])
def reset():
	global energyConsumptionChartData,avgEnergyConsumptionPerDayData,energyConsumptionChartDataPerDay
	try:
		labels_for_day_energy_chart = labels
		line_values =  [0]
		labels_for_week_energy_chart = labels_week
		lables_week_values = [0]
		del energyConsumptionChartDataPerDay[:]
		del avgEnergyConsumptionPerDayData[:]
		print 'energyConsumptionChartDataPerDay',str(energyConsumptionChartData)
		print 'avgEnergyConsumptionPerDayData',str(avgEnergyConsumptionPerDayData)
		return render_template('chart.html', title='Live Energy Consumption', max=10, labels=labels_for_day_energy_chart, values= line_values , labels_week = labels_for_week_energy_chart, lables_week_values = lables_week_values )
	
	except:
		print ("Error:{}".format(e))
		raise e


# *******************************************************************************
  # Function    : weekReport()
  # Description : Function to show weekly data on web page
  #               
  # Input       : NA
  # Output      : NA
  # Return      : renders weekData webpage
# *******************************************************************************/

# Function for weekly energy monitoring
@app.route('/week-report', methods=["GET"])
def weekReport():
	global listForperDayCost,totalCostForaWeek
	try:
		labels_for_weekly_energy_chart = weekly_report_labels
		print "List of Week Day is",str(listForperDayCost)
		# if len becomes 7 , reset the chart
		if len(listForperDayCost) == 7:
			del listForperDayCost[:]
			# listForperDayCost = [0]
		return render_template('weekDataChart.html', title='Weekly Cost Report', max= 100, labels = labels_for_weekly_energy_chart, values = listForperDayCost , totalCost = totalCostForaWeek)
	except:
		print ("Error:{}".format(e))
		raise e

# *******************************************************************************
  # Function    :resetWeekData()
  # Description : Function to reset weekly energy data.
  #               
  # Input       : NA
  # Output      : NA
  # Return      : renders weekData webpage
# *******************************************************************************/

@app.route('/resetweek-mode', methods=["GET"])
def resetWeekData():
	try:
		global listForperDayCost
		labels_for_week_energy_chart = weekly_report_labels
		values_week = [0]
		print 'Week Data resseted'
		del listForperDayCost[:]
		return render_template('weekDataChart.html', title='Weekly Cost Report', max= 100, labels = labels_for_week_energy_chart, values = values_week )
	except:
		print ("Error:{}".format(e))
		raise e

# *******************************************************************************
  # Function    :temperatureControl()
  # Description : Function to get temperature and Humidity values
  #               
  # Input       : NA
  # Output      : Turns on AC if temperature goes beyond 25 degree Celcius
  # Return      : Json Response ( Success/Failure)
# *******************************************************************************/

@app.route('/device/environment', methods=["GET"])
def temperatureControl():
	# return 'ok'
	try:
		[temp,humidity] = grovepi.dht(temp_sensor,blue)
		time.sleep(1)  
		if math.isnan(temp) == False and math.isnan(humidity) == False:
			print("temp = %.02f C humidity =%.02f%%"%(temp, humidity))

		if (temp >= 25):
			print 'Turning ON AC'

		elif (temp < 25):
			print 'Turning on Heater'

		else:
			print('Failed to get reading. Try again!')

		return Response(json.dumps({
				"status": "success",
				"temperature":int(temp),
				"humidity": int(abs(humidity)),
				"message": "Data received successfully"
			}, default=json_util.default), mimetype="application/json")

	except Exception, e:

		print
		print ("Error:{}".format(e))
		raise e
		return Response(json.dumps({
			"status": "failure",
			"message": "Invalid request: %s" %e
		}, default=json_util.default), mimetype="application/json")


		
	

