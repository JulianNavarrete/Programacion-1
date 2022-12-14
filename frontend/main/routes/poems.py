from flask import Blueprint, render_template, url_for, redirect, json, current_app, request, flash, make_response, flash
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
    print("Llega acá 0")
    jwt = functions.get_jwt()
    print("Llega acá 1")
    if jwt:
        if request.method == 'POST':
            title = request.form['title']
            body = request.form['body']
            print("Llega acá 2")
            # print(title)
            # print(body)
            id = request.cookies.get('id')
            data = {'title': title, 'body': body, 'userId': id}
            headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {jwt}'}
            if title != "" and body != "":
                response = requests.post(f'{current_app.config["API_URL"]}/poems', json=data, headers=headers)
                # print(response)
                if response.ok:
                    response = json.loads(response.text)
                    # print(response)
                    return redirect(url_for('main.home'))  # main.user_main
                else:
                    return redirect(url_for('poems.write_poem'))
            else:
                return redirect(url_for('poems.write_poem'))
        else:
            return render_template('write_poem.html', jwt=jwt)
    else:
        flash('You must be logged in to do that.', 'warning')
        return redirect(url_for('main.login'))


@poems.route('/poems/<id>', methods=['GET'])
def view_poem(id):
    if request.cookies.get('access_token'):
        userId = request.cookies.get('id')
        jwt = functions.get_jwt()
        api_url = f'{current_app.config["API_URL"]}/poem/{id}'
        headers = {f"Content-Type": "application/json", "Authorization": "Bearer {}".format(jwt)}
        response = requests.get(api_url, headers=headers)
        poem = json.loads(response.text)
        scores = functions.get_scores_by_poem_id(id)
        scores = json.loads(scores.text)
        print("Hola")
        return render_template('poem_details.html', poem=poem, jwt=jwt, userId=int(userId), scores=scores)
    else:
        return render_template('main.home')


@poems.route('/poem/<id>/rate', methods=['GET', 'POST'])
def rate_poem(id):
    jwt = functions.get_jwt()
    if jwt:
        if request.method == 'GET':
            api_url = f'{current_app.config["API_URL"]}/poem/{id}'
            headers = {"Content-Type": "application/json", "Authorization": f"Bearer {jwt}"}
            response = requests.get(api_url, headers=headers)
            poem = json.loads(response.text)
            return render_template('rate_poem.html', poem=poem)

        if request.method == 'POST':
            api_url = f'{current_app.config["API_URL"]}scores'
            headers = {"Content-Type": "application/json", "Authorization": f"Bearer {jwt}"}
            user_id = request.cookies.get('id')
            score = request.form['score']
            commentary = request.form['comment']
            response = functions.add_mark(user_id=user_id, poem_id=id, score=score, comment=commentary)
            if response.ok:
                response = json.loads(response.text)
                return redirect(url_for('main.home'))
                
            return redirect(url_for('main.home'))
    else:
        return redirect(url_for('main.login'))

