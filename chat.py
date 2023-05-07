import db
import user
from flask import session


def create_chat_with_user(username):
    with db.Connection() as cur:

        # Check if a private chat already exists, add only if it doesn't
        cur.execute("SELECT chat_id FROM ChatMembers GROUP BY chat_id HAVING COUNT(CASE WHEN user_id NOT IN (SELECT id FROM Users WHERE name IN (%s, %s)) = TRUE THEN 1 END) = 0;",
                    (user.username(), username))
        if (id := cur.fetchone()):
            chat_id = id[0]
            cur.execute("SELECT 1 FROM ChatGroupChats CGC, ChatGroups CG WHERE CG.id=CGC.chat_group_id AND CG.user_id=%s AND CGC.chat_id=%s",
                        (user.user_id(), chat_id))
            if not cur.fetchone():
                cur.execute("INSERT INTO ChatGroupChats (chat_group_id, chat_id) SELECT id, %s FROM ChatGroups WHERE user_id=%s ORDER BY index ASC LIMIT 1",
                            (chat_id, user.user_id()))
            return chat_id

        cur.execute("INSERT INTO Chats (name) VALUES (NULL) RETURNING id;")
        new_chat_id = cur.fetchone()[0]
        cur.execute("INSERT INTO ChatMembers (chat_id, user_id) SELECT %s, id FROM Users WHERE name IN (%s, %s);",
                    (new_chat_id, user.username(), username))

        # ATTENTION: Assumes both indices are 0, thus "ORDER BY index LIMIT 2"
        cur.execute("""
            INSERT INTO
                ChatGroupChats (chat_group_id, chat_id)
            SELECT
                CG.id, %s
            FROM
                ChatGroups CG, Users U
            WHERE
                CG.user_id=U.id and U.name IN (%s, %s)
            ORDER BY
                CG.index ASC
            LIMIT 2""", 
            (new_chat_id, username, user.username()))

        return new_chat_id

def get_chat_users(chat_id):
    with db.Connection() as cur:
        cur.execute("SELECT U.name, U.id, C.present FROM Users U, ChatMembers C WHERE C.chat_id=%s AND C.user_id=U.id", (chat_id,))
        return cur.fetchall()

def get_chats():
    with db.Connection() as cur:
        cur.execute("""
            SELECT
                CG.id, CG.name, C.id, COALESCE(C.name, U.name)
            FROM
                ChatGroups CG, ChatGroupChats CGC, Chats C, ChatMembers CM1, ChatMembers CM2, Users U
            WHERE
                CG.user_id=%(user_id)s AND CG.id=CGC.chat_group_id AND CGC.chat_id=C.id
            AND 
                C.id=CM1.chat_id AND C.id=CM2.chat_id AND CM1.user_id=%(user_id)s AND CM2.user_id != %(user_id)s AND U.id=CM2.user_id
            ORDER BY
                CG.index ASC""",
            {"user_id": user.user_id()})
        chats = cur.fetchall()
        ret = []
        for group_id, group_name, chat_id, chat_name in chats:
            if (len(ret) == 0) or (ret[-1][0] != group_id):
                ret.append((group_id, group_name, []))
            
            ret[-1][2].append((chat_id, chat_name))

        return ret

def hide_chat(chat_id):
    with db.Connection() as cur:
        cur.execute("DELETE FROM ChatGroupChats CGC USING ChatGroups CG WHERE CGC.chat_group_id=CG.id AND CG.user_id=%s AND CGC.chat_id=%s",
            (user.user_id(), chat_id))

def is_chat_member(user_id, chat_id):
    with db.Connection() as cur:
        cur.execute("SELECT 1 FROM ChatMembers WHERE chat_id=%s and user_id=%s", (chat_id, user_id))
        return (True if cur.fetchone() else False)

def join_chat(chat_id):
    if is_chat_member(user.user_id(), chat_id):
        session["chat_id"] = chat_id
        return True
    else:
        return False

def leave_chat(chat_id):
    session["chat_id"] = chat_id

def get_current_chat_id():
    return session["chat_id"]

def has_auth(chat_id, user_id):
    with db.Connection() as cur:
        cur.execute("SELECT user_id FROM ChatMembers WHERE chat_id=%s AND user_id=%s", (chat_id, user_id))
        if cur.fetchone():
            return True
        else:
            return False

def set_present(chat_id, user_id, present=True):
    with db.Connection() as cur:
        cur.execute("UPDATE ChatMembers SET present=%s WHERE chat_id=%s AND user_id=%s;", (present, chat_id, user_id))

def get_present(chat_id):
    with db.Connection() as cur:
        cur.execute("SELECT user_id FROM ChatMembers WHERE chat_id=%s AND present=TRUE;", (chat_id,))
        return [x[0] for x in cur.fetchall()]

def get_messages(chat_id, amount, pivot_message_id=None):
    with db.Connection() as cur:
        if not pivot_message_id:
            pivot_message_id = 2147483647

        cur.execute("""
            SELECT
                M.id, TO_CHAR(M.time, 'YYYY-MM-DD HH24:MI:SS'), U.name, M.content
            FROM
                Messages M LEFT JOIN Users U
            ON
                M.user_id=U.id
            WHERE
                M.chat_id = %s AND M.id < %s
            ORDER BY
                M.id DESC
            LIMIT %s""", (chat_id, pivot_message_id, amount))
        return cur.fetchall()

def add_message(chat_id, user_id, content):
    with db.Connection() as cur:
        cur.execute("""
            INSERT INTO
                Messages (chat_id, user_id, time, content)
            VALUES
                (%s, %s, NOW(), %s)
            RETURNING
                id, TO_CHAR(time, 'YYYY-MM-DD HH24:MI:SS')""", (chat_id, user_id, content))
        return cur.fetchone()