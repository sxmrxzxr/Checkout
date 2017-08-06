import requests
import json
from datetime import datetime
from flask import (abort, jsonify, g, session, render_template, redirect,
                   request, url_for)
from functools import wraps
from manage import app, client
from random import randint
from . import main


@main.before_request
def before_request():
    session.permanent = True
    g.user = None
    if 'user' in session:
        g.user = session['user']

@main.route('/')
def index():
    db = client.tudev_checkout
    
    inventory = db.inventory.find()
    inventory_list = []
    for item in inventory:
        formatted_item = '''
        <tr>
        <td>{name}</td>
        <td>{quantity}</td>
        <td>{reservation_length}</td>
        <td>{item_category}</td>
        <td>{tutorials_link}</td>
        <td>
            <input type="number" name="cart_quanity" min="1" max="{quantity}"
            placeholder="1">
            <a href="#add_to_cart"> Add to Cart <i class="fa fa-shopping-cart"
            aria-hidden="true"></i></a>
        </td>
        </tr>'''.format(name=item['name'], quantity=item['quantity'],
                        reservation_length=item['reservation_length'],
                        item_category=item['category'],
                        tutorials_link=item['tutorials_link'])
        inventory_list.append(formatted_item)
    formatted_inventory = '\n'.join(inventory_list)

    hackathons = db.hackathons.find()
    hackathon_list = []
    for hackathon in hackathons:
        formatted_hackathon = '''
        <tr>
        <td>{name}</td>
        <td>{location}</td>
        <td>{date}</td>
        </tr>
        '''.format(name=hackathon['name'], location=hackathon['location'],
                   date=hackathon['date'])
        hackathon_list.append(formatted_hackathon)
    formatted_hackathons = '\n'.join(hackathon_list)

    client_id = None
    welcome_msg = None
    user = None
    if g.user is None or 'user' not in session:
        client_id = app.config['CLIENT_ID']
    else:
        db = client.tudev_checkout
        found_user = db.users.find_one({'email': session['user']})
        user = session['user']
        if found_user:
            if found_user['email'] == 'shetyeshail@gmail.com':
                user = 'Cuff Boy'
            else:
                user = found_user['name'].split(' ')[0]
        random_msg_index = randint(0,len(app.config['WELCOME_MSG'])-1)
        welcome_msg = app.config['WELCOME_MSG'][random_msg_index]

    return render_template('index.html', inventory=formatted_inventory,
                           hackathons=formatted_hackathons, user=user,
                           client_id=client_id, welcome_msg=welcome_msg)
def admin_required(f):
    '''
        Allows the passed function to only be executed when the user is
        logged in
    :return:
        decorated function
    '''
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' in session:
            if session['user'] in app.config['ADMIN_EMAILS']:
                return f(*args, **kwargs)
        return redirect(url_for('.index'))
        return f(*args, **kwargs)
    return decorated_function

@main.route('/admin')
@admin_required
def admin():
    return jsonify({'yay': 'admin'})

@main.route('/authorize')
def authorize():
    code = request.values['code']
    oauth_url = ('https://slack.com/api/oauth.access?client_id=%s'
                 '&client_secret=%s&code=%s' % (app.config['CLIENT_ID'],
                                                app.config['CLIENT_SECRET'],
                                                code))
    oauth_verify = requests.get(oauth_url)
    
    response = json.loads(oauth_verify.text)

    if response['ok']:
        # set session for user
        session['user'] = response['user']['email']

        # add user to databse to track how many people have signed in
        db = client.tudev_checkout
        db.users.update({'email': response['user']['email']},
                        {
                         'email': response['user']['email'],
                         'name': response['user']['name'],
                         'recent-signin': datetime.now()
                        }, upsert=True)

        if response['user']['email'] in app.config['ADMIN_EMAILS']:
            return redirect(url_for('.admin'))
        else:
            redirect(url_for('.index'))
    else:
        print(response)
        return jsonify({'status': 'not logged in'})

@main.route('/request_item')
def request_item():
    data = request.form
    name = data['name']
    email = data['email']
    item = data['item']
    content = data['content']

@main.route('/inventory')
def inventory():
    return jsonify({'status': 'wip'})

@main.route('/logout')
def logout():
    g.user = None
    session.pop('user', None)
    return redirect(url_for('.index'))    