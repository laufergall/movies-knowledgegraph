# This repo

:construction: *ongoing work* :construction: I am constructing a knowledge graph of movies shown in Berlin cinemas.


# Scraping cinema movies

We retrieve currently showing movies from [Berlin.de](https://www.berlin.de/kino/_bin/azfilm.php) using [scrapy](https://docs.scrapy.org/en/latest/).

Start four containers:

* a container where the scrapy job runs, and stops when finished.
* a [MongoDB](https://www.mongodb.com/) database
* the [Nosqlclient](https://github.com/nosqlclient/nosqlclient) (formerly mongoclient)
* our Flask-RESTPlus backend

```bash
docker-compose build
docker-compose up
```

There are two alternatives for storing data: 1) write to MongoDB database, or 2) write to json file.

## write to MongoDB database

Retrieve playing cinema movies (the specified pipeline will insert the data into MongoDB): 

```bash
cd scrapy/kinoprogramm
scrapy crawl kinoprogramm
```

Open the mongo client on `http://localhost:3300/` and connect to MongoDB by:
1. Click on "Connect" (up-right corner).
2. Click on "Edit" the default connection.
3. Clear connection url. Under the "Connection" tab, Database Name: `kinoprogramm`.
4. On tab "Authentication", `Scram-Sha-1` as Authentication Type, Username: `root`, Password: `12345`, Authentication DB: leave empty.
5. Click on "Save", and click on "Connect".

See stored data under "Collections" -> "kinos".

Go to "Tools" -> "Shell" to write [mongodb queries](https://docs.mongodb.com/manual/tutorial/query-documents/) such as: 

```shell
db.kinos.distinct( "shows.title" )
```

## write to json file

You need Python 3.7.4 and [requirements.txt](scrapy/requirements.txt).

You can start the spider by just:

```bash
cd scrapy/kinoprogramm
scrapy crawl kinoprogramm -o ../data/kinoprogramm.json
```

Data will be written to the file specified with the `-o` parameter. Data will also be written to the MongoDB database, unless the file `pipelines.py` is adapted.

## scrapy deployment

To deploy to the [Scrapy Cloud](https://scrapinghub.com/scrapy-cloud):

1. Sign up to [Scrapy Cloud](https://app.scrapinghub.com/). There is a free plan.
2. Create a new project
3. cd to `movies-knowledgegraph/scrapy`
4. Deploy by `pip install shub`, `shub login`, `shub deploy <PROJECT_ID>`

Link to [Scrapinghub Support Center](https://support.scrapinghub.com/support/home).

Link to [Scrapinghub API Reference](https://doc.scrapinghub.com/scrapy-cloud.html?_ga=2.243489287.325994476.1574619401-1607314863.1570297387).

Once deployed, the spyder can run by:

1. Retrieve the [API key](https://app.scrapinghub.com/account/apikey)

2. Run spyder by:

```bash
curl -u <API_KEY>: https://app.scrapinghub.com/api/run.json -d project=<PROJECT_ID> -d spider=kinoprogramm
```

3. Scraped data can be retrieved by:

```bash
curl -u <API_KEY>: https://storage.scrapinghub.com/items/:<PROJECT_ID>[/<SPIDER_ID>][/<JOB_ID>][/<ITEM_NUMBER>][/<FIELD_NAME>]
```

Example retrieving contact from first cinema (item 0) of spyder 1 job 6 and project id 417389:
```bash
curl -u <API_KEY>: https://storage.scrapinghub.com/items/417389/1/6/0/contact
```

# Backend

You can access the Swagger UI of Flask-RESTPlus backend under  `http://localhost:8001/`. 

Here, you can use the different endpoints to retrieve data from the MongoDB database.


# Tests

After installing `requirements_tests.txt`, tests for scrapy can be run by:

```bash
cd scrapy/kinoprogramm
python -m pytest tests/
```
