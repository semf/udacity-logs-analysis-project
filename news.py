#!/usr/bin/env python

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
    print("What are the most popular three articles of all time?")
    get_popular_article(3)
    print("\nWho are the most popular article authors of all time?")
    get_popular_author()
    print("\nOn which days did more than 1% of requests lead to errors?")
    error_ratio(1)
