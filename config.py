import json

CONFIG = None

def load_config():

    global CONFIG

    with open("config.json", "r") as f:
        CONFIG = json.load(f)

    print(CONFIG)
    
def save_config():
    print("SAVING CONFIG")
    try:

        with open("config.json", "w") as f:
            json.dump(CONFIG, f, indent=4)

    except Exception as e:
        print(str(e))
        return False
    
    return True

def update_pg_conf(url, port, username, password):
    print("XXX", port)
    CONFIG["database"]["postgres"]["url"] = url
    CONFIG["database"]["postgres"]["port"] = port
    CONFIG["database"]["postgres"]["username"] = username
    CONFIG["database"]["postgres"]["password"] = password
    
    return save_config()

def update_redis_conf(url, port, username=None, password=None):

    CONFIG["database"]["redis"]["url"] = url
    CONFIG["database"]["redis"]["port"] = port
    if username:
        CONFIG["database"]["redis"]["username"] = username
    if password:
        CONFIG["database"]["redis"]["password"] = password

    return save_config()

def get_pg_conf():
    pgconf = CONFIG["database"]["postgres"]

    details = (pgconf.get("url"), pgconf.get("port"), pgconf.get("username"), pgconf.get("password"))

    return details

def get_redis_conf():
    redisconf = CONFIG["database"]["redis"]

    details = (redisconf.get("url"), redisconf.get("port"), redisconf.get("username"), redisconf.get("password"))

    return details
