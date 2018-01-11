# Udacity Logs Analysis Project

## Quick start guide
- To create view table before running python file.
run the following code in the folder where the newsdata.sql is located.

```sh
$python setting.py
$python news.py
```

## About the views
- viewer : This view has information about each articles viewer number
based on http get method of log table
- responseok : This view count the status code(200 OK) group by a day
- responsefail : This view count the status code(404 NOT FOUND) group by a day
