# Log Analysis

## Description
An exercise for the Udacity full-stack nanodegree that uses Python code
to access and report on the content of a PostgreSQL database of articles and web traffic to those articles. The emphasis of the exercise is
incorporating as much of the data crunching as possible in SQL queries and doing very little in Python code.

## Requirements
Python 3; os and psycopg libraries
PostgreSQL

## Installation
Create three helper views using the following statements:

### 1. Article Views

`create view article_views as select substring (path from 10) as path, count(*) as num from log where path like '%article%' group by path order by num desc;`

### 2. Queries by Date

`create view queries_by_date as select log.time::date as date, count(status) as queries from log group by 1;`

### 3. Errors by Date

`create view errors_by_date as select log.time::date as date, count(status) as errors from log where status != '200 OK' group by 1;`

## License
No licensed content