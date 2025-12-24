from flask import Flask, request
from flask import Response, redirect, url_for, session
from flask import render_template

login_app = Flask(__name__)
login_app.secret_key = "supersecret" #use session to locked (mandatory for session used in flask)


# route page
@login_app.route("/")
def route_to_login():
    return redirect(url_for("login_page"))

#Login Page
@login_app.route("/login",methods=["GET","POST"])
def login_page():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == 'admin' and password == "12345678":
            session['user'] = username # user details stores in session
            return redirect(url_for("welcome"))
        else:
            return Response("Invalid Credential! Try Again", mimetype="text/plain")
        
    return '''
    <h2>Login Page</h2>
    <form method="POST">
    Username : <input type = "text" name="username"><br>
    Password : <input type = "text" name="password"><br>
    <input type = "submit" value = "Login">
    </form>

    # '''
    # return render_template("login.html")
        
#WELCOME - home page(After Login Page)
@login_app.route("/welcome")
def welcome():
    if "user" in session:
        return f'''
        <h2>Welcome {session["user"]}!</h2>
        <a href={url_for("logout_page")}>Logout</a> 
    '''
    return redirect(url_for("login"))

#Logout Page
@login_app.route("/logout")
def logout_page():
    session.pop("user",None)
    return redirect(url_for("login_page"))


if __name__ == "__main__":
    login_app.run(debug=True) 