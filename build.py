import sqlite3
from queries import *

def main():
    db = sqlite3.connect('social.db')
    with db:
        make_accounts(db)

def make_accounts(db):
    add_account(db, 'firstpost')

main()
