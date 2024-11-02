from flask import Blueprint, render_template, request, redirect, url_for, session, make_response
import json

questController = Blueprint("questoes", __name__)

@questController.route("/")
def index():
    return render_template("index.html")

@questController.route("/verifica", methods=["POST"])
def verifica():
    nome = request.form.get("Nome")
    email = request.form.get("E-mail")
    session["email"] = email
    session["nome"] = nome
    return redirect(url_for("questoes.questionario"))

@questController.route("/questionario")
def questionario():
    shopping_cart = request.cookies.get("shopping_cart")
    if shopping_cart:
        cart = json.loads(shopping_cart)
    else:
        cart = []
    return render_template("questionario.html", cart=cart)

@questController.route("/logout")
def logout():
    session.pop("email", None)
    session.pop("nome", None)
    return redirect(url_for("questoes.index"))

@questController.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    item = request.form.get("item")
    cart = request.cookies.get("shopping_cart", "[]")
    cart = json.loads(cart)
    cart.append(item)
    resp = make_response(redirect(url_for("questoes.questionario")))
    resp.set_cookie("shopping_cart", json.dumps(cart))
    return resp

@questController.route("/clear_cart")
def clear_cart():
    resp = make_response(redirect(url_for("questoes.questionario")))
    resp.set_cookie("shopping_cart", "", expires=0)
    return resp
