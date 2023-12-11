# - *- coding: utf- 8 - *-
import configparser

config = configparser.ConfigParser()
config.read("settings.ini", encoding='utf-8')
BOT_TOKEN = config["settings"]["token"]
main_admin = config["settings"]["main_admin"]
bot_description = config["settings"]["bot_description"]


pay = configparser.ConfigParser()
pay.read("settings.ini", encoding="utf-8")

curency =  "RUB "
change_hwid_price = 250
bot_version = "0.1"
sticker_agreement = "CAACAgIAAxkBAAEKZF9lEhAtlcr_NoKMAXPAXbz7TRLZJgACgRMAAjrNaUtsywABz5O_dm8wBA"
api_zelenka = "5588f516f493a204d5d6584d8507d442f3fe498f"
id_zelenka = "wwdx7mv85x"
login_zelenka = "samuel"
login_crystal = "(oasd90fiw98g932)"
crystal_secret = "0fe43777d51d8b5c2596e70c94702dda3c6483c1"
crystal_salt = "0ef8b9f40a894d9e4cb99af9a07c3c1b7c6bc8d7"
