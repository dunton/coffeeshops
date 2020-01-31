# Coffeeshop Catalog

This is a catalog of local coffeeshops and their items. Users can add, edit and delete their own 
coffeeshops and items.

### Set-Up

You must install vagrant in order to run  this program. After vagrant is 
installed you can unzip **Coffeeshop_Catalog**. The zipped file should
contain:

* **Vagrantfile**
* **pg_config.sh**
* **README**.**md**
* A folder named **catalog** containing:
    * **coffeeshopmenu**.**db**
    * **database_populator.py**
    * **database_setup**.pyc**
    * **final_project.py**
    * **fb_client_secrets.json**
    * A folder named Templates
    * A folder named Static
* The Template folder includes:
    * **coffeeshops.html**
    * **database_setup.pyc**
    * **deleteCoffeeShop.html**
    * **deleteMenuItem.html**
    * **editCoffeeShop.html**
    * **editMenuItem.html**
    * **header.html**
    * **login.html**
    * **main.html**
    * **menu.html**
    * **newCoffeeShop.html**
    * **publicCoffeeshop.html**
    * **publicmain.html**
    * **publicmenu.html**
    * **editCoffeeshop.html**
* The Static folder includes:
    * **styles.css**
    * **top-banner.jpg**
    * **blank_user.gif**

### Running the Program

First "vagrant up" to launch the vm then sign in using "vagrant ssh".

Navigate to 'vagrant' by typing `cd /vagrant` into the command line. Then navigate into catalog by
typing `cd catalog`.  Then type `python final_project.py` to launch the application. 

After launching, go to your browser and type `localhost:8000/coffeeshops`. Have fun exploring the 
website!
