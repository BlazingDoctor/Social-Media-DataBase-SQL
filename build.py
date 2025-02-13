import sqlite3
import subprocess
from queries import *

DB_NAME = 'social.db'
SCHEMA_FILE = 'schema.sql'
def main():
    subprocess.run(["rm", "-f", DB_NAME], check=True)
    subprocess.run(["rm", "-rf", '__pycache__'], check=True)
    subprocess.run(f"sqlite3 {DB_NAME} < {SCHEMA_FILE}", shell=True, check=True)
    db = sqlite3.connect(DB_NAME)
    with db:
        make_accounts(db)

def make_accounts(db):
    add_account(db, 'secondpost')

main()
