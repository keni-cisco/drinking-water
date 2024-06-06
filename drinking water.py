from machine import Pin, ADC, SoftI2C, PWM
from utime import sleep, sleep_ms
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
from hcsr04 import HCSR04
import ujson
from umqtt.simple import MQTTClient
import network, time, urequests

#Ultra Sonido
sensor = HCSR04(trigger_pin = 4, echo_pin = 5)

#Sensor TDS
adc = ADC(Pin(34))
tds = ADC(Pin(35))
#LCD con I2C
I2C_ADDR = 0x27
totalRows = 4
totalColumns = 16
i2c = SoftI2C (scl = Pin(22), sda = Pin(21), freq = 20000)
lcd = I2cLcd (i2c, I2C_ADDR, totalRows, totalColumns)

#Leds de Almacenamiento
ledv = Pin(25, Pin.OUT)
ledr = Pin(23, Pin.OUT)

#Servo motor
servo = PWM(Pin(32), freq = 50)

def map_servo(x):
   
    return int((x - 0) * (125 - 25) / (100 - 0) + 25)

angulos = [0 , 45, 90, 125, 180]



# MQTT Servidor Parametros
MQTT_CLIENT_ID = "fghfgbhgfhvnhgvbnmgfbngv"
MQTT_BROKER    = "broker.hivemq.com"
MQTT_USER      = ""
MQTT_PASSWORD  = ""
MQTT_TOPIC     = "yulius/0806/"

def conectaWifi (red, password):
      global miRed
      miRed = network.WLAN(network.STA_IF)    
      if not miRed.isconnected():              #Si no está conectado…
          miRed.active(True)                   #activa la interface
          miRed.connect(red, password)         #Intenta conectar con la red
          print('Conectando a la red', red +"…")
          timeout = time.time ()
          while not miRed.isconnected():           #Mientras no se conecte..
              if (time.ticks_diff (time.time (), timeout) > 10):
                  return False
      return True


if conectaWifi ("Xperia L1_6bd9", "SAMUELPALACIOS"):

    print ("Conexión exitosa!")
    print('Datos de la red (IP/netmask/gw/DNS):', miRed.ifconfig())


    print("Conectando a  MQTT server... ",MQTT_BROKER,"...", end="")
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, user=MQTT_USER, password=MQTT_PASSWORD)
    client.connect()

    print("Conectado!")

    nuevo_dato = ""



    while True:
   
        vol = adc.read()
        sensor_vol = (vol * 9)/ 65356
        print("V:",sensor_vol,"v")
        sleep_ms(1)
       
        #Sensor TDS
        tdss = tds.read()
        sensor_tdss = (tdss / 4095) * 1000
        print("TDS:",sensor_tdss,"ppm")
        sleep_ms(1)
   
        #Sensor de Ultrasonido
        distancia = sensor.distance_cm()
        sensor_ultra = (distancia / 35) * 100
        print("Alm:", sensor_ultra, "%")
        sleep_ms(50)
   
        #Leds de Almacenamiento y Servo Motor
        if sensor_ultra <80:
            ledv.on()
            ledr.off()
            m = map_servo(0)
            servo.duty(m)  
        else:
            ledv.off()
            ledr.on()
            m = map_servo(90)
            servo.duty(m)
       
        #LCD con I2C
        lcd.putstr('   * DATOS *    TDS:{:.2f} ppm      Alm:{:.0f}%        Volt:{:.0f}'.format(sensor_tdss,sensor_ultra,sensor_vol))
        sleep(0.75)
        lcd.clear()
        sleep_ms(50)
   
   
        print("Revisando Condiciones ...... ")
        message = ujson.dumps({
        "TDS": sensor_tdss,
        "Alm": sensor_ultra,
        "V": sensor_vol,
        })
       
        print("Reportando a  MQTT topic {}: {}".format(MQTT_TOPIC, message))
        client.publish(MQTT_TOPIC, message)

else:
       print ("Imposible conectar")
       miRed.active (False)
