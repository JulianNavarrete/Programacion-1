from flask import Blueprint, render_template, make_response, request, current_app, redirect, url_for
import requests, json

main = Blueprint('main', __name__, url_prefix='/')


@main.route('/')
def home():
    return render_template('home.html')
