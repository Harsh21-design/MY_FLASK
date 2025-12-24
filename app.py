# MYTODO APP

from flask import Flask
from flask import render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = "supersecret123"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return f"{self.sno}-{self.title}"

# home page - dashboard
@app.route("/")
def home():
    return render_template("home.html")

# Login page
@app.route("/login",methods=["GET","POST"])
def mytodologin():
    if request.method=="POST":
        username = request.form.get('username')
        password = request.form['password']
        if username == 'admin' and password == "11223344":
            session['user'] = username
            session['password'] = password
            return render_template("index.html")
        else:
            return jsonify({"Message":"Error! Please Enter Correct Credential to Login MyTodo App!!"})
    
    return render_template("login.html")

# Registration Page
@app.route("/register",methods=["GET","POST"])
def mytodoregister():
    if request.method=="POST":
        return ""
    return "Coming Soon!"


# Add a todo and view all todos
@app.route("/mytodo",methods=["GET","POST"])
def mytodo():
    if ("user" and "password" in session):
        if request.method=="POST":
            title = request.form['title']
            desc = request.form['desc']
            todo = Todo(title=title,desc=desc)
            db.session.add(todo)
            db.session.commit()
        
        allTodo = Todo.query.all()
    
        return render_template("index.html",allTodo=allTodo) #rendering from templates/base.html
    return jsonify({"Message":"Error! Please Enter Correct Credential to Login MyTodo App!!"})

# update a todo
@app.route('/update/<int:sno>',methods=['GET','POST'])
def mytodoupdate(sno):
    if ("user" and "password" in session) and request.method=="POST":
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/mytodo")
    
    todo = Todo.query.filter_by(sno=sno).first()   
    return render_template("update.html",todo=todo)

# delete a todo
@app.route('/delete/<int:sno>',methods=['GET','POST'])
def mytododelete(sno):
    if ("user" and "password" in session): 
        todo = Todo.query.filter_by(sno=sno).first()
        db.session.delete(todo)
        db.session.commit()
        return redirect("/mytodo")
    
# #Logout Page
@app.route("/logout",methods=["GET","POST"])
def mytodologout():
    if request.method == "POST":
        session.pop("password",None)
        session.pop("user",None)
        return redirect(url_for("mytodologin"))

if __name__ == "__main__":
    app.run(debug=True)  #port=8000
