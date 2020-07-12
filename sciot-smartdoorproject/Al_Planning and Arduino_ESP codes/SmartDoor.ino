/*******************************************************************************
                              Includes
*******************************************************************************/
#include "I2Cdev.h"                           // I2C Library
#include "SPI.h"                              // SPI library
#include "MFRC522.h"                          // RFID library
#include "MPU6050.h"                          // GrovePi IMU9D0F Library
#include "rgb_lcd.h"                          // GrovePi RGB LCD Library
#include "Wire.h"   

/*******************************************************************************
                              Defines
*******************************************************************************/
#define buzzer            4
#define MaxThreshold      359
#define MaxTiltThreshold  359
#define sample_num_mdate  5000
#define triggerPin        7
#define echoPin           8
#define pinRST            9
#define pinSDA            10
#define doorlockPin       6

/*******************************************************************************
                            Global Variables
*******************************************************************************/
bool flag = true;
int getDistanceInches = 0;
uint8_t buffer_m[6];
int16_t ax, ay, az;
int16_t gx, gy, gz;
int16_t   mx, my, mz;
float refhead;
float reftilthead;
float heading;
float tiltheading;
float Axyz[3];
float Gxyz[3];
float Mxyz[3];

MPU6050 accelgyro;
I2Cdev   I2C_M;
rgb_lcd rgblcd;
MFRC522 mfrc522(pinSDA, pinRST);             // Set up mfrc522 on the Arduino


/*******************************************************************************
* Function Name : setup  
* Description   : This function will Initialize and set up all the sensors, 
*                 actuators and display configuration
* Input         : NA
* Output        : NA
* Return        : NA
*******************************************************************************/
void setup()
{
  Serial.begin(9600);                       // Initialize Serial Monitor at 9600 baud rate
  Wire.begin();                             // Initialize Wire Connection
  pinMode(buzzer, OUTPUT);                  // Set Buzzer as Output at Pin D4 on GrovePi
  pinMode(echoPin, INPUT);                  // Set Ultrasonic's Echopin as Input at Pin 7 on Uno
  pinMode(triggerPin, OUTPUT);              // Set Ultrasonic's Triggerpin as Output at Pin 8 on Uno
  pinMode(doorlockPin, OUTPUT);             // Set Door Locked Indication as Output at Pin 6 on Uno
  SPI.begin();                              // Initialize SPI Connection
  mfrc522.PCD_Init();                       // Initialize Proximity Coupling Device(PCD) for MFRC522 Sensor(RFID)
  rgblcd.begin(16, 2);                      // Initialize LCD Connection
  rgblcd.setRGB(255, 0, 0);                 // Set LCD backlight color to RED
  accelgyro.initialize();                   // Initialize IMU9D0F Sensor
  delay(1000);                              // Delay required to set up IMU9D0F sensor
  getAccel_Data();                          // Get Initial details about the Door state              
  getGyro_Data();
  getCompass_Data();
  refhead = getHeading();                   // Take Initial Door state as Reference for head reading
  reftilthead = getTiltHeading();           // Take Initial Door state as Reference for tilt head reading
}

