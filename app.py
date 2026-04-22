from flask import Flask, render_template, redirect, request
import sqlite3

app = Flask(__name__)

def init_database():
    conn = sqlite3.connect("citas.db")
    
    conn.execute(
        """
        create table if not exists pacientes(
            id integer PRIMARY KEY AUTOINCREMENT,
            mascota text not null,
            propietario text not null,
            especie text not null,
            fecha text not null
        );
        """
    )
    conn.commit()
    conn.close()
    
    
init_database()


@app.route("/")
def index():
    conn = sqlite3.connect("citas.db")
    conn.row_factory = sqlite3.Row
    
    cursor = conn.cursor()
    cursor.execute("select * from pacientes")
    pacientes = cursor.fetchall()
    
    return render_template('index.html', pacientes = pacientes)


@app.route("/crear")
def crear():
    return render_template('crear.html')

@app.route("/agendar", methods = ['POST'])
def agentar_citas():
    mascota = request.form['mascota']
    propietario = request.form['propietario']
    especie = request.form['especie']
    fecha = request.form['fecha']
    
    conn = sqlite3.connect("citas.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        insert into pacientes (mascota, propietario, especie, fecha)
        values (?,?,?,?)
        """,(mascota,propietario,especie,fecha)
    ) 
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/eliminar/<int:id>")
def cancelar_cita(id):
    conn = sqlite3.connect("citas.db")
    cursor = conn.cursor()
    cursor.execute("delete from pacientes where id = ?",(id,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/editar/<int:id>")
def editar_cita(id):
    conn = sqlite3.connect("citas.db")
    conn.row_factory = sqlite3.Row
    
    cursor = conn.cursor()
    
    cursor.execute("select * from pacientes where id = ?",(id,))
    paciente = cursor.fetchone()
    conn.close()
    return render_template("editar.html", paciente = paciente)

@app.route("/edicion", methods = ['POST'])
def edicion():
    id = request.form['id']
    mascota = request.form['mascota']
    propietario = request.form['propietario']
    especie = request.form['especie']
    fecha = request.form['fecha']
    
    conn = sqlite3.connect("citas.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        update pacientes set mascota=?,propietario=?,
        especie=?,fecha=? where id=?
        """,(mascota,propietario,especie,fecha,id)
    )
    conn.commit()
    conn.close()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)