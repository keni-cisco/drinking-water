# drinking-water
Importación de módulos y bibliotecas:

machine: Este módulo proporciona una API para interactuar con el hardware de la placa, como pines GPIO, ADC y PWM.
utime: Proporciona funciones para medir el tiempo y hacer pausas en el código.
Pin: Permite controlar los pines GPIO de la placa.
ADC: Facilita la lectura de valores analógicos a digitales.
SoftI2C: Implementa la comunicación I2C por software.
PWM: Permite generar señales PWM para controlar dispositivos como motores y servos.
HCSR04: Es una biblioteca para el sensor de ultrasonido que simplifica la medición de distancias.
lcd_api, i2c_lcd: Son bibliotecas para controlar una pantalla LCD mediante la interfaz I2C.
ujson: Proporciona funciones para codificar y decodificar datos en formato JSON.
MQTTClient de umqtt.simple: Ofrece una implementación simple de cliente MQTT para la publicación y suscripción a temas MQTT.
network: Permite la configuración y gestión de conexiones de red.
time: Proporciona funciones relacionadas con la gestión del tiempo.
urequests: Permite realizar solicitudes HTTP de manera simplificada.
Inicialización de hardware:

Se instancia el sensor de ultrasonido (HCSR04) con pines específicos para el disparo y la recepción de señales ultrasónicas.
Se configuran dos pines GPIO como entradas analógicas (ADC) para leer los valores de los sensores TDS.
Se establece la comunicación I2C (SoftI2C) para controlar el LCD, definiendo la dirección del dispositivo (I2C_ADDR), el número de filas y columnas de la pantalla.
Se configuran dos pines GPIO como salidas digitales para controlar los LEDs de almacenamiento.
Se configura un pin GPIO para generar señales PWM y controlar el servo motor.
Funciones útiles:

map_servo(x): Esta función mapea un valor de entrada al rango de pulsos PWM necesario para controlar la posición del servo motor.
Conexión WiFi:

La función conectaWifi(red, password) intenta conectar el dispositivo a una red WiFi especificada. Utiliza la interfaz STA_IF de la clase network.WLAN para realizar la conexión.
Conexión MQTT:

Se define el ID del cliente MQTT, la dirección del broker MQTT, así como las credenciales de usuario y contraseña.
Se intenta conectar al servidor MQTT utilizando el cliente MQTT proporcionado por umqtt.simple.
Bucle principal:

Dentro del bucle principal, se realizan las siguientes tareas:
Lectura de valores analógicos de los sensores TDS y conversión a unidades adecuadas (voltaje y partes por millón, respectivamente).
Lectura de la distancia del sensor de ultrasonido y cálculo del nivel de almacenamiento en base a esa distancia.
Control de los LEDs y del servo motor en función del nivel de almacenamiento.
Visualización de los datos en el LCD.
Publicación de los datos recopilados en un tema MQTT.
Manejo de errores:

Si la conexión a la red WiFi falla, se imprime un mensaje indicando que la conexión no fue posible. Esto se hace después de intentar conectarse durante un período de tiempo limitado
https://mail.google.com/mail/u/0?ui=2&ik=b18f381767&attid=0.1&permmsgid=msg-a:r-8732520721476933924&th=18fbf53d8e64d37b&view=fimg&fur=ip&sz=s0-l75-ft&attbid=ANGjdJ-nkk8uo2NJafOgNOBmOfpNKrbz9YvphQXkW-NroU6wQ5hRDTi5-hVXgmN9ItKegUWsdNHLXohPhogjX-O0CjPtsEhjGVJy52Bf5PnW2lrf_FLvB0wlQKruRKo&disp=emb&realattid=ii_lwqf21i70