/*******************************************************************************
* Function Name : loop  
* Description   : This function will execute indefinitely. Reads the sensor data 
*                 and does the Smart Door operation accordingly            
* Input         : NA
* Output        : NA
* Return        : NA
*******************************************************************************/
void loop()
{
  getDistanceInches = ((0.01723 * readUltrasonicDistance()) / 2.54);  // Get distance from Ultrasonic sensor

  if (getDistanceInches <= 15)                        // If distance detected is <= 15 inches
  {
    int i = 3;
    bool Door_Locked_Status = 0;
    bool RFID_Read_flag = 0;
    digitalWrite(doorlockPin, LOW);                   // LED OFF to show door not locked
    rgblcd.clear();
    rgblcd.setRGB(0, 128, 127);
    rgblcd.print("Person Near Door");                 // Display "Person Near Door" on LCD
    delay(1000);

    rgblcd.clear();
    rgblcd.setRGB(100, 65, 100);
    rgblcd.print("If Owner Scan");                   
    rgblcd.setCursor(0, 1);
    rgblcd.print("the Tag in");
    while(i>0)                                        // Wait for i secs for the RFID tag scan if Owner
    {
      i--;
      delay(1000);
      rgblcd.setCursor(11, 1);
      rgblcd.print(i);
      rgblcd.print(" Sec");

      if (mfrc522.PICC_IsNewCardPresent())            // If RFID tag is present
      {
        RFID_Read_flag = 1;                           // Set RFID_Read_flag and break the while loop
        break;
      }
      else
      {
        RFID_Read_flag = 0;                           // Clear RFID_Read_flag
      }
    }
        
    if (RFID_Read_flag == 1)                          // If RFID_Read_flag == 1
    {
      if (mfrc522.PICC_ReadCardSerial())              // Read the RFID tag number
      {
        String uid = "";
        for (int i = 0; i < mfrc522.uid.size; i++)
        {
          Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? "0" : "");
          Serial.print(mfrc522.uid.uidByte[i], HEX);                    // Print 
          uid.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? "0" : ""));
          uid.concat(String(mfrc522.uid.uidByte[i], HEX));
        }
        uid.toUpperCase();                            // Final RFID tag number
        if (uid == "F2D36133")                        // If RFID tag number == Owner's RFID tag number
        {
          rgblcd.clear();
          rgblcd.setRGB(120, 0, 200);
          rgblcd.print("Owner Detected");             // Display "Owner Detected" on LCD 
          bool Owner = 1;
          delay(2500);
          Door_Locked_Status = getData(Owner);        // Get IMU sensor data on the door
          if (Door_Locked_Status == 1)                // If Door_Locked_Status == 1
          {
            digitalWrite(doorlockPin, HIGH);          // LED ON to show door locked
            rgblcd.clear();
            rgblcd.setRGB(0, 100, 255);
            rgblcd.print("Door Locked");              // Display "Door Locked" on LCD 
            delay(1000);
          }
        }
      }
    }
    else                                              // If RFID tag not present           
    {
      digitalWrite(doorlockPin, LOW);                 // LED OFF to show door not locked
      rgblcd.clear();
      rgblcd.setRGB(0, 0, 255);
      rgblcd.print("Customer");
      rgblcd.setCursor(0, 1);
      rgblcd.print("Detected");                       // Display "Customer Detected" on LCD 
      bool Owner = 0;
      delay(2000);
      getData(Owner);
    }

    delay(1000);
  }
  else                                                // If distance detected is > 15 inches
  {
    rgblcd.clear();
    rgblcd.setRGB(255, 0, 0);
    Buzzer(0);
    delay(500);
  }
}

/*******************************************************************************
* Function Name : getHeading  
* Description   : This function calculates heading from IMU9D0F           
* Input         : NA
* Output        : NA
* Return        : heading
*******************************************************************************/
float getHeading(void)
{
  heading = 180 * atan2(Mxyz[1], Mxyz[0]) / PI;
  if (heading < 0) heading += 360;
  return heading;
}

/*******************************************************************************
* Function Name : getTiltHeading  
* Description   : This function calculates tilt heading from IMU9D0F           
* Input         : NA
* Output        : NA
* Return        : tiltheading
*******************************************************************************/
float getTiltHeading(void)
{
  float pitch = asin(-Axyz[0]);
  float roll = asin(Axyz[1] / cos(pitch));
  float xh = Mxyz[0] * cos(pitch) + Mxyz[2] * sin(pitch);
  float yh = Mxyz[0] * sin(roll) * sin(pitch) + Mxyz[1] * cos(roll) - Mxyz[2] * sin(roll) * cos(pitch);
  float zh = -Mxyz[0] * cos(roll) * sin(pitch) + Mxyz[1] * sin(roll) + Mxyz[2] * cos(roll) * cos(pitch);
  tiltheading = 180 * atan2(yh, xh) / PI;
  if (yh < 0)    tiltheading += 360;
  return tiltheading;
}

/*******************************************************************************
* Function Name : getAccel_Data  
* Description   : This function calculates Accelerate Data from IMU9D0F           
* Input         : NA
* Output        : NA
* Return        : NA
*******************************************************************************/
void getAccel_Data(void)
{
  accelgyro.getMotion9(&ax, &ay, &az, &gx, &gy, &gz, &mx, &my, &mz);
  Axyz[0] = (double) ax / 16384;//16384  LSB/g
  Axyz[1] = (double) ay / 16384;
  Axyz[2] = (double) az / 16384;
}

/*******************************************************************************
* Function Name : getGyro_Data  
* Description   : This function calculates Gyroscope Data from IMU9D0F           
* Input         : NA
* Output        : NA
* Return        : NA
*******************************************************************************/
void getGyro_Data(void)
{
  accelgyro.getMotion9(&ax, &ay, &az, &gx, &gy, &gz, &mx, &my, &mz);
  Gxyz[0] = (double) gx * 250 / 32768;//131 LSB(��/s)
  Gxyz[1] = (double) gy * 250 / 32768;
  Gxyz[2] = (double) gz * 250 / 32768;
}

/*******************************************************************************
* Function Name : getCompass_Data  
* Description   : This function calculates Compass Data from IMU9D0F           
* Input         : NA
* Output        : NA
* Return        : NA
*******************************************************************************/
void getCompass_Data(void)
{
  I2C_M.writeByte(MPU9150_RA_MAG_ADDRESS, 0x0A, 0x01); //enable the magnetometer
  delay(10);
  I2C_M.readBytes(MPU9150_RA_MAG_ADDRESS, MPU9150_RA_MAG_XOUT_L, 6, buffer_m);
  mx = ((int16_t)(buffer_m[1]) << 8) | buffer_m[0] ;
  my = ((int16_t)(buffer_m[3]) << 8) | buffer_m[2] ;
  mz = ((int16_t)(buffer_m[5]) << 8) | buffer_m[4] ;
  Mxyz[0] = (double) mx * 4800 / 8192;
  Mxyz[1] = (double) my * 4800 / 8192;
  Mxyz[2] = (double) mz * 4800 / 8192;
}

