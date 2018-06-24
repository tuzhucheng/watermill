# watermill
Automated machine learning experimentation workflow on GPU

This code is currently in alpha. Changes occur quickly and compatibility may break at any time.

## Setup

Create a `config.ini` file with your own settings.
```
[DEFAULT]
json1 = /u/z3tu/projects/watermill/json1
```

To query JSON using the `json1` extension. You can get the extension by running `get_json1.sh` (make you have required headers before installing, i.e. `sudo apt-get install libsqlite3-dev`).

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

## Demo

Querying the model that performs the best on the validation set for model selection.
```sql
sqlite> select rowid,
json_extract(args, '$.arch') as arch, json_extract(args, '$.dataset') as dataset,
json_extract(args, '$.dropout') as dropout,
json_extract(args, '$.sparse_features') as sparse,
json_extract(args, '$.attention') as attention,
json_extract(args, '$.wide_conv') as wide,
dev_metric
from experiments where group_id=27 and dataset='trecqa' and arch='mpcnn_no_per_dim_no_multi_pooling'
order by json_extract(dev_metric, '$.cross_entropy_loss') asc limit 5;
1738|mpcnn_no_per_dim_no_multi_pooling|trecqa|||basic|1|{"cross_entropy_loss": 0.4985522381834612, "map": 0.7363, "mrr": 0.8013}
1819|mpcnn_no_per_dim_no_multi_pooling|trecqa|0||basic|1|{"cross_entropy_loss": 0.5391504070859139, "map": 0.7501, "mrr": 0.8367}
1704|mpcnn_no_per_dim_no_multi_pooling|trecqa|||basic|1|{"cross_entropy_loss": 0.549805790052525, "map": 0.7064, "mrr": 0.7467}
2156|mpcnn_no_per_dim_no_multi_pooling|trecqa|0||none||{"cross_entropy_loss": 0.5713172829780818, "map": 0.772, "mrr": 0.8467}
1817|mpcnn_no_per_dim_no_multi_pooling|trecqa|0||basic|1|{"cross_entropy_loss": 0.5848681800794473, "map": 0.7266, "mrr": 0.7892}
```
