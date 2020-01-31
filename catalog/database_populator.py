from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from database_setup import CoffeeShop, Base, MenuItem, User
from connect_database import connect_database


def populate_database():
    '''Populate the database'''

    session = connect_database()

    # create four intial users
    User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
                 picture='https://bootcampbarista.com/wp-content/uploads/2014/06/barista-holding-coffee-cu$
    session.add(User1)
    session.commit()

    User2 = User(name="Emma Bell", email="emmabell@gmail.com",
           picture='http://i2.cdn.turner.com/money/dam/assets/130529130233-starbucks-barista-1024x576.jpg'$
    session.add(User2)
    session.commit()

    User3 = User(name="Brittney Wright", email="brittneywrighter@gmail.com",
           picture='http://www.gannett-cdn.com/-mm-/af4fbd59496432518189c9ae390709aca94fe18f/c=547-506-244$
    session.add(User3)
    session.commit()

    User4 = User(name="Ryan Dunton", email="ryandunton1@gmail.com",
           picture="https://v.cdn.vine.co/v/avatars/62E84159-EE83-4cD1-Bc4c-cAc47E469A69-465-0000002AcFFA4$
    session.add(User4)
    session.commit()
    
    # Menu for Blue Bottle coffee
    coffeeShop1 = CoffeeShop(user_id=1, name="Blue Bottle Coffee")

    session.add(coffeeShop1)
    session.commit()

    menuItem1 = MenuItem(user_id=1, name="Blue Bottle Special",
                         description="House blend of our Blue Bottle coffee",
                         price="$3.50", coffeeshop=coffeeShop1)

    session.add(menuItem1)
    session.commit()


    menuItem2 = MenuItem(user_id=1, name="Decaf Blue Bottle",
                         description="A decaf version of our Blue Bottle special",
                         price="$2.99", coffeeshop=coffeeShop1)

    session.add(menuItem2)
    session.commit()

    menuItem3 = MenuItem(user_id=1, name="Blue Bottle club",
                         description="club sandwich on sourdough bread",
                         price="$5.99", coffeeshop=coffeeShop1)

    session.add(menuItem3)
    session.commit()

    menuItem4 = MenuItem(user_id=1, name="BB espresso shot",
                         description="Quick shot of espresso to pick you up",
                         price="$2.99", coffeeshop=coffeeShop1)

    session.add(menuItem4)
    session.commit()

    menuItem5 = MenuItem(user_id=1, name="Blue Bottle Water",
                         description="16oz of refreshing goodness",
                         price="$1.99", coffeeshop=coffeeShop1)

    session.add(menuItem5)
    session.commit()

    menuItem6 = MenuItem(user_id=1, name="Morning scone",
                         description="Vanilla scone, perfect for your commute",
                         price="$3.99", coffeeshop=coffeeShop1)

    session.add(menuItem6)
    session.commit()
    
    # Menu for Philz
    coffeeShop2 = CoffeeShop(user_id=2, name="Philz")

    session.add(coffeeShop2)
    session.commit()


    menuItem1 = MenuItem(user_id=2, name="Silken Splendor",
                         description="creamy thick goodness in coffee form",
                         price="$4.50", coffeeshop=coffeeShop2)

    session.add(menuItem1)
    session.commit()

    menuItem2 = MenuItem(user_id=2, name="Greater Alarm",
                         description="Our strongest blend of coffee!",
                         price="$4.99", coffeeshop=coffeeShop2)

    session.add(menuItem2)
    session.commit()

    menuItem3 = MenuItem(user_id=2, name="Ether",
                         description="A dark blend of coffee to wake you up!",
                         price="$3", coffeeshop=coffeeShop2)

    session.add(menuItem3)
    session.commit()

    menuItem4 = MenuItem(user_id=2, name="Jacob's Wonderbar",
                         description='''Another dark roast,
                                     popular with college students''',
                         price="$3.45", coffeeshop=coffeeShop2)

    session.add(menuItem4)
    session.commit()

    menuItem5 = MenuItem(user_id=2, name="canopy of Heaven",
                         description="Light roast of herbs, lemon and currant.",
                         price="$4.00", coffeeshop=coffeeShop2)

    session.add(menuItem5)
    session.commit()

    menuItem6 = MenuItem(user_id=2, name="Philtered Soul",
                         description='''Medium roast of our most
                                     popular blend of coffee''',
                         price="$4.29", coffeeshop=coffeeShop2)

    session.add(menuItem6)
    session.commit()
    
    # Menu for Starbucks
    coffeeShop3 = CoffeeShop(user_id=3, name="Starbucks")

    session.add(coffeeShop3)
    session.commit()


    menuItem1 = MenuItem(user_id=3, name="Americano",
                         description="Shot of espresso and hot water",
                         price="$4.30", coffeeshop=coffeeShop3)

    session.add(menuItem1)
    session.commit()

    menuItem2 = MenuItem(user_id=3, name="Salad Box",
                         description='''Box filled with tomatoes,
                                     lettuce and dressing.''',
                         price="$6.99", coffeeshop=coffeeShop3)

    session.add(menuItem2)
    session.commit()

    menuItem3 = MenuItem(user_id=3, name="Blonde Roast",
                         description="Our lightest roast, only served before 11!",
                         price="$3.95", coffeeshop=coffeeShop3)

    session.add(menuItem3)
    session.commit()
    
    menuItem4 = MenuItem(user_id=3, name="Pike's Place",
                         description='''Our signature roast and the favorite
                                     of customers all over the world''',
                         price="$3.99", coffeeshop=coffeeShop3)

    session.add(menuItem4)
    session.commit()

    menuItem5 = MenuItem(user_id=3, name="Decaf Roast",
                         description="A pour over of our decaf roast",
                         price="$2.50", coffeeshop=coffeeShop3)

    session.add(menuItem5)
    session.commit()
    
    # Menu for Huckberry Roasters
    coffeeShop4 = CoffeeShop(user_id=4, name="Huckberry Roasters")

    session.add(coffeeShop4)
    session.commit()


    menuItem1 = MenuItem(user_id=4, name="Milk Latte",
                         description="Latte made with milk and local beans!",
                         price="$2.99", coffeeshop=coffeeShop4)

    session.add(menuItem1)
    session.commit()

    menuItem2 = MenuItem(user_id=4, name="House Blend",
                         description='''Our traditional house blend made
                                     with fresh and local beans''',
                         price="$3.99", coffeeshop=coffeeShop4)

    session.add(menuItem2)
    session.commit()

    menuItem3 = MenuItem(user_id=4, name="Decaf House Blend",
                         description="A decaf version of our House Blend",
                         price="$4.50", coffeeshop=coffeeShop4)

    session.add(menuItem3)
    session.commit()

    menuItem4 = MenuItem(user_id=4, name="Espresso Shot",
                         description="Our take on the traditional espresso shot!",
                         price="$2.95", coffeeshop=coffeeShop4)

    session.add(menuItem4)
    session.commit()

    menuItem5 = MenuItem(user_id=4, name="croissant",
                         description='''French favorite, great way to
                                     start your s'morning!''',
                         price="$3.95", coffeeshop=coffeeShop4)

    session.add(menuItem5)
    session.commit()

    print "added menu items!"
