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
