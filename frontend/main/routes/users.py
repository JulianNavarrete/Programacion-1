from flask import Blueprint, render_template, url_for, redirect, json, current_app, request, flash, make_response
import requests, json
from . import functions

users = Blueprint('users', __name__, url_prefix='/')


@users.route('users/my-profile')
def my_profile():
    jwt = functions.get_jwt()
    if jwt:
        user = request.cookies.get('id')
        # print("user", user)
        user_req = functions.get_user_info(user)
        user_req = json.loads(user_req.text)
        print("user_req: ",user_req)

        return render_template('user_details.html', jwt = jwt, user_req= user_req)
    else:
        return redirect(url_for('main.home'))


@users.route('users/profile', methods=['GET', 'POST'])
def modify_profile():
    jwt = request.cookies.get('access_token')
    if jwt:
        user_id = request.cookies.get('id')
        print("Asdddd")
        if request.method == 'GET':
            api_url = f'{current_app.config["API_URL"]}/user/{user_id}'
            headers = {'Content-type': 'application/json', 'Authorization': f"Bearer {jwt}"}
            response = requests.get(api_url, headers=headers)
            
            print(response)
            user = json.loads(response.text)
            print("B")
            return render_template('edit_user.html', user=user)
            
        if request.method == 'POST':
            print("Holaaaa")
            name = request.form['Name']
            print("name", name)
            password = request.form['Password']
            print("password", password)
            api_url = f'{current_app.config["API_URL"]}/users/{user_id}'
            data = {"name": name, "plain_password": password}
            headers = {'Content-type': 'application/json', 'Authorization' : f"Bearer {jwt}"}
            if name != "" and password != "":
                response = requests.put(api_url, json=data, headers=headers)
                if response.status_code == 200:
                    response = json.loads(response.text)
                    return redirect(url_for('users.my_profile'))
                else:
                    return redirect(url_for('users.my_profile'))
            
            elif name != "":
                data = {"name": name}
                response = requests.put(api_url, json=data, headers=headers)
                if response.status_code == 200:
                    response = json.loads(response.text)
                    return redirect(url_for('users.my_profile'))
                else:
                    return redirect(url_for('users.my_profile'))
            
            elif password != "":
                data = {"plain_password": password}
                response = requests.put(api_url, json=data, headers=headers)
                if response.status_code == 200:
                    response = json.loads(response.text)
                    return redirect(url_for('users.my_profile'))
                else:
                    return redirect(url_for('users.my_profile'))
            
            else:
                return redirect(url_for('users.my_profile'))
    return redirect(url_for('main.login'))

