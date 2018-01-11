#!/usr/bin/env python

import psycopg2

DBNAME = "news"


if __name__ == "__main__":
    db = psycopg2.connect(database=DBNAME)
    print("connecting msg:",db)
    c = db.cursor()
    c.execute('''create view viewer as select split_part(path,'/',3)
    as slug, count(*) as views
    from log where status='200 OK'
    group by path, status order by views desc offset 1;''')
    c.execute('''create view responseok as
    select date_trunc('day', time) as "day", count(*) as num
    from log where status='200 OK' group by 1 order by 1;''')
    c.execute('''create view responsefail as
    select date_trunc('day', time) as "day", count(*) as num
    from log where status='404 NOT FOUND' group by 1 order by 1;''')
    db.commit()
    db.close()
