from flask import Flask, render_template, redirect, request, url_for, Response, jsonify

# BROKENzinho
# from gpiozero.pins.pigpio import PiGPIOFactory
# from gpiozero import LED, AngularServo, Servo
# BROKENZINHO

# import RPi.GPIO as GPIO

from time import sleep
import cv2 #importa o cv2, ás vezes
from datetime import datetime
import requests

import pytz

API_KEY = '1fd96af488c1e2f6bbc5b108b952ee7c' # Define personal key for API
CITY = 'Blumenau' # City name to be searched through API

#--------------------------------
servo_pin = 18

# myFactory = PiGPIOFactory()
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(servo_pin, GPIO.OUT)
# GPIO.setup(27,GPIO.OUT)

# PWM config
# pwm = GPIO.PWM(servo_pin, 50)
# pwm.start(0)
#-------------------------------

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# myServo = Servo(servo_pin, min_pulse_width = 0.05/100, max_pulse_width = 2.5/1000, pin_factory = myFactory)

angulo_inicial = 0
angulo_objetivo = 180

# ------------------------------------------------ FUNCTIONS ------------------------------------------------------------
## FUNCTION TO AQUIRE TIME AND WEATHER INFO -----------------------------------------------------------------------------
def say_hello():
    
    current_time = datetime.now().strftime("%H:%M") # Timetable acquisition

    # --------------- To know if it's day or night ------------------
    # Converter a hora atual em um objeto datetime para comparação
    current_hour = datetime.now().hour

    # Definir os períodos do dia e da noite
    if 6 <= current_hour < 18:
        day_night = "dia"
    else:
        day_night = "noite"
    # ---------------------------------------------------------------

    # Acquiring weather via API via weather forecast API URL
    url = f'http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric&lang=pt_br'
    
    # Make the request to the API
    response = requests.get(url)
    weather_data = response.json()
    
    # Extract the relevant data
    if weather_data["cod"] == 200:
        temperature = int(weather_data["main"]["temp"])
        description = weather_data["weather"][0]["description"]
        humidity = weather_data["main"]["humidity"]
        city = weather_data["name"]
        country = weather_data["sys"]["country"]
        weather_data = {
            "temperature": temperature,
            "description": description,
            "city": city
        }
    else:
        weather_info = None

    return current_time, weather_data, description, humidity, country
#--------------------------------------------------------------------------------------------------------
def say_hello1(CITY):
    
    current_time = datetime.now().strftime("%H:%M") # Timetable acquisition

    # --------------- To know if it's day or night ------------------
    # Converter a hora atual em um objeto datetime para comparação
    current_hour = datetime.now().hour

    # Definir os períodos do dia e da noite
    if 6 <= current_hour < 18:
        day_night = "dia"
    else:
        day_night = "noite"
    # ---------------------------------------------------------------

    # Acquiring weather via API via weather forecast API URL
    url = f'http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric&lang=pt_br'
    
    # Make the request to the API
    response = requests.get(url)
    weather_data = response.json()
    
    # Extraindo os dados relevantes da resposta JSON
    if weather_data["cod"] == 200:
        temperature = int(weather_data["main"]["temp"])
        city = weather_data["name"]
        feels_like = weather_data["main"]["feels_like"]
        temp_min = weather_data["main"]["temp_min"]
        temp_max = weather_data["main"]["temp_max"]
        pressure = weather_data["main"]["pressure"]
        humidity = weather_data["main"]["humidity"]
        description = weather_data["weather"][0]["description"]
        wind_speed = weather_data["wind"]["speed"]
        sunrise_timestamp = weather_data["sys"]["sunrise"]
        sunset_timestamp = weather_data["sys"]["sunset"]
                
        # Convertendo timestamps de nascer e pôr do sol para horário local
        timezone = pytz.timezone('America/Sao_Paulo')
        sunrise = datetime.fromtimestamp(sunrise_timestamp, tz=timezone).strftime('%H:%M')
        sunset = datetime.fromtimestamp(sunset_timestamp, tz=timezone).strftime('%H:%M')

    else:
        error_message = f'Erro ao obter dados: {weather_data["message"]}'

    weather_info = {
            "temperature": temperature,
            "description": description,
            "city": city,
            "feels": feels_like,
            "min": temp_min,
            "max": temp_max,
            "pressure": pressure,
            "wind": wind_speed,
            "humidity": humidity,
            "sunrise": sunrise,
            "sunset": sunset,
    }

    return weather_info, temperature, feels_like, temp_min, temp_max, pressure, humidity, description, wind_speed, sunrise, sunset, current_time

