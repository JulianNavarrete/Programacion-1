from flask import request, current_app
import requests, json


def login(email, password):
    api_url = f'{current_app.config["API_URL"]}/auth/login'
    data = {"email": email, "password": password}
    headers = {"Content-Type": "application/json"}

    return requests.post(api_url, json=data, headers=headers)


def get_jwt():
    return request.cookies.get('access_token')


def get_poems_by_id(id, page=1, perpage=3):
    api_url = f'{current_app.config["API_URL"]}/poems'
    data = {"page": page, "perpage": perpage, "userId": id}
    headers = get_headers(without_token=True)

    return requests.get(api_url, json=data, headers=headers)


def get_scores_by_poem_id(id):
    api_url = f'{current_app.config["API_URL"]}/scores'
    data = {"poemId": id}
    headers = get_headers(without_token=False)

    return requests.get(api_url, json=data, headers=headers)


def get_headers(without_token=False, jwt=None):
    if jwt == None and without_token == False:
        return {"Content-Type": "application/json", "Authorization": f"Bearer {get_jwt()}"}
    if jwt and without_token == False:
        return {"Content-Type": "application/json", "Authorization": f"Bearer {jwt}"}
    else:
        return {"Content-Type": "application/json"}


def add_score(user_id, poem_id, score, comment):
    jwt = request.cookies.get('access_token')
    api_url = f'{current_app.config["API_URL"]}/scores'
    data = {"userId": user_id, "poemId": poem_id, "score": score, "comment": comment}
    headers = {"Content-Type": "application/json", "Authorization" : f"Bearer {jwt}"}
    return requests.post(api_url, json=data, headers=headers)


def get_user_info(id):
    api_url = f'{current_app.config["API_URL"]}/user/{id}'
    headers = get_headers()

    return requests.get(api_url, headers=headers)

def delete_poem(user_id, poem_id, score, comment):
    jwt = request.cookies.get('access_token')
    api_url = f'{current_app.config["API_URL"]}/poem/{id}'
    data = {"poemId": poem_id}
    headers = {"Content-Type": "application/json", "Authorization" : f"Bearer {jwt}"}
    return requests.delete(api_url, json=data, headers=headers)

