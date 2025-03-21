import configparser

config = configparser.ConfigParser()
config.read("./database/database.ini")

DB_CONFIG = {
    "dbname": config["postgres"]["database"],
    "user": config["postgres"]["user"],
    "password": config["postgres"]["password"],
    "host": config["postgres"]["host"],
}


