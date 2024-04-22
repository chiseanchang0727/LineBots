import sqlite3


def execute_sql(sql, params=None):
    conn = sqlite3.connect('line_bot.db')
    c = conn.cursor()
    try:
        if params:
            c.execute(sql, params)
        else:
            c.execute(sql)
        conn.commit()
    except sqlite3.OperationalError as e:
        print("SQL Error:", e)
        print("Failed SQL:", sql)
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



# summary