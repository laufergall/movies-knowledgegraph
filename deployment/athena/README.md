
# Queries

In [Athena](https://docs.aws.amazon.com/athena/latest/ug/getting-started.html), we perform queries to parse our jsons (stored in S3 with scraped data).

&#8594; Go through Athena Walkthrough (next section) if you have not yet, to define our database, tables and views.

&#8594; To view today's scraped data:

```sql
MSCK REPAIR TABLE cinemas;
```

```sql
select cinema, title, showtime
FROM v_cinemas
WHERE title LIKE '%Aladdin%';
```

With this sample query, we get a table with three rows:
* cinema (name of cinema)
* title (movie title which contains `Aladdin`: `Aladdin`, `Aladdin (OmU)` and `Aladdin 3D`)
* showtime (day and time for the show, formatted as `dd.MM HH:mm`)


# Athena Walkthrough

Here is how we defined our database, table, and view.

&#8594; Create database, named `kinoprogramm`:

```sql
CREATE DATABASE kinoprogramm
```

&#8594; Create table, named `cinemas`:

```sql
CREATE EXTERNAL TABLE cinemas (
    name string,
    description string,
	shows array<
		struct<title: string,
               times: array<string> >>
)
PARTITIONED BY ( 
    year string, 
    month string, 
    day string)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
LOCATION 's3://kinoprogramm-scraper/berlin-de/';
```

&#8594; Load all partitions to be able to query data:

```sql
MSCK REPAIR TABLE cinemas;
```

&#8594; Create view, named `v_cinemas`. This is the view we will query to see today's scraped movies and show times.

```sql
CREATE OR REPLACE VIEW v_cinemas AS 
SELECT name as cinema, 
  description, 
  title, 
  format_datetime(date_parse(showtimes, '%Y-%m-%dT%H:%i:%s'), 'dd.MM HH:mm') as showtime
FROM
  (
       SELECT
         name, description, sdesc.title, sdesc.times
       FROM
     (
       (
      SELECT *
      FROM
        cinemas
      WHERE (date(date_parse(concat(year, month, day), '%Y%m%d')) = current_date)
      )
   CROSS JOIN UNNEST(shows) t(sdesc)
     )
 )
CROSS JOIN UNNEST(times) t(showtimes)
```


# References

* [Tables from nested jsons](https://aws.amazon.com/blogs/big-data/create-tables-in-amazon-athena-from-nested-json-and-mappings-using-jsonserde/)
* [Flattening arrays](https://docs.aws.amazon.com/athena/latest/ug/flattening-arrays.html)
* [Presto date_parse](https://prestosql.io/docs/current/functions/datetime.html#date_parse)
