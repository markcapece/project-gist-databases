import requests


BASE_URL = 'https://api.github.com/users/'


def import_gists_to_database(db, username, commit=True):
    url = BASE_URL + username + '/gists'
    response = requests.get(url)

    if response.status_code != 200:
        raise requests.exceptions.HTTPError

    jresp = response.json()

    gitlist = [
        (
            idx,
            entry['id'],
            entry['html_url'],
            entry['git_pull_url'],
            entry['git_push_url'],
            entry['commits_url'],
            entry['forks_url'],
            int(bool(entry['public'])),
            entry['created_at'],
            entry['updated_at'],
            int(entry['comments']),
            entry['comments_url']
        )
        for idx, entry in enumerate(jresp)
    ]

    if commit:
        with open('schema.sql', 'r') as f:
            schema = f.read()

        db_conn = db
        db_conn.executescript(schema)

        for element in gitlist:
            db_conn.execute('INSERT INTO gists VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', element)
