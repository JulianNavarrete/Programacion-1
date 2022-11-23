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


def get_headers(without_token=False, jwt=None):
    if jwt == None and without_token == False:
        return {"Content-Type": "application/json", "Authorization": f"Bearer {get_jwt()}"}
    if jwt and without_token == False:
        return {"Content-Type": "application/json", "Authorization": f"Bearer {jwt}"}
    else:
        return {"Content-Type": "application/json"}


