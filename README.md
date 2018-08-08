# Sheet2db

Sheet2db is a tiny python library for one-way syncing the Google spreadsheet to database. (Currently, it supports only MySQL)

It is useful for managing some static data on Google spreadsheet, but also want to sync the sheet data to database.

***Sheet2db DOES NOT collect any your secret values!***

# Installation

```
pip install sheet2db
```

# Usage

> You must have API key which is accessible to Google Spreadsheet API

Example sheet format (**items** tab):

````
===========================
|  A |    B |     C |   D |
===========================
| id | name | count | ver |
|----|------|-------|-----|
| .. | .... | ..... | ... |
===========================
````

Following example will sync **items** tab of **1U3un2ZJPRhLrWzc2DMXq8VI7Nqf9pYlajfO4mQVCZpE** spreadsheet to database:

```python
from sheet2db import Sheet2db

# Provide API key
syncer = Sheet2db('AIzaSyC6pabjqmaPiguYoHbq4W7a0DV0wQg5JGk')

# Fetch data from spreadsheet
syncer.fetch(
    sheet = '1U3un2ZJPRhLrWzc2DMXq8VI7Nqf9pYlajfO4mQVCZpE',
    tab = 'items',
    range = 'A1:D')

# Sync fetched data to database (mysql)
syncer.sync(
    host = '192.168.168.10',
    port = 3306,
    user = 'mingrammer',
    password = 'p@ssw0rd',
    db = 'static',
    table = 'items')
```

You can also use ssh tunneling to access to remote database with **sshtunnel**

```python
with sshtunnel.SSHTunnelForwarder(
    ('db.service.io', 22),
    ssh_username='ssh_user'
    ssh_pkey='~/.ssh/id_rsa'
    ssh_private_key_password='ssh_pk_password',
    remote_bind_address=('localhost', 3306),
) as tunnel:
    syncer.sync(
        host = tunnel.local_bind_host,
        port = tunnel.local_bind_host,
        user = 'mingrammer',
        password = 'p@ssw0rd',
        db = 'static',
        table = 'items')
```

# License

MIT
