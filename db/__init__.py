import configparser
import os
import sqlite3

config = configparser.ConfigParser()
config.read('config.ini')

conn = sqlite3.connect('watermill.db', check_same_thread=False)
conn.enable_load_extension(True)
conn.load_extension(config['DEFAULT']['json1'])


def delete_experiment_row(stdout_fn, stderr_fn):
    try:
        os.remove(f'log/{stdout_fn}')
        os.remove(f'log/{stderr_fn}')
    except OSError:
        pass

conn.create_function('delete_experiment_row', 2, delete_experiment_row)

c = conn.cursor()
c.execute('PRAGMA foreign_keys=on')

# Create tables if this is the first time
res = c.execute("SELECT name from sqlite_master where type='table' and name='experiment_groups'")
if res.fetchone() is None:
    c.execute('''CREATE TABLE experiment_groups(gid integer primary key autoincrement, name text, description text)''')
    c.execute('''INSERT INTO experiment_groups(name, description) VALUES ('adhoc', 'ad-hoc experiment group')''')

    c.execute('''CREATE TABLE experiments(group_id integer, args text, stdout text, stderr text, status_code int,
                  start_time text, end_time text, train_metric text, dev_metric text, test_metric text,
                  FOREIGN KEY(group_id) REFERENCES experiment_groups(gid) ON DELETE CASCADE)''')

    c.execute('''CREATE TRIGGER del_logs AFTER DELETE ON experiments
                  FOR EACH ROW BEGIN SELECT delete_experiment_row(OLD.stdout, OLD.stderr); END''')

conn.commit()
