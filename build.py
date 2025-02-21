import sqlite3
import subprocess
from queries import SocialNetwork

DB_NAME = 'social.db'
SCHEMA_FILE = 'schema.sql'

def main():
    # Remove old database and cache
    subprocess.run(["rm", "-f", DB_NAME], check=True)
    subprocess.run(["rm", "-rf", '__pycache__'], check=True)

    # Rebuild database schema
    subprocess.run(f"sqlite3 {DB_NAME} < {SCHEMA_FILE}", shell=True, check=True)

    # Populate database with test data
    populate_database()

def populate_database():
    """Creates sample users, accounts, follows, posts, etc."""
    social = SocialNetwork(DB_NAME)

    # Create users
    social.create_user("jane.doe@utahtech.edu")
    social.create_user("john.smith@utahtech.edu")
    social.create_user("alice.jones@utahtech.edu")

    # Create accounts
    social.create_account("jane.doe@utahtech.edu", "jane_d")
    social.create_account("john.smith@utahtech.edu", "johnny")
    social.create_account("alice.jones@utahtech.edu", "alicej")

    # Follow relationships
    social.follow_account("jane_d", "johnny")
    social.follow_account("johnny", "alicej")
    social.follow_account("alicej", "jane_d")

    # Create posts
    social.create_post("jane_d", "Hello world!")
    social.create_post("johnny", "Excited to be here!")
    social.create_post("alicej", "Loving this platform!")

    # Like posts
    social.like_post("johnny", 1)
    social.like_post("alicej", 1)
    social.like_post("jane_d", 2)

    # Report a post
    social.report_post("alicej", 2, "Spam content")

    # Close connection
    social.close()

if __name__ == "__main__":
    main()

