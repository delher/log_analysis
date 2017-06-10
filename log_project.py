#!/usr/bin/env python3
# Logs Analysis Project
import psycopg2
import os
DBNAME = "news"


def get_top3():
    """Return top 3 articles from news db in descending order"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute('''SELECT articles.title, authors.name, article_views.num
                from article_views
                join articles on article_views.path = articles.slug
                join authors on articles.author = authors.id
                order by article_views.num desc limit 3;''')
    top3 = c.fetchall()
    db.close()
    return top3


def author_ranking():
    """Return list of authors ranked by number of article views """
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute('''SELECT authors.name, SUM(article_views.num)
                FROM article_views
                JOIN articles ON article_views.path = articles.slug
                JOIN authors ON articles.author = authors.id
                GROUP BY authors.name
                ORDER BY SUM(article_views.num) DESC;''')
    author_list = c.fetchall()
    db.close()
    return author_list


def find_high_error_dates():
    """Return list of dates with logged error rates > 1 percent"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute('''SELECT errors_by_date.date AS date,
                errors_by_date.errors AS errors,
                queries_by_date.queries AS queries
                FROM errors_by_date
                JOIN queries_by_date
                ON errors_by_date.date = queries_by_date.date
                WHERE errors::float / queries::float > .01;''')
    high_error_dates = c.fetchall()
    db.close()
    return high_error_dates


def clear_screen():  # from StackExchange 15195832
    os.system(['clear', 'cls'][os.name == 'nt'])

clear_screen()
print("*** Top 3 Most Popular Articles ***")
result = (get_top3())
for idx, item in enumerate(result):
    print("{}. {} by {} ({} views)".format(idx+1, *item))
print
print("*** Authors Ranked By Article Views ***")
result = author_ranking()
for idx, item in enumerate(result):

    print("{}. {:<24} {:>7} views".format(idx+1, *item))
print
print("*** Find Dates With Error Rate > 1% ***")
result = find_high_error_dates()
for item in result:
    print("On {}, there were {} errors in {} queries.".format(*item))
print
print("*** End of Report ***")
print