/*******************************************************************************
* Function Name : LCD  
* Description   : This function displays data on LCD          
* Input         : NA
* Output        : NA
* Return        : NA
*******************************************************************************/
void LCD(bool On, bool Owner)
{
  if ((On == 1) && (Owner == 1))          // Display messages w.r.t to Owner
  {
    rgblcd.clear();
    rgblcd.setRGB(0, 255, 0);
    rgblcd.print("Do Not Forget");
    rgblcd.setCursor(0, 1);
    rgblcd.print("Your Keys");
  }
  else if ((On == 1) && (Owner == 0))     // Display messages w.r.t to Customer
  {
    rgblcd.clear();
    rgblcd.setRGB(255, 128, 125);
    rgblcd.print("Thank You Visit");
    rgblcd.setCursor(0, 1);
    rgblcd.print("Again");
  }
  else
  {
    rgblcd.clear();
    rgblcd.setRGB(255, 0, 0);
  }
}

/*******************************************************************************
* Function Name : Buzzer  
* Description   : This function turns on/ off the buzzer         
* Input         : NA
* Output        : NA
* Return        : NA
*******************************************************************************/
void Buzzer(bool On)
{
  if (On == 1)                    // Buzzer ON
  {
    digitalWrite(buzzer, HIGH);
    delay(3000);
    digitalWrite(buzzer, LOW);
  }
  else if (On == 0)               // Buzzer OFF
  {
    digitalWrite(buzzer, LOW);
  }
  else
  {
    // Do Nothing
  }
}

/*******************************************************************************
* Function Name : AngleData  
* Description   : This function calculates the angle from IMU9D0F Sensor         
* Input         : head, tilthead, passedOwner
* Output        : NA
* Return        : Door_Locked_flag
*******************************************************************************/
bool AngleData(float head, float tilthead, bool passedOwner) 
{
  bool Angle_Detected = 0;
  bool Door_Locked_flag = 0;
  getCompass_Data();
  if (flag == true)
  {
    while ( abs(refhead - head) > 3 || abs(reftilthead - tilthead) > 3 )
    {
      getAccel_Data();
      getGyro_Data();
      getCompass_Data();
      head = getHeading();
      tilthead = getTiltHeading();
      if (abs(refhead - head) > 3)            // If angle is > 30 deg
      {
        if (passedOwner == 1)                 // If owner == 1
        {
          LCD(1, 1);                          // Display message w.r.t to Owner
          Buzzer(1);                          // Buzzer ON
          Door_Locked_flag = 1;               // Return Door_Locked_flag to lock the door
        }
        else if (passedOwner == 0)            // If owner == 0
        {
          LCD(1, 0);                          // Display message w.r.t to Customer  
          Buzzer(1);                          // Buzzer ON
        }
        else
        {
          // Do nothing
        }
      }
      else
      {
         LCD(0, 0);                           // Display Nothing
         Buzzer(0);                           // Buzzer OFF           
      }
    }
    return Door_Locked_flag;
  }
}

/*******************************************************************************
* Function Name : getData  
* Description   : This function calculates the angle from IMU9D0F Sensor         
* Input         : passOwner
* Output        : NA
* Return        : Door_Locked_flag
*******************************************************************************/
bool getData(bool passOwner)
{
  bool Door_locked_flag = 0;
  getAccel_Data();                                    // Get Accerlerate Data
  getGyro_Data();                                     // Get Gyroscope Data
  getCompass_Data();                                  // Get Compass Data
  float currenthead = getHeading();                   // Get Heading Data    
  float currentilthead = getTiltHeading();            // Get Tilt Heading Data
  Door_locked_flag = AngleData(currenthead, currentilthead, passOwner);   // Get AngleData Data
  return Door_locked_flag;
}

/*******************************************************************************
* Function Name : readUltrasonicDistance  
* Description   : This function calculates the angle from IMU9D0F Sensor         
* Input         : NA
* Output        : NA
* Return        : echopin value 
*******************************************************************************/
long readUltrasonicDistance()
{
  digitalWrite(triggerPin, LOW);
  delayMicroseconds(2);
  digitalWrite(triggerPin, HIGH);           // Set the trigger pin to HIGH state for 10 microseconds
  delayMicroseconds(10);
  digitalWrite(triggerPin, LOW);            // Read the echo pin, and returns the sound wave travel time in microseconds
  return pulseIn(echoPin, HIGH);
}

/******************************************************************************
                      End of File
******************************************************************************/
