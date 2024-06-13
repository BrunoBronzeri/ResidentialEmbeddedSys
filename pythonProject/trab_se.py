from flask import Flask, render_template, redirect, request, url_for, Response
# from gpiozero import LED
from time import sleep
import cv2

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/hello')
def say_hello():
    return "Hello world!"

@app.route('/bbb1')
def teste():
    led = LED(17)

    while True:
        led.on()
        sleep(1)
        led.off()
        sleep(1)

@app.route('/ledon', methods=["POST", "GET"])
def led_on():
    
    if request.method == "POST":
        valor = request.form["nm"]
        if valor == "ON":
            return redirect(url_for("teste"))
        elif valor == "OFF":
            return redirect(url_for("teste"))
    else:
        return render_template("ligabutao.html")
    
@app.route('/led')
def led():
    return render_template("index.html")

def gen_frames():
    cap = cv2.VideoCapture(0)  # Captura do dispositivo de vídeo 0 (normalmente a webcam)
    while True:
        success, frame = cap.read()  # Ler o quadro da webcam
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # Concatena os bytes para formar a resposta HTTP correta

@app.route('/cam')
def index():
    return render_template('camera.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True, port = 5001, host="0.0.0.0")
