# This repo

(ongoing work)

I am constructing a knowledge graph of movies shown in Berlin cinemas.

# Data 

We retrieve currently showing movies from [Berlin.de](https://www.berlin.de/kino/_bin/azfilm.php) using [scrapy](https://docs.scrapy.org/en/latest/).

# Retrieve cinema movies

## write to json file

```bash
cd kinoprogramm
```

You need Python 3.7.4 and [requirements.txt](kinoprogramm/requirements.txt).

You can start the spider to retrieve currently showing cinema movies by just:

```bash
scrapy crawl kinoprogramm -o ../data/kinoprogramm.json
```

Data will be written to the file specified with the `-o` parameter.

## write to MongoDB database

Start two containers, one with [MongoDB](https://www.mongodb.com/) and another one with [Nosqlclient](https://github.com/nosqlclient/nosqlclient) (formerly mongoclient) by:

```bash
docker-compose build
docker-compose up
```

Retrieve showing cinema movies (the specified pipeline will insert the data into MongoDB): 

```bash
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


# Deployment

To deploy to the [Scrapy Cloud](https://scrapinghub.com/scrapy-cloud):

1. Sign up to [Scrapy Cloud](https://app.scrapinghub.com/). There is a free plan.
2. Create a new project
3. cd to `movies-knowledgegraph/kinoprogramm`
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

# Tests

After installing `requirements_tests.txt`, tests can be run by:

```shell
python -m pytest tests/
```
