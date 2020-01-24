# dtables
SQLA Python to jquery datatables.

Thie module provides a framework to automatically create a scrolling dynamic table on a web browser using the jquery-datatables browser library by instrospecing tables, fields and data types from a database.

This module is more focussed on performance and ease of use than having a fancy UI. Filtering, sorting and paging are all done on the server side by building server side queries on front end actions.

There are no data size limits as long as the generated queries do not ask for too much data. This code works easily with tables having hundreds of millions of rows.

What you need to test this is a basic database as described in schema.py and a url to this database
in settings.ini
```
[database]
connection=mysql://rfo:verysecret@localhost/mydatabase
```

Then make a virtualenv and install requirements.txt
The run app.py
