import json
from flask import Flask, render_template, redirect, url_for, request
from config import *
from database import * 
from auth import *

app = Flask(__name__, template_folder='templates')

CONFIGURED = False

@app.route('/')
def index():    
    return render_template('dashboard.html')

@app.route('/setup')
def setup():
    if CONFIGURED:
        return redirect(url_for('index'))
    return render_template('setup.html')

@app.route('/configure', methods=['POST'])
def configure():
    print(request.form)
    
    username = request.form['username']
    userpw = request.form['pw']

    dburl = request.form['dburl']
    dbport = request.form['dbport']

    dbuser = request.form['dbusername']
    dbpw = request.form['dbpw']

    cachedburl = request.form['cachedburl']
    cachedbport = request.form['cachedbport']
    cachedbuser = request.form.get('cachedbusername')
    cachedbpw = request.form.get('cachedbpw')

    if not check_pg_db_con(dburl, dbport, dbuser, dbpw):
        return redirect(url_for('setup')) 
    if not check_cache_db_con(cachedburl, cachedbport, cachedbuser, cachedbpw):
        print("NO CACHE DB")
        return redirect(url_for('setup')) 

    # Configure Application

    # Update Database Config
    updated_pg = update_pg_conf(dburl, dbport, dbuser, dbpw)
    updated_redis = update_redis_conf(cachedburl, cachedbport, cachedbuser, cachedbpw)

    if not updated_pg or not updated_redis:
        return redirect(url_for('setup')) 

    setup_database()
    setup_user(username, userpw)

    global CONFIGURED
    CONFIGURED = True

    return redirect(url_for('index')) 

@app.route('/listeners/add/webtrack')
def add_webtrack_listener():

    return render_template('add_webtrack.html')

@app.route('/listeners', methods=['GET'])
def listeners():

    return render_template('listeners.html')

def check_database():
    conf = get_pg_conf()
    global CONFIGURED

    CONFIGURED = False

    if check_pg_db_con(conf[0], conf[1], conf[2], conf[3]):
        CONFIGURED = True
    
    if is_configured():
        CONFIGURED = True

def startup_routine():
    load_config()
    check_database()

    startup_routine()

if __name__ == "__main__":
    app.run()
