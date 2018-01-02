import email
import hashlib
import json
import os
import requests
import smtplib
import uuid
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
        <td id="{name}-quant">{quantity}</td>
        <td>{reservation_length}</td>
        <td>{item_category}</td>
        <td><a href="{tutorials_link}">Link</a></td>
        <td>
            <form id="add-to-cart">
                <input type="number" name="cart_quanity" min="1"
                       max="{quantity}" placeholder="1"
                       id="cart_quantity" required>
                <input id="name" value="{name}" style="display: none" disabled>
                <button id="add_to_cart_b" type="submit"
                        style="background: none; border: none;">
                    <a>
                      Add to Cart
                      <i class="fa fa-shopping-cart" aria-hidden="true"></i>
                    </a>
                </button>
            </form>
        </td>
        </tr>
        '''.format(item_id=item['item_id'], name=item['name'],
                        quantity=item['quantity'],
                        reservation_length=item['reservation_length'],
                        item_category=item['category'],
                        tutorials_link=item['tutorials_link'])
        inventory_list.append(formatted_item)
    formatted_inventory = '\n'.join(inventory_list)

    hackathons = db.hackathons.find()
    hackathon_list = []
    for hackathon in hackathons:
        maps_link = 'https://www.google.com/maps/search/' + \
                    hackathon['location']
        formatted_hackathon = '''
        <tr>
        <td><a href="{link}" target="_blank">{name}</a></td>
        <td><a href="{location_link}" target="_blank">{location}</a></td>
        <td>{date}</td>
        </tr>
        '''.format(name=hackathon['name'], location=hackathon['location'],
                   location_link=maps_link, date=hackathon['date_range'],
                   link=hackathon['link'])
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
    admin = False
    if 'user' in session:
        admin = session['user'] in app.config['ADMIN_EMAILS']
    return render_template('index.html', inventory=formatted_inventory,
                           hackathons=formatted_hackathons, user=user,
                           client_id=client_id, welcome_msg=welcome_msg,
                           admin=admin)

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

def login_required(f):
    '''
        Allows the passed function to only be executed when the user is
        logged in
    :return:
        decorated function
    '''
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' in session:
            db = client.tudev_checkout
            found_user = db.users.find_one({'email': session['user']})
            if found_user:
                return f(*args, **kwargs)
        abort(405)
        return f(*args, **kwargs)
    return decorated_function

@main.route('/submit_request', methods=['POST'])
@login_required
def submit_request():
    db = client.tudev_checkout
    data = dict(request.form)
    print(data)
    resp = {}
    resp['success'] = []
    resp['failed'] = []
    for item in data:
        item_name = data[item][0]
        item_quantity = int(data[item][1])
        stored_item = db.inventory.find_one({'name': item_name})
        if(stored_item):
            if(stored_item['quantity'] >= item_quantity):
                new_quant = stored_item['quantity'] - item_quantity
                db.inventory.update({'name': item_name},
                                    {'$set': {'quantity': new_quant}})
                resp['success'].append({'name': item_name,
                                       'quantity': item_quantity})
            else:
                resp['failed'].append({'name': item_name,
                                       'quantity': item_quantity})
    request_id = str(uuid.uuid4())[:4]
    resp['id'] = request_id
    return jsonify(resp)

@main.route('/admin')
@admin_required
def admin():
    db = client.tudev_checkout
    
    inventory = db.inventory.find()
    inventory_list = []
    for item in inventory:
        formatted_item = '''
        <tr>
        <td>{item_id}</td>
        <td>{name}</td>
        <td>{quantity}</td>
        <td>{reservation_length}</td>
        <td>{item_category}</td>
        <td><a href="{tutorials_link}">Link</a></td>
        </tr>'''.format(item_id=item['item_id'], name=item['name'],
                        quantity=item['quantity'],
                        reservation_length=item['reservation_length'],
                        item_category=item['category'],
                        tutorials_link=item['tutorials_link'])
        inventory_list.append(formatted_item)
    formatted_inventory = '\n'.join(inventory_list)

    hackathons = db.hackathons.find()
    hackathon_list = []
    for hackathon in hackathons:
        maps_link = 'https://www.google.com/maps/search/' + \
                    hackathon['location']
        formatted_hackathon = '''
        <tr>
        <td><a href="{link}" target="_blank">{name}</a></td>
        <td><a href="{location_link}" target="_blank">{location}</a></td>
        <td>{date}</td>
        </tr>
        '''.format(name=hackathon['name'], location=hackathon['location'],
                   date=hackathon['date_range'], link=hackathon['link'],
                   location_link=maps_link)
        hackathon_list.append(formatted_hackathon)
    formatted_hackathons = '\n'.join(hackathon_list)

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

    return render_template('admin.html', inventory=formatted_inventory,
                           hackathons=formatted_hackathons, user=user,
                           welcome_msg=welcome_msg)

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

        # add user to database to track how many people have signed in
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
        return jsonify({'status': 'not logged in'})

@main.route('/request_item', methods=['POST'])
@login_required
def request_item():
    data = request.form
    try:
        name = data['name']
        email_account = data['email']
        item = data['item']
        content = data['content']
        confirm_msg = email.message.Message()
        confirm_msg['Subject'] = 'Request Item - Request Recieved'
        confirm_msg['From'] = app.config['REQUEST_EMAIL_SEND']
        confirm_msg['To'] = email_account
        confirm_msg.add_header('Content-Type', 'text/html')

        email_content = '''
        <html>
        <body>
            <p>
            Hey {name}!
            <br>
            We recieved your request, we'll look into "{item}".
            <br>
            Happy Hacking,
            <br>
            The TUDev Team
            </p>
        </body>
        </html>'''.format(name=name.split(' ')[0], item=item)

        confirm_msg.set_payload(email_content)

        email_server = smtplib.SMTP(app.config['SMTP'])

        email_server.starttls() 
        email_server.login(app.config['EMAIL_USER'], app.config['EMAIL_PASS'])
        # send email
        email_server.sendmail(app.config['REQUEST_EMAIL_SEND'], email_account,
                              confirm_msg.as_string())

        request_msg = email.message.Message()
        request_msg['Subject'] = 'TUDev Hardware - Item Request'
        request_msg['From'] = app.config['REQUEST_EMAIL_SEND']
        request_msg['To'] = email_account
        request_msg.add_header('Content-Type', 'text/html')

        email_content = '''
        <html>
        <body>
            <h1>Item Request</h1>
            <p><strong>From: </strong>{name}</p>
            <p><strong>Email: </strong>{email_account}</p>
            <p><strong>Item Requested: </strong>{item}</p>
            <p><strong>Reason for request</strong><br>{content}</p>
        </body>
        </html>'''.format(name=name, email_account=email_account, item=item,
                          content=content)

        request_msg.set_payload(email_content)
        for account in app.config['REQUEST_EMAIL_ADMINS']:
            email_server.sendmail(app.config['REQUEST_EMAIL_SEND'],
                                  account, request_msg.as_string())

        return jsonify({'status': 'request sent'})

    except KeyError as e:
        abort(400)


@main.route('/inventory')
def inventory():
    return jsonify({'status': 'wip'})

@main.route('/add_hackathon', methods=['POST'])
@admin_required
def add_hackathon():
    data = request.form

    try:
        name = data['name']
        location = data['location']
        date_range = data['date']
        link = data['link']

        db = client.tudev_checkout
        db.hackathons.update({'name': name},
                              {
                              'name': name,
                              'location': location,
                              'date_range': date_range,
                              'link': link
                              }, upsert=True)
        return jsonify({'Status': 'Hackathon added/updated.'})
    except KeyError:
        abort(400)

@main.route('/remove_hackathon', methods=['POST'])
@admin_required
def remove_hackathon():
    data = request.form
    try:
        hackathon_name = data['name']
        db = client.tudev_checkout
        db.hackathons.remove({'name': hackathon_name})

        return jsonify({'status': 'hackathon removed'})
    except KeyError:
        abort(400)

@main.route('/add_item', methods=['POST'])
@admin_required
def add_tem():
    data = request.form

    try:
        name = data['name']
        quantity = int(data['quantity'])
        res_length = data['res_length']
        category = data['category']
        tutorial_link = data['item_link']
        item_id = data['item_id']

        if item_id:
            db = client.tudev_checkout

            db.inventory.update({'item_id': item_id},
                            {
                                'name': name,
                                'quantity': quantity,
                                'reservation_length': res_length,
                                'category': category,
                                'tutorials_link': tutorial_link,
                                'item_id': item_id
                            }, upsert=True)
            return jsonify({'updated': item_id})
        else:
            item_id = hashlib.sha1(bytes(os.urandom(32)))
            item_id = item_id.hexdigest()[:4]
            
            db = client.tudev_checkout

            db.inventory.insert({
                                'name': name,
                                'quantity': quantity,
                                'reservation_length': res_length,
                                'category': category,
                                'tutorials_link': tutorial_link,
                                'item_id': item_id
                            })
            return jsonify({'inserted': item_id})
    except KeyError:
        abort(400)

    return jsonify({'status': 'done'})

@main.route('/increase_quantity', methods=['POST'])
@admin_required
def increase_quantity():
    data = request.form

    try:
        item_id = data['item_id']
        add_ons = int(data['quantity'])

        db = client.tudev_checkout

        c_item = db.inventory.find_one({'item_id': item_id})

        if c_item:
            db.inventory.update({'item_id': item_id},
                                {
                                    'name': c_item['name'],
                                    'quantity': c_item['quantity'] + add_ons,
                                    'reservation_length': c_item['reservation_length'],
                                    'category': c_item['category'],
                                    'tutorials_link': c_item['tutorials_link'],
                                    'item_id': item_id
                                })
            return jsonify({'updated': item_id})
        else:
            abort(404)
    except KeyError:
        abort(400)

@main.route('/remove_item', methods=['POST'])
@admin_required
def remove_item():
    data = request.form

    try:
        item_id = data['item_id']
        if data['quantity']:
            removals = int(data['quantity'])
        else:
            removals = 0

        if removals:
            db = client.tudev_checkout
            c_item = db.inventory.find_one({'item_id': item_id})

            if c_item:
                if c_item['quantity'] > removals:
                    db.inventory.update({'item_id': item_id},
                                        {
                                        'name': c_item['name'],
                                        'quantity': c_item['quantity'] - \
                                                    removals,
                                        'reservation_length': c_item['reservation_length'],
                                        'category': c_item['category'],
                                        'tutorials_link': c_item['tutorials_link'],
                                        'item_id': item_id
                                        })
                    return jsonify({'updated': item_id})
                else:
                    db.inventory.remove({'item_id': item_id})
                    return jsonify({'removed': item_id})
        else:
            db = client.tudev_checkout
            db.inventory.remove({'item_id': item_id})
            return jsonify({'removed': item_id})
    except KeyError:
        abort(400)

@main.route('/logout')
def logout():
    g.user = None
    session.pop('user', None)
    return redirect(url_for('.index'))    