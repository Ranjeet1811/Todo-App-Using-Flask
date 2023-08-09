from flask import Flask,render_template,redirect,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:ranjeet@localhost/python"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    sno= db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(200),nullable = False)
    desc = db.Column(db.String(500),nullable = False)
    date = db.Column(db.DateTime,default = datetime.now())

    def __repr__(self):
        return f"{self.sno} -{self.titile}"
    
@app.route('/',methods =['GET','POST'])
def index():
    if request.method =='POST':
        title = request.form["title"]
        desc = request.form['desc']
        todo = Todo(title=title,desc = desc)
        db.session.add(todo)
        db.session.commit()
        # return("data store in db")
    allTodo = Todo.query.all()
    return render_template('index.html',allTodo = allTodo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno = sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')


@app.route('/update/<int:sno>',methods = ['GET','POST'])
def update(sno):
    if request.method=='POST':
        title = request.form["title"]
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno = sno).first()
        todo.title = title
        todo.desc= desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo = Todo.query.filter_by(sno = sno).first()
    return render_template('update.html',todo = todo)


if __name__ == "__main__":
    app.run(debug = True)