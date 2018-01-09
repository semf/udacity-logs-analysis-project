#!/usr/bin/env python
"""
PLEASE CREATE VIEW before running this module
create view viewer as select split_part(path,'/',3) as slug, count(*) as views
from log where status='200 OK'
group by path, status order by views desc offset 1;
create view responseok as
select date_trunc('day', time) as "day", count(*) as num
from log where status='200 OK' group by 1 order by 1;
create view responsefail as
select date_trunc('day', time) as "day", count(*) as num
from log where status='404 NOT FOUND' group by 1 order by 1;
"""

import psycopg2

DBNAME = "news"


def get_popular_article(num):
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute('''
    SELECT title, views FROM articles JOIN viewer
    ON articles.slug = viewer.slug LIMIT %s ;''', (num,))
    data = c.fetchall()
    db.close()
    for article in data:
        print("%s - %i views" % (article[0], article[1]))
    return data


def get_popular_author():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute('''
    SELECT name, sum FROM authors JOIN (SELECT author,sum(views)
    FROM articles JOIN viewer ON articles.slug = viewer.slug
    GROUP BY author ORDER BY sum desc) AS t ON authors.id = t.author;
    ''')
    data = c.fetchall()
    db.close()
    for authors in data:
        print("%s - %i views" % (authors[0], authors[1]))
    return data


def error_ratio(more_than):
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute('''
    SELECT o.day, (f.num*100.0)/o.num AS percent
    FROM responseok AS o LEFT JOIN responsefail AS f ON o.day = f.day
    WHERE (f.num*100.0)/o.num > %s ;''', (more_than,))
    data = c.fetchall()
    db.close()
    for log in data:
        print("%s - %.1f" % (log[0].strftime('%B %d, %y'), log[1]) + "%errors")
    return data


if __name__ == "__main__":
    get_popular_article(3)
    get_popular_author()
    error_ratio(1)
