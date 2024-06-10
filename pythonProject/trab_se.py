from flask import Flask,render_template, redirect, request, url_for
from gpiozero import LED
from time import sleep
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

if __name__ == "__main__":
    app.run(debug=True, port = 5001, host="0.0.0.0")
