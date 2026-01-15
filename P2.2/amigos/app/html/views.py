from flask import render_template, redirect, url_for
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
