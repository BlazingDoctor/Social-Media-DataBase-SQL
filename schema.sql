-- Drop tables if they already exist (for reset purposes)
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Accounts;
DROP TABLE IF EXISTS Followers;
DROP TABLE IF EXISTS Posts;
DROP TABLE IF EXISTS Likes;
DROP TABLE IF EXISTS Reports;

-- Users table stores user information
CREATE TABLE Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL
);

-- Accounts table stores multiple accounts per user
CREATE TABLE Accounts (
    account_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    username TEXT UNIQUE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- Followers table tracks who follows whom
CREATE TABLE Followers (
    follower_id INTEGER NOT NULL,
    followed_id INTEGER NOT NULL,
    PRIMARY KEY (follower_id, followed_id),
    FOREIGN KEY (follower_id) REFERENCES Accounts(account_id) ON DELETE CASCADE,
    FOREIGN KEY (followed_id) REFERENCES Accounts(account_id) ON DELETE CASCADE
);

-- Posts table stores posts with timestamps
CREATE TABLE Posts (
    post_id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES Accounts(account_id) ON DELETE CASCADE
);

-- Likes table tracks which accounts like which posts
CREATE TABLE Likes (
    like_id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER NOT NULL,
    account_id INTEGER NOT NULL,
    FOREIGN KEY (post_id) REFERENCES Posts(post_id) ON DELETE CASCADE,
    FOREIGN KEY (account_id) REFERENCES Accounts(account_id) ON DELETE CASCADE
);

-- Reports table to allow users to report posts
CREATE TABLE Reports (
    report_id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER NOT NULL,
    account_id INTEGER NOT NULL,
    reason TEXT NOT NULL,
    FOREIGN KEY (post_id) REFERENCES Posts(post_id) ON DELETE CASCADE,
    FOREIGN KEY (account_id) REFERENCES Accounts(account_id) ON DELETE CASCADE
);

-- A dynamic view that shows Suggested Accounts to Follow
-- Actual special query because the one I made before was just a basic join
CREATE VIEW SuggestedFollows AS
WITH FollowedByUser AS (
    SELECT f1.follower_id, f2.followed_id
    FROM Followers f1
    JOIN Followers f2 ON f1.followed_id = f2.follower_id
    WHERE f1.follower_id <> f2.followed_id
)
SELECT a1.username AS user, a2.username AS suggested_user, COUNT(*) AS mutual_follows
FROM FollowedByUser fb
JOIN Accounts a1 ON fb.follower_id = a1.account_id
JOIN Accounts a2 ON fb.followed_id = a2.account_id
WHERE fb.followed_id NOT IN (SELECT followed_id FROM Followers WHERE follower_id = fb.follower_id)
GROUP BY a1.username, a2.username
ORDER BY mutual_follows DESC;
