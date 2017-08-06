import requests
import json
from flask import abort, jsonify, render_template, redirect, request
from manage import app, client
from . import main

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

    return render_template('index.html', inventory=formatted_inventory,
                           hackathons=formatted_hackathons,
                           client_id=app.config['CLIENT_ID'])

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
        print('yay')
        print(response)
    else:
        print('nay')
        print(response)

    print(response)

    return jsonify({'status': 'wip'})

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
    