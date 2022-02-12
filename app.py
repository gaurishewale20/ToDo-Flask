import sqlite3
from flask import Flask,render_template,request,redirect
from flask_sqlalchemy  import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todos.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ToDo(db.Model):
    srno = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(300),nullable=False)
    desc = db.Column(db.String(500),nullable=False)
    date_created = db.Column(db.DateTime,default=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"{self.srno}-{self.title}"



@app.route('/',methods=['GET','POST'])
def home():
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = ToDo(title = title,desc =desc)
        db.session.add(todo)
        db.session.commit()
    allToDos = ToDo.query.all()

    return render_template('index.html',allToDos=allToDos)


@app.route('/edit/<int:srno>',methods=['GET','POST'])
def edit(srno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        toDo = ToDo.query.filter_by(srno=srno).first()
        toDo.title = title
        toDo.desc = desc
        db.session.commit()
        return redirect("/")

    todo = ToDo.query.filter_by(srno=srno).first()
    return render_template('edit.html',todo=todo)


@app.route('/delete/<int:srno>')
def delete(srno):
    toDo = ToDo.query.filter_by(srno=srno).first()
    db.session.delete(toDo)
    db.session.commit()
    return redirect("/")



if __name__ == '__main__':
    app.run(debug=True)