import RPi.GPIO as GPIO
import grovepi
# /***************************************
#  *  CONSTANTS DECLARATION
#  ****************************************/
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
global breathingEffect
Imu90dofSensorReading = 0
tableLightled = 6
normalLightLed = 5
light_sensor = 0
temp_sensor = 2
blue = 0
flag = True
value = 10
startTime = 0
startTimeOfAutomaticLight = 0
totalTimeNormalLight = 0 
totalTimeAutomaticLight = 0
dutyValue = 100
energyConsumptionChartData = []
kwattHourEnergyConsumedData = []
avgEnergyConsumptionPerDayData = []
avgEnergyConsumptionPerDay = 0
listForWeekCost = []
listForperDayCost = []
energyConsumptionChartDataPerDay = []
totalCostForaWeek = [0]
brightnessControlLed = 16
p1 = 0
mqttProcess = 0
billEmailnotification = '<html> <h2> Total bill for this day is:-</h2> <p> Regards <p> </html>'
panicEmailNotification = '<html> <h2> Hello, Mr Pushkar Kulkarni is in trouble ,Please help him with his key and contact him immidiately  </h2> <p> Regards <p> </html>'
# Turn on LED once sensor exceeds threshold resistance
threshold = 10
grovepi.pinMode(light_sensor,"INPUT")

grovepi.pinMode(tableLightled,"OUTPUT")
grovepi.pinMode(normalLightLed,"OUTPUT")
GPIO.setup(brightnessControlLed,GPIO.OUT)
GPIO.output(brightnessControlLed,GPIO.LOW)
breathingEffect = GPIO.PWM(brightnessControlLed,1000)
breathingEffect.start(0)
brightness = 1
labels = [
    '0','1', '2', '3', '4',
    '5', '6', '7', '8',
    '9', '10', '11', '12',
    '13', '14'
]

labels_week = [
   '0','1', '2', '3', '4',
    '5', '6', '7', '8',
    '9', '10', '11', '12',
    '13', '14' 
]


weekly_report_labels = [
   'Mon','Tue', 'Wed', 'Thur', 'Fri',
    'Sat', 'Sun'
]

colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]

# /***************************************
#  *  END OF CONSTANTS DECLARATION
#  ****************************************/
