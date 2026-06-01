from app import db

class Amigo(db.Model):
    """
    Definición de la tabla 'amigos' de la base de datos
    """

    __tablename__ = "amigos"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    longi = db.Column(db.String(32))
    lati = db.Column(db.String(32))
    device = db.Column(db.Text(), default="")

    def __repr__(self):
        return "<Amigo[{}]: {}>".format(self.id, self.name)

def get_all_devices():
    amigos = Amigo.query.filter(Amigo.device != None, Amigo.device != "").all()
    return [a.device for a in amigos]
