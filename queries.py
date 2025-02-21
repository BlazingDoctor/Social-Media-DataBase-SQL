import sqlite3
from datetime import datetime

"""I got rid of the add_account function that was here before but feel free to add it again."""

class SocialNetwork:
    def __init__(self, db_name="social.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_user(self, email):
        """Creates a new user with the given email."""
        self.cursor.execute("INSERT INTO Users (email) VALUES (?)", (email,))
        self.conn.commit()
        print(f"User created: {email}")

    def create_account(self, email, username):
        """Creates a new account linked to a user email."""
        self.cursor.execute("SELECT user_id FROM Users WHERE email = ?", (email,))
        user = self.cursor.fetchone()
        if not user:
            print("User not found.")
            return
        user_id = user[0]
        self.cursor.execute("INSERT INTO Accounts (user_id, username) VALUES (?, ?)", (user_id, username))
        self.conn.commit()
        print(f"Account created: {username} for user {email}")

    def follow_account(self, follower, followed):
        """Adds a follow relationship between two accounts."""
        self.cursor.execute("SELECT account_id FROM Accounts WHERE username = ?", (follower,))
        follower_id = self.cursor.fetchone()
        self.cursor.execute("SELECT account_id FROM Accounts WHERE username = ?", (followed,))
        followed_id = self.cursor.fetchone()
        
        if not follower_id or not followed_id:
            print("One or both accounts not found.")
            return
        
        self.cursor.execute("INSERT INTO Followers (follower_id, followed_id) VALUES (?, ?)", (follower_id[0], followed_id[0]))
        self.conn.commit()
        print(f"{follower} is now following {followed}")

    def create_post(self, username, content):
        """Creates a post for a given account."""
        self.cursor.execute("SELECT account_id FROM Accounts WHERE username = ?", (username,))
        account = self.cursor.fetchone()
        if not account:
            print("Account not found.")
            return
        
        self.cursor.execute("INSERT INTO Posts (account_id, content, timestamp) VALUES (?, ?, ?)", (account[0], content, datetime.now()))
        self.conn.commit()
        print(f"Post created by {username}: {content}")

    def like_post(self, username, post_id):
        """Allows an account to like a post."""
        self.cursor.execute("SELECT account_id FROM Accounts WHERE username = ?", (username,))
        account = self.cursor.fetchone()
        if not account:
            print("Account not found.")
            return
        
        self.cursor.execute("INSERT INTO Likes (post_id, account_id) VALUES (?, ?)", (post_id, account[0]))
        self.conn.commit()
        print(f"{username} liked post {post_id}")

    def report_post(self, username, post_id, reason):
        """Allows an account to report a post."""
        self.cursor.execute("SELECT account_id FROM Accounts WHERE username = ?", (username,))
        account = self.cursor.fetchone()
        if not account:
            print("Account not found.")
            return
        
        self.cursor.execute("INSERT INTO Reports (post_id, account_id, reason) VALUES (?, ?, ?)", (post_id, account[0], reason))
        self.conn.commit()
        print(f"{username} reported post {post_id} for {reason}")

    def close(self):
        self.conn.close()
