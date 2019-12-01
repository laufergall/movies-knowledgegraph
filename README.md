# movies-knowledgegraph

(ongoing work)

I am constructing a knowledge graph of movies shown in Berlin cinemas.

## Data 

We retrieve currently showing movies from [Berlin.de](https://www.berlin.de/kino/_bin/azfilm.php) using [scrapy](https://docs.scrapy.org/en/latest/).

## Retrieve cinema movies

```bash
cd kinoprogramm
```

You need Python 3.7.4 and [requirements.txt](kinoprogramm/requirements.txt).

You can start the spider to retrieve currently showing cinema movies by just:

```bash
scrapy crawl kinoprogramm -o ../data/kinoprogramm.json
```

Data will be written to the file specified with the `-o` parameter.

## Deployment

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
