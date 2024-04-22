import sqlite3

def record_info(user_send, tagged_user, msg_content):

    conn = sqlite3.connect('line_bot.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO messages (user_id, message, tagged_users) VALUES (?, ?, ?)",
                (user_send, msg_content, ','.join(tagged_user)))
        
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

def view_table_content(table_name):
    conn = sqlite3.connect('line_bot.db')
    c = conn.cursor()
    
    query = f"SELECT * FROM {table_name};"
    
    try:
        c.execute(query)
        rows = c.fetchall()
        for row in rows:
            print(row)
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()


def view_table_content_with_headers(table_name):
    conn = sqlite3.connect('line_bot.db')
    c = conn.cursor()
    
    try:
        c.execute(f"PRAGMA table_info({table_name});")
        columns = [description[1] for description in c.fetchall()]
        print("Column Names:", columns)

        c.execute(f"SELECT * FROM {table_name};")
        rows = c.fetchall()
        for row in rows:
            print(row)
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()


# summary