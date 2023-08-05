async-request
=============

A lightweight network request framework based on requests & asyncio

install
-------

```bash
pip install async_request
```

usage
-----
Just like scrapy:
```python
from async_request import AsyncSpider, Request


class MySpider(AsyncSpider):
    
    start_urls = ['https://cn.bing.com/']
    
    async def parse(self, response):
        print(response.xpath('//a/@href').get())
        yield Request('https://github.com/financialfly/async-request', callback=self.parse_github)

    def parse_github(self, response):
        yield {'hello': 'github'}
    
    async def process_result(self, result):
        # Process result at here.
        print(result)


if __name__ == '__main__':
    # Run spider
    MySpider().run()
```
For more detailed control (like: handle cookies, download delay, concurrent requests, max retries, logs settings etc.): (refer to the constructor of the `Crawler` class):
```python
from async_request import AsyncSpider

class MySpider(AsyncSpider):
    ...

if __name__ == '__main__':
    MySpider(
        handle_cookies=True, 
        download_delay=0,
        concurrent_requests=10,
        max_retries=3,
        log_file='spider.log'
    ).run()
```

test
----
Use `fetch` function to get a response immediately:
```python
from async_request import fetch


def parse():
    response = fetch('https://www.bing.com')
    print(response)
    
   
if __name__ == '__main__':
    parse()
```
the output will like this:
```
<Response 200 https://cn.bing.com/>
```

Use the `test` decorator is also a method to test spider:
```python
import async_request as ar


@ar.test('https://www.baidu.com')
def parse(response):
    print(response.url, response.status_code)
    
    
if __name__ == '__main__':
    parse()
```
then run the script, you will see the result:
```
https://www.baidu.com/ 200
```
