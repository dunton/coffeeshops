# Project to create a website of local coffeeshops that owners of
# Said Coffeeshops can use to edit, add, delete and display their
# coffeeshops to the public
#
# Created by Ryan Dunton on April 6, 2016

from flask import Flask, render_template, request, redirect
from flask import jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker, scoped_session
from database_setup import Base, User, CoffeeShop, MenuItem
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from oauth2client.client import AccessTokenCredentials
import httplib2
import json
from flask import make_response
import requests
import sys
import os
from connect_database import connect_database

app = Flask(__name__)

app.secret_key = 'secret'

#engine = create_engine('sqlite:///coffeeShopmenu.db')
#Base.metadata.bind = engine

#DBSession = sessionmaker(bind=engine)
#session = DBSession()


@app.route('/login')
@app.route('/coffeeshops/login')
def showLogin():
    '''Create login page and state variable'''
    state = ''.join(random.choice(string.ascii_uppercase +
                    string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    '''Allows user to login by using their Facebook account'''
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token
    
    fb_client_secrets_file = 'var/www/coffeeshops/catalog/fb_client_secrets.json'
    
    app_id = json.loads(open(fb_client_secrets_file, 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open(fb_client_secrets_file, 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (app_id, app_secret, access_token) 
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.4/me"
    # strip expire tag from access token
    token = result.split("&")[0]

    url = 'https://graph.facebook.com/v2.5/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to
    # properly logout
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = 'https://graph.facebook.com/v2.5/me/picture?%s&redirect=0&height=200&width=200' % token  
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;">'  # noqa

    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    '''Disconnects from Facebook id'''
    facebook_id = login_session['facebook_id']
    # The access token must be included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


# User Helper Functions
def createUser(login_session):
    '''Allows us to create new users'''
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session = connect_database()
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    session = connect_database()
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    session = connect_database()
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/coffeeshops/disconnect')
@app.route('/disconnect')
def disconnect():
    '''Disconnect based on provider, sends back to homepage'''
    if 'provider' in login_session:
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['credentials']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showCoffeeshops'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showCoffeeshops'))


@app.route('/coffeeshops/JSON')
def coffeeshopsJSON():
    '''Allows API calls of all coffeeshops'''
    session = connect_database()
    coffeeshops = session.query(CoffeeShop).order_by(CoffeeShop.id).all()
    return jsonify(CoffeeShops=[i.serialize for i in coffeeshops])


@app.route('/coffeeshops/<int:coffeeshop_id>/menu/JSON')
def coffeeshopMenuJSON(coffeeshop_id):
    '''Allows API calls of coffeeshop menus'''
    session = connect_database()
    coffeeshop = session.query(CoffeeShop).filter_by(id=coffeeshop_id).one()
    items = session.query(MenuItem).filter_by(coffeeshop_id=coffeeshop_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/coffeeshops/<int:coffeeshop_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(coffeeshop_id, menu_id):
    '''Allows API calls of coffeeshop menu items'''
    session = connect_database()
    menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem=menuItem.serialize)


@app.route('/')
@app.route('/coffeeshops')
@app.route('/coffeeshops/')
def showCoffeeshops():
    '''Establish homepage, check if logged in or not'''
    session = connect_database()
    coffeeshops = session.query(CoffeeShop).order_by(asc(CoffeeShop.name))
    if 'username' not in login_session:
        return render_template('publicCoffeeshops.html',
                               coffeeshops=coffeeshops)
    else:
        return render_template('coffeeshops.html', coffeeshops=coffeeshops)


@app.route('/coffeeshops/<int:coffeeshop_id>/')
@app.route('/coffeeshops/<int:coffeeshop_id>/menu')
def coffeeshopMenu(coffeeshop_id):
    '''Allows access to coffeeshops depending if user is logged in or not'''
    session = connect_database()
    coffeeshop = session.query(CoffeeShop).filter_by(id=coffeeshop_id).one()
    creator = getUserInfo(coffeeshop.user_id)
    items = session.query(MenuItem).filter_by(coffeeshop_id=coffeeshop_id).all()
    if 'username' not in login_session or creator.id != login_session['user_id']:
        return render_template('publicmenu.html', items=items,
                               coffeeshop=coffeeshop, creator=creator)
    return render_template('menu.html', coffeeshop=coffeeshop, items=items)


@app.route('/coffeeshops/<int:coffeeshop_id>/menu/new/',
           methods=['GET', 'POST'])
def newMenuItem(coffeeshop_id):
    '''Create new menu item if owner of the coffeshop'''
    if 'username' not in login_session:
        return redirect('/login')
    session = connect_database()
    coffeeshop = session.query(CoffeeShop).filter_by(id=coffeeshop_id).one()
    if login_session['user_id'] != coffeeshop.user_id:
        flash('''You are not authorized to add menu items to this restaurant.
        Please create your own restaurant in order to add items.''')
        return redirect(url_for('coffeeshopMenu', coffeeshop_id=coffeeshop_id))
    # Accesses what is inside the form at newMenuItem.html
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'],
                           description=request.form['description'],
                           price=request.form['price'],
                           coffeeshop_id=coffeeshop_id,
                           user_id=coffeeshop.user_id)
        session.add(newItem)
        session.commit()
        flash("New menu item created!")
        return redirect(url_for('coffeeshopMenu', coffeeshop_id=coffeeshop_id))
    else:
        return render_template('newMenuItem.html', coffeeshop_id=coffeeshop_id)


@app.route('/coffeeshops/new', methods=['GET', 'POST'])
def newCoffeeshop():
    '''Allows user to create a new coffeeshop if they log in'''
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newCoffeeshop = CoffeeShop(name=request.form['name'],
                                   user_id=login_session['user_id'])
        # Adds coffeeshop to database
        session = connect_database()
        session.add(newCoffeeshop)
        session.commit()
        flash("new coffee shop created!")
        return redirect(url_for('showCoffeeshops'))
    else:
        return render_template('newCoffeeShop.html')


@app.route('/coffeeshops/<int:coffeeshop_id>/menu/<int:menu_id>/edit/',
           methods=['GET', 'POST'])
def editMenuItem(coffeeshop_id, menu_id):
    '''Allows user to edit menu items of their restaurant'''
    if 'username' not in login_session:
        return redirect('/login')
    session = connect_database()
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    coffeeshop = session.query(CoffeeShop).filter_by(id=coffeeshop_id).one()
    if login_session['user_id'] != coffeeshop.user_id:
        flash('''You are not authorized to edit menu items to this restaurant.
              Please create your own restaurant in order to edit items.''')
        return redirect(url_for('coffeeshopMenu', coffeeshop_id=coffeeshop_id,
                                menu_id=menu_id))
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']
        # Changes menu item in database
        session = connect_database()
        session.add(editedItem)
        session.commit()
        flash("menu item edited!")
        return redirect(url_for('coffeeshopMenu', coffeeshop_id=coffeeshop_id,
                        menu_id=menu_id))
    else:
        return render_template('editMenuItem.html',
                               coffeeshop_id=coffeeshop_id, menu_id=menu_id,
                               i=editedItem)


@app.route('/coffeeshops/<int:coffeeshop_id>/edit', methods=['GET', 'POST'])
def editCoffeeShop(coffeeshop_id):
    '''Allows user to edit coffeeshop name'''
    editedShop = session.query(CoffeeShop).filter_by(id=coffeeshop_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if editedShop.user_id != login_session['user_id']:
        flash('''You are not authorized to edit this restaurant.
              Please create your own restaurant in order to edit.''')
        return redirect(url_for('showCoffeeshops'))
    if request.method == 'POST':
        if request.form['name']:
            editedShop.name = request.form['name']
        session = connect_database()
        session.add(editedShop)
        session.commit()
        flash("Coffee shop edited!")
        return redirect(url_for('showCoffeeshops'))
    else:
        return render_template('editCoffeeShop.html', coffeeshop=editedShop)


@app.route('/coffeeshops/<int:coffeeshop_id>/menu/<int:menu_id>/delete',
           methods=['GET', 'POST'])
def deleteMenuItem(coffeeshop_id, menu_id):
    '''Allows user to delete items of their coffeeshop'''
    if 'username' not in login_session:
        return redirect('/login')
    session = connect_database()
    coffeeshop = session.query(CoffeeShop).filter_by(id=coffeeshop_id).one()
    itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
    if login_session['user_id'] != coffeeshop.user_id:
        flash('''You are not authorized to delete menu items to this restaurant.
              Please create your own restaurant in order to delete items.''')
        return redirect(url_for('coffeeshopMenu', coffeeshop_id=coffeeshop_id))
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("menu item deleted!")
        return redirect(url_for('coffeeshopMenu', coffeeshop_id=coffeeshop_id))
    else:
        return render_template('deleteMenuItem.html', i=itemToDelete)


@app.route('/coffeeshops/<int:coffeeshop_id>/delete', methods=['GET', 'POST'])
def deleteCoffeeShop(coffeeshop_id):
    '''Allows user to delete their coffeeshop'''
    coffeeshopToDelete = session.query(CoffeeShop).filter_by(
        id=coffeeshop_id).one()
    if 'username' not in login_session:
        return redirect('login')
    if coffeeshopToDelete.user_id != login_session['user_id']:
        flash('''You are not authorized to delete this restaurant.
            Please create your own restaurant in order to delete.''')
        return redirect(url_for('showCoffeeshops'))
    if request.method == 'POST':
        session = connect_database()
        session.delete(coffeeshopToDelete)
        session.commit()
        flash("coffee shop deleted!")
        return redirect(url_for('showCoffeeshops'))
    else:
        return render_template('deleteCoffeeShop.html',
                               coffeeshop=coffeeshopToDelete)

# Runs on port 8000
#if __name__ == '__main__':
    #app.secret_key = 'super_secret_key'
    #app.debug = True
    #app.run(host='0.0.0.0', port=8000)
    
