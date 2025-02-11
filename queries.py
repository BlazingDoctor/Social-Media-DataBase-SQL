def add_account(db, username):
    db.execute(f"INSERT INTO accounts (username) VALUES (?)", (username,))
