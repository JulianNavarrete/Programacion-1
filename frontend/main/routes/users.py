from flask import Blueprint, render_template, url_for, redirect, json, current_app, request, flash, make_response
import requests, json
from . import functions

users = Blueprint('users', __name__, url_prefix='/')


@users.route('user/my-profile')
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


@users.route('user/edit-profile', methods=['GET', 'POST'])
def modify_profile():
    jwt = request.cookies.get('access_token')
    if jwt:
        user_id = request.cookies.get('id')
        # print("Asdddd")
        if request.method == 'GET':
            api_url = f'{current_app.config["API_URL"]}/user/{user_id}'
            headers = {'Content-type': 'application/json', 'Authorization': f"Bearer {jwt}"}
            response = requests.get(api_url, headers=headers)            
            user = json.loads(response.text)

            return render_template('edit_user.html', user=user)
            
        if request.method == 'POST':
            name = request.form['name']
            print("name", name)
            email = request.form['email']
            print(email)
            password = request.form['password']
            print("password", password)
            api_url = f'{current_app.config["API_URL"]}/user/{user_id}'
            # data = {"name": name, "email": email, "plain_password": password}
            headers = {'Content-type': 'application/json', 'Authorization' : f"Bearer {jwt}"}
            print("1")
            if email != "":
                print("2")
                data = {"email": email}
                response = requests.put(api_url, json=data, headers=headers)
                print("3")
                if response.status_code == 200:
                    response = json.loads(response.text)
                    return redirect(url_for('users.my_profile'))
                else:
                    return redirect(url_for('users.my_profile'))
            
            if name != "":
                data = {"name": name}
                response = requests.put(api_url, json=data, headers=headers)
                if response.status_code == 200:
                    response = json.loads(response.text)
                    return redirect(url_for('users.my_profile'))
                else:
                    return redirect(url_for('users.my_profile'))
            
            if password != "":
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