## FUNCTION TO MOVE SERVO--------------------------------------------------------------------------------
def move(angle):
    mini = 2
    maxi = 12
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servo_pin, GPIO.OUT)

    duty = mini + (angle / 180)*(maxi-mini)
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(servo_pin, False)
    pwm.ChangeDutyCycle(0)
#     myServo.value = 0
    
    return jsonify({"status": "success", "angle": angle})
    
## FUNCTION TO SMOOTH SERVO'S MOVEMENT
def suave(start, end, step=1, delay=0.02):
    if start<end:
        for angle in range(start, end, step):
            move(angle)
            sleep(delay)
    else:
        for angle in range(start, end,-step):
            move(angle)
            sleep(delay)

## FUNCTION TO GENERATE CAMREA FRAMES-------------------------------------------------------------------------------------
def gen_frames():
   # pipeline = "v4l2src device = /dev/vide0 ! videoconvert ! appsink"
    cap = cv2.VideoCapture(0)  # Capture from video device 0 (typically the webcam)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
    while True:
        success, frame = cap.read()  # Read the webcam frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                    # Concatenates the bytes to form the correct HTTP response

# ------------------------------------------------ MAIN -----------------------------------------------------------------

@app.route('/main')
def main():
    [current_time, weather_data, description, humidity, country] = say_hello()
    return render_template("main.html", current_time=current_time, weather_data=weather_data, description=description)

# ------------------------------------------------- LED -----------------------------------------------------------------
@app.route('/state')
def manipulando(valor):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(27,GPIO.OUT)
    if valor == "on":
        print(valor)
        print("ligando led")
        GPIO.output(27,GPIO.HIGH)
        return 0

    elif valor == "off":
        print(valor)
        print("deligando led")
        GPIO.output(27,GPIO.LOW)
        GPIO.cleanup()
        return 0

        
@app.route('/ledon', methods=["POST", "GET"])
def led_on():
    [current_time, weather_data, description, humidity, country] = say_hello()
    
    if request.method == "POST":
        valor = request.form.get("nm")
        if valor == "on":
            manipulando(valor)
            return jsonify({"status": "success", "message": "LED is now ON"})
        elif valor == "off":
            manipulando(valor)
            return jsonify({"status": "success", "message": "LED is now OFF"})
    else:
        return render_template("ligabutao.html", current_time=current_time, weather_data=weather_data, description=description)

# ------------------------------------------------- LIGHT ----------------------------------------------------------------

@app.route('/luz')
def luz():
    [current_time, weather_data, description, humidity, country] = say_hello()
    return render_template("led_on.html", current_time=current_time, weather_data=weather_data, description=description)

# ------------------------------------------------- TEMP ------------------------------------------------------------------

@app.route('/temp', methods=['GET', 'POST'])
def temp():
    [current_time, weather_data, description, humidity, country] = say_hello()
    city = CITY
    if request.method == 'POST':
        city = request.form.get('city')
        print(city)
    [weather_info, temperature, feels_like, temp_min, temp_max, pressure, humidity, description, wind_speed, sunrise, sunset, current_time] = say_hello1(city)
    return render_template("temp.html", weather_data=weather_data, weather_info=weather_info, temperature=temperature, feels_like=feels_like, temp_min=temp_min, temp_max=temp_max, pressure=pressure, humidity=humidity, description=description, wind_speed=wind_speed, sunrise=sunrise, sunset=sunset, current_time=current_time)


# ------------------------------------------------- CAM -------------------------------------------------------------------
@app.route('/cam', methods=['GET','POST']) # Não mexa -> horas gastas = 7.5
def cam_on():
    global angulo_inicial, angulo_objetivo
    if request.method == 'GET':
        [current_time, weather_data, description, humidity, country] = say_hello()
        return render_template('camera.html', current_time=current_time, weather_data=weather_data, description=description)
    else:
        [current_time, weather_data, description, humidity, country] = say_hello()
        angle = request.form['angle']
        angle = int(angle)
#         angulo_objetivo = angle
#         suave(angulo_inicial, angulo_objetivo)
#         angulo_inicial = angulo_objetivo
        move(angle)
        return render_template('camera.html', current_time=current_time, weather_data=weather_data, description=description)
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# ------------------------------------------------- HOST -------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True, port = 5001, host="0.0.0.0")
