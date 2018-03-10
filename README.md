# watermill
Automated machine learning experimentation workflow on GPU

This code is currently in alpha. Changes occur quickly and compatibility may break at any time.

## Setup

Create a `config.ini` file with your own settings.
```
[DEFAULT]
json1 = /u/z3tu/projects/watermill/json1
```

## Starting workers

This starts two workers, each can process 2 tasks at once.
```
celery -A task_queue worker --loglevel=INFO --concurrency=2 -n worker1 -Q gpu0
celery -A task_queue worker --loglevel=INFO --concurrency=2 -n worker2 -Q gpu1
```

## Querying

One can query using the SQLite shell:
```sql
$ sqlite3 watermill.db 
SQLite version 3.22.0 2018-01-22 18:45:57
Enter ".help" for usage hints.
sqlite> .load json1
sqlite> select json_extract(args, '$.arch'), json_extract(args, '$.program') from experiments limit 5;
```
