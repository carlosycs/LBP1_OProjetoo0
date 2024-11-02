from flask import Flask, render_template, session, redirect, url_for, request, make_response
from controllers.questController import questController
import json

app = Flask(__name__)
app.secret_key = "chavesecreta123"

app.register_blueprint(questController)

@app.route("/")
def hello_world():
    return render_template("index.html")

rotas_publicas = ["questoes.index", "questoes.verifica"]

@app.before_request
def verificarIdentifica():
    if request.endpoint in rotas_publicas:
        return

    if "email" in session:
        return 
    return redirect(url_for("questoes.index"))

@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    item = request.form.get("item")
    cart = request.cookies.get("shopping_cart", "[]")
    cart = json.loads(cart)

    cart.append(item)
    
    resp = make_response(redirect(url_for("questoes.questionario")))
    resp.set_cookie("shopping_cart", json.dumps(cart))
    return resp

if __name__ == "__main__":
    app.run(debug=True)
