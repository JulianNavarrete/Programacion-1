from flask import Blueprint, render_template, url_for, redirect, json, current_app, request, flash, make_response
import requests, json
from . import functions

users = Blueprint('users', __name__, url_prefix='/')


@users.route('/users')
def a():
    pass

