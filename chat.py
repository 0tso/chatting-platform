import db
import user

def create_chat_with_user(username):
    with db.Connection() as cur:

        # Check if a private chat already exists, add only if it doesn't
        cur.execute("SELECT chat_id FROM ChatMembers GROUP BY chat_id HAVING COUNT(CASE WHEN user_id NOT IN (SELECT id FROM Users WHERE name IN (%s, %s)) = TRUE THEN 1 END) = 0;",
                    (user.username(), username))
        if (id := cur.fetchone()):
            return id[0]

        cur.execute("INSERT INTO Chats (name) VALUES (NULL) RETURNING id;")
        new_chat_id = cur.fetchone()[0]
        print(f"new_chat_id: {new_chat_id}")
        cur.execute("INSERT INTO ChatMembers (chat_id, user_id) SELECT %s, id FROM Users WHERE name IN (%s, %s);",
                    (new_chat_id, user.username(), username))
        return new_chat_id

def get_chat_users(chat_id):
    with db.Connection() as cur:
        cur.execute("SELECT U.name FROM Users U, ChatMembers C WHERE C.chat_id=%s AND C.user_id=U.id", (chat_id,))
        return [x[0] for x in cur.fetchall()]