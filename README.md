# Smart-Restaurant-System
An IoT system which monitors energy consumption controls lightings, appliances using GUI based on flask server (backend)

Introduction: -

This project has 2 independent devices i.e Smart Door device(offline) and Smartlighting  device(online)  implemented  on  different  hardwares.
Smart  door  device detects door movements,restaurant owner/customer and reminds about key/belongingsto the user.
The Smart lighting device enables user to control all lighting,appliances and monitors energy consumption,average cost of energy consumed per day and
gets notified about energy bill via Amazon Email service.Smart lighting Device uses Amazon Alexa and AI planner for turning ON central(main) lights.
Additionally smart assistance feature is also implemented in case if user forgets to turn off appliance.
Lastly on behalf of smart lighting device user can send panic notificationto concerned authority in case of emergency/locked out situation.

For buisness logic have a look at app/api/device/controller.py file

Run codes present in "Al_Planning and Arduino_ESP codes" folder on respective hardware ( e.g run Smart Door.ino on arduino uno and Alexa_ESP8266_mqtt.ino on ESP8266 microcontroller)
Run AI planning files( problem.pddl,domain.ppdl,planning.py )either on laoptop or raspberry pi

Execution -

1.clone this repository on raspberry pi file system
2. Install all dependancies
3. Run python server file with IP address of broker as a commnad line parameter (e.g python server.py 192.168.0.110)
4. Hit e.g http://192.168.0.110:7000/control-panel/ in the web browser




