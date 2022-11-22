from flask import Blueprint, render_template, make_response, request, current_app, redirect, url_for
import requests, json

poem = Blueprint('poem', __name__, url_prefix='/poem')


@poem.route('/create_poem')
def create_poem():
    return render_template('create_poem.html')
