from flask import Blueprint, render_template, url_for, redirect, json, current_app, request, flash, make_response
import requests, json
from . import functions

poems = Blueprint('poems', __name__, url_prefix='/')

'''
@poems.route('/view/my-poems')
def view():
    jwt = functions.get_jwt()
    if jwt:
        userId = request.cookies.get('id')
        # print("user_id", userId)
        response = functions.get_poems_by_id(userId)
        # print("api_url", response)
        poems = json.loads(response.text)
        # print("poems", poems)
        poemsList = poems["poems"]

        return render_template('#not exist#.html', jwt=jwt, poems=poemsList)
    else:
        return redirect(url_for('main.login'))
'''


@poems.route('/write-poem', methods=['GET', 'POST'])
def write_poem():
    jwt = functions.get_jwt()
    if jwt:
        if request.method == 'POST':
            title = request.form['title']
            body = request.form['body']
            print(title)
            print(body)
            id = request.cookies.get('id')
            data = {'title': title, 'body': body, 'userId': id}
            headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {jwt}'}
            if title != "" and body != "":
                response = requests.post(f'{current_app.config["API_URL"]}/poems', json=data, headers=headers)
                print(response)
                if response.ok:
                    response = json.loads(response.text)
                    print(response)
                    return redirect(url_for('main.home'))  # main.user_main
                else:
                    return redirect(url_for('poems.write_poem'))
            else:
                return redirect(url_for('poems.write_poem'))
        else:
            return render_template('write_poem.html', jwt=jwt)
    else:
        return redirect(url_for('main.login'))

