import sqlite3

conn = sqlite3.connect('watermill.db')

c = conn.cursor()

# Create tables if this is the first time
res = c.execute("SELECT name from sqlite_master where type='table' and name='experiment_groups'")
if res.fetchone() is None:
    c.execute('''CREATE TABLE experiment_groups(name text, description text)''')
    c.execute('''INSERT INTO experiment_groups(name, description) VALUES ('adhoc', 'ad-hoc experiment group')''')

    c.execute('''CREATE TABLE experiments(group_id integer, args text, stdout text, stderr text,
                  FOREIGN KEY(group_id) REFERENCES experiment_groups(rowid))''')
    conn.commit()
