from flask import (abort, g, jsonify, render_template, redirect,
                   request, send_file, session, url_for)
from manage import app, manager
import os
from random import randint
from . import main

@main.route('/')
def index():
    return render_template('index.html')