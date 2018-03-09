import argparse
import sys

from db import conn


def create_experiment_group(name, description):
    cursor = conn.cursor()
    cursor.execute('INSERT INTO experiment_groups(name, description) VALUES (?, ?)', (name, description))
    conn.commit()
    cursor.close()


def list_experiment_groups():
    cursor = conn.cursor()
    for row in cursor.execute('SELECT * from experiment_groups'):
        print('\t'.join(map(str, row)))
    cursor.close()


def query(select, select_json_fields, where, where_json_conds, end_query):
    """
    This is currently a bit hacky - white space sensitive.
    """
    cursor = conn.cursor()
    select = select.strip()
    if len(select_json_fields) == 0:
        select_query = select
        if len(select) == 0:
            select_query = '*'
    else:
        select_json_columns = list(map(lambda s: s.strip(), select_json_fields.split(',')))
        select_json_query = ','.join([f"json_extract(args, '$.{k}') as {k}" for k in select_json_columns])
        select_query = select_json_query if not len(select) else select + ',' + select_json_query

    where = where.strip()
    if len(where_json_conds) == 0:
        where_query = where
        if len(where) == 0:
            where_query = '1'
    else:
        json_clauses = list(map(lambda s: s.strip(), where_json_conds.split(',')))
        json_clause_parts = [c.split(' ') for c in json_clauses]  # each part should have length 3: operand1 operator operand2
        json_filter_query = ' AND '.join([f"json_extract(args, '$.{k}') {op} {v}" for (k, op, v) in json_clause_parts])
        where_query = json_filter_query if not len(where) else where + ' AND ' + json_filter_query

    overall_query = f'SELECT {select_query} FROM experiments WHERE {where_query} {end_query}'
    print('Query:', overall_query)
    res = cursor.execute(overall_query)
    for row in res:
        print('\t'.join(map(str, row)))
    cursor.close()


def delete_experiment(criteria):
    """
    Delete experiment by some criteria.
    NOTE: watermill is meant for personal use so THIS DOES NOT HANDLE SQL INJECTION ATTACKS.
    """
    cursor = conn.cursor()
    cursor.execute(f'DELETE FROM experiments WHERE {criteria}')
    conn.commit()


def delete_experiment_group(name):
    cursor = conn.cursor()
    cursor.execute('DELETE FROM experiment_groups WHERE name=?', (name,))
    conn.commit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CLI for querying and managing experiments')
    parser.add_argument('command', choices=['create_group', 'query', 'list_groups', 'delete', 'delete_group'])
    parser.add_argument('args', nargs='*', help='arguments depending on the command')
    args = parser.parse_args()

    action = args.command
    params = args.args

    if action == 'create_group':
        if len(params) != 2:
            print('Usage: create_group [name] [description]')
            sys.exit(1)

        create_experiment_group(*params)
    elif action == 'query':
        if len(params) != 5:
            print('Usage: query [select] [select_json_fields] [where] [where_json_conds] [end_query]')
            sys.exit(1)

        query(*params)
    elif action == 'list_groups':
        list_experiment_groups()
    elif action == 'delete':
        if len(params) != 1:
            print('Usage: delete [query]')
            print('query is a SQL filter for the WHERE clause of experiments')
            sys.exit(1)

        delete_experiment(params[0])
    elif action == 'delete_group':
        if len(params) != 1:
            print('Usage: delete [experiment_group_name]')
            sys.exit(1)

        delete_experiment_group(params[0])
