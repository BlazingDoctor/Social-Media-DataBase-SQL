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

    def show_likes_for_user(self, username, post_id=None):
        # Verify the user exists
        self.cursor.execute("SELECT account_id FROM Accounts WHERE username = ?", (username,))
        account = self.cursor.fetchone()
        if not account:
            print(f"Account not found: {username}")
            return
        account_id = account[0]
        # Get all posts that this user has liked with post content and original poster
        self.cursor.execute("""
            SELECT p.post_id, p.content, a.username as post_author, p.timestamp
            FROM Likes l
            JOIN Posts p ON l.post_id = p.post_id
            JOIN Accounts a ON p.account_id = a.account_id
            WHERE l.account_id = ?
            ORDER BY p.timestamp DESC
        """, (account_id,))
        
        liked_posts = self.cursor.fetchall()
        
        if not liked_posts:
            print(f"{username} hasn't liked any posts yet.")
            return
        print(f"Posts liked by {username}:")
        for post in liked_posts:
            post_id, content, post_author, timestamp = post
            print(f"- Post {post_id} by {post_author} at {timestamp}")
            print(f"  Content: {content}")
            print() #/n    


    def get_posts_for_user(self, username):
        # Verify the user exists
        self.cursor.execute("SELECT account_id FROM Accounts WHERE username = ?", (username,))
        account = self.cursor.fetchone()
        if not account:
            print(f"Account not found: {username}")
            return
        account_id = account[0]

        self.cursor.execute("""
            SELECT p.post_id, p.content, a.username as post_author, p.timestamp
            FROM Posts p
            JOIN Accounts a ON p.account_id = a.account_id
            WHERE p.account_id = ?
            ORDER BY p.timestamp DESC
        """, (account_id,))
        
        user_posts = self.cursor.fetchall()
        
        if not user_posts:
            print(f"{username} hasn't posted yet.")
            return
        print(f"Posts authored by {username}:")
        for post in user_posts:
            post_id, content, post_author, timestamp = post
            print(f"- Post {post_id} by {post_author} at {timestamp}")
            print(f"  Content: {content}")
            print() #/n    


    def check_post_liked(self, username, post_id):
         # Verify the user exists
        self.cursor.execute("SELECT account_id FROM Accounts WHERE username = ?", (username,))
        account = self.cursor.fetchone()
        if not account:
            print(f"Account not found: {username}")
            return
        account_id = account[0]
        #check if post was liked by user
        if post_id:
            self.cursor.execute("""
                SELECT 1
                FROM Likes
                WHERE account_id = ? AND post_id = ?
            """, (account_id, post_id))
            
            liked = self.cursor.fetchone()
            if liked:
                print(f"{username} has liked post {post_id}")
            else:
                print(f"{username} has not liked post {post_id}")
            return

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

    """Brooke's interesting query which sees how many likes are on a post and tells what accounts liked it"""
    def get_post_likes(self, post_id):
        # Verify the post exists
        self.cursor.execute("SELECT post_id FROM Posts WHERE post_id = ?", (post_id,))
        post = self.cursor.fetchone()
        if not post:
            print("Post not found for get_post_likes")
            return
        post_id = post[0]
        """Retrieve all likes on a specific post, showing who liked it."""
        self.cursor.execute("""
            SELECT Likes.like_id, Accounts.username 
            FROM Likes
            JOIN Accounts ON Likes.account_id = Accounts.account_id
            WHERE Likes.post_id = ?;
        """, (post_id,))
        
        likes = self.cursor.fetchall()
        
        if not likes:
            print(f"No likes found for post {post_id}.")
            return []

        return [{"like_id": like[0], "liked_by": like[1]} for like in likes]
	
   

    def close(self):
        self.conn.close()