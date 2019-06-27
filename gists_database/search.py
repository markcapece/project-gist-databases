from .models import Gist


def search_gists(db_connection, **kwargs):
    # Setup arguments
    db_conn = db_connection

    input_args = kwargs.copy()
    input_keys = input_args.keys()

    params = {}
    string_list = []

    # Parse kwargs into params and string_list
    for k in input_keys:
        if k == 'github_id':
            params['github_id'] = input_args[k]
            string_github = 'github_id = :github_id'
            string_list.append(string_github)

        if k.startswith('created_at'):
            params['created_at'] = input_args[k]
            string_created = 'datetime(created_at) {} datetime(:created_at)'
            if k.endswith('lte'):
                string_created = string_created.format('<=')
            elif k.endswith('lt'):
                string_created = string_created.format('<')
            elif k.endswith('gte'):
                string_created = string_created.format('>=')
            elif k.endswith('gt'):
                string_created = string_created.format('>')
            else:
                string_created = string_created.format('==')
            string_list.append(string_created)

        if k.startswith('updated_at'):
            params['updated_at'] = input_args[k]
            string_updated = 'datetime(updated_at) {} datetime(:updated_at)'
            if k.endswith('lte'):
                string_updated = string_updated.format('<=')
            elif k.endswith('lt'):
                string_updated = string_updated.format('<')
            elif k.endswith('gte'):
                string_updated = string_updated.format('>=')
            elif k.endswith('gt'):
                string_updated = string_updated.format('>')
            else:
                string_updated = string_updated.format('==')
            string_list.append(string_updated)

    # Construct SQL command string
    base_string = 'SELECT * FROM gists'
    if len(string_list) > 0:
        base_string += ' WHERE '
    conditional_string = ' AND '.join(string_list)
    execute_string = base_string + conditional_string

    # Execute SQL command and return retrieved entries
    cursor = db_conn.execute(execute_string, params)
    return [Gist(entry) for entry in cursor.fetchall()]
