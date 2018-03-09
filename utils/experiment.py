from db import conn


def delete_experiment(criteria):
    """
    Delete experiment by some criteria.
    NOTE: watermill is meant for personal use so THIS DOES NOT HANDLE SQL INJECTION ATTACKS.
    """
    cursor = conn.cursor()
    cursor.execute(f'DELETE FROM experiments WHERE {criteria}')
    conn.commit()
