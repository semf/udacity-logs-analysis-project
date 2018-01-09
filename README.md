# Udacity Logs Analysis Project

## Quick start guide
- create view table before running python file. After connecting to the news
database, run the following code.
```sql
 create view viewer as
 select split_part(path,'/',3) as slug, count(*) as views
 from log where status='200 OK'
 group by path, status order by views desc offset 1;

 create view responseok as
 select date_trunc('day', time) as "day", count(*) as num
 from log where status='200 OK' group by 1 order by 1;

 create view responsefail as
 select date_trunc('day', time) as "day", count(*) as num
 from log where status='404 NOT FOUND' group by 1 order by 1;
 ```

 - And then run news.py `python news.py`
