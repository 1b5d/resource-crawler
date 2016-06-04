# Crawler

This solution is a simple crawler that crawls a website to get links and the page resources presented inside those links, it outputs a sitemap that contains all the resulted links in HTML format.

The crawler is written in python, and it uses multithreading to enhance the performace and make a better use of the machine resources.

# Algorithm
The algorithm used in the crawler is very simple at the core, it consists of a worker pool and a shared queue, and works by the following steps:

* Add the initial URLs to the processing queue.
* Initialize the pool of workers and run it.
* Foreach worker, repeat the following steps:
* Get a link item off the queue.
* Fetche the contents of the URL stored in the link.
* Parse the content fetched by the URL, and extract the links of the contents.
* Add the navigable links extected from the last step to the processing queue.
* If the queue stayed empty for 10 seconds, terminate the worker.
* Terminate the crawler when all the workers terminate.

urllib3 thread-safe lib is used to fetch the links from the original website, and the workers run in parallel to make use of the time gap spend while download the content of the page.

# How to use

You can use the crawler class by initializing it, for example in a `main.py` file:

```python
crawler = Crawler(seed_urls=['http://gocardless.com'], domains=['gocardless.com'], num_threads=20, verbose=True)
```

Then you can start the crawler by simply running `start()` method:
```python
crawler.start()
```

and you can generate the sitemap HTML file by passing `crawler.links` to a `sitemap.Generator` object:

```python
generator = Generator(crawler.links)
with codecs.open('output.html', 'w', encoding='utf-8') as f:
    f.write(generator.get_html())
f.close()
```

after that, just run the file by running:

```sh
$ python main.py
```

and wait for crawling to be finished, then an HTML file `output.html` will be generated in the project directory, containing all the crawled links with the resources inside each page.