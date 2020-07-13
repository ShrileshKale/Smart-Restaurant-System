# Smart-Restaurant-System
An IoT system which monitors energy consumption controls lightings, appliances using GUI based on flask server (backend)

For buisness logic have a look at app/api/devices/controller.py file

Introduction: -

This project has two independent devices, an offline device called as Smart Door based on Arduino Uno  and another online device as Smart lighting imple- mented on RPi , these are implemented on different hardware platforms. The Smart Door device detects door movements, restaurant owner/customer and reminds about key/belongings to the user respectively. The Smart Lighting de- vice enables user to control all lighting and appliances to monitor the energy consumption, then, average cost of energy consumed per day is calculated and notified to the user via Amazon Email services . Smart Lighting device uses Amazon Alexa and AI planner  for turning ON central(main) lighting in the restaurant. Additionally, a smart safety assistance feature is added in case the user forgets to turn off appliance. Lastly, Smart Lighting device can send panic notification to concerned authorities on behalf of user in case of emer- gency/locked out situation.

Run codes present in "Al_Planning and Arduino_ESP codes" folder on respective hardware ( e.g run Smart Door.ino on arduino uno and Alexa_ESP8266_mqtt.ino on ESP8266 microcontroller)
Run AI planning files( problem.pddl,domain.ppdl,planning.py )either on laoptop or raspberry pi

Execution -

1.clone this repository on raspberry pi file system
2. Install all dependancies
3. Run python server file with IP address of broker as a commnad line parameter (e.g python server.py 192.168.0.110)
4. Hit e.g http://192.168.0.110:7000/control-panel/ in the web browser




