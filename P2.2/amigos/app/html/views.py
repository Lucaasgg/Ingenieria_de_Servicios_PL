from flask import render_template, redirect, url_for, request, abort
from . import html
from ..models import Amigo
from .. import db

@html.route("/amigos")
def tabla_amigos():
    amigos = Amigo.query.all()
    return render_template("tabla_amigos.html", amigos=amigos)

@html.route("/delete_amigo/<int:id>")
def delete_amigo(id):
    amigo = Amigo.query.get_or_404(id)
    db.session.delete(amigo)
    db.session.commit()

    return redirect(url_for("html.tabla_amigos"))
@html.route("/edit_amigo/<int:id>")
def edit_amigo(id):
    amigo = Amigo.query.get_or_404(id)
    return render_template("edit_amigo.html", amigo=amigo)

@html.route("/new_amigo/")
def new_amigo():
    return render_template("edit_amigo.html", amigo=None)

@html.route("/save_amigo", methods=["POST"])
def save_amigo():
    id = request.form.get("id")
    if id is None or id == "":
        name = request.form.get("name")
        if not name:
            abort(422)
        lati = request.form.get("lati", "0")
        longi = request.form.get("longi", "0")

        amigo = Amigo(name=name, lati=lati, longi=longi)
        db.session.add(amigo)
        db.session.commit()
    else:
        amigo = Amigo.query.get_or_404(int(id))
        name = request.form.get("name")
        if name:
            amigo.name = name
        lati = request.form.get("lati")
        if lati:
            amigo.lati = lati
        longi = request.form.get("longi")
        if longi:
            amigo.longi = longi
        db.session.commit()
    return redirect(url_for("html.tabla_amigos"))
