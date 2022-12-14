from flask import Blueprint, render_template, make_response, request, current_app, redirect, url_for, flash
import requests, json
from . import functions


main = Blueprint('main', __name__, url_prefix='/')


@main.route('/')
def home():
    api_url = f'{current_app.config["API_URL"]}/poems'
    headers = {"Content-Type": "application/json"}
    data = {}
    response = requests.get(api_url, headers=headers, json=data)
    poems = json.loads(response.text)
    print(poems)

    return render_template('home.html', poems=poems['poems'])


@main.route('/login', methods=['GET', 'POST'])
def login():
    jwt = functions.get_jwt()
    if jwt:
        return redirect(url_for('main.home'))
    else:
        if request.method == 'GET':
            jwt = functions.get_jwt()
            api_url = f'{current_app.config["API_URL"]}/auth/login/request.cookies.get("id")'
            headers = functions.get_headers()
        if (request.method == 'POST'):
            email = request.form['email']
            password = request.form['password']
            if email != None and password != None:
                response = functions.login(email, password)
                print("login", response)
                if (response.ok):
                    response = json.loads(response.text)
                    token = response["access_token"]
                    user_id = str(response["id"])
                    response = make_response(redirect(url_for('main.home')))
                    response.set_cookie("access_token", token)
                    response.set_cookie("id", user_id)

                    return response
            return (render_template('login.html', error="Usuario o contraseña incorrectos"))
        else:
            return render_template('login.html')


@main.route("/logout")
def logout():
    resp = make_response(redirect(url_for("main.home")))
    resp.delete_cookie("access_token")
    resp.delete_cookie("id")
    return resp


@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        role = 'poet'
        if name != "" and email != "" and password != "":
            api_url = f'{current_app.config["API_URL"]}auth/register'
            print(api_url)
            data = {"name": name, "email": email, "password": password, "rol": role}
            headers = {"Content-Type": "application/json"}
            response = requests.post(api_url, json=data, headers=headers)
            if response.ok:
                return redirect(url_for("main.login"))
            else:
                return render_template("register.html")
        else:
            return render_template("register.html")
    else:
        return render_template("register.html")

