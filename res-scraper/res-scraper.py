import asyncio
from pyppeteer import launch
import sys


def run_script(main_url):
    urls = set()
    async def get_urls(interceptedRequest):
        urls.add(interceptedRequest.url)
        await interceptedRequest.continue_()

    async def main():
        browser = await launch()
        page = await browser.newPage()
        await page.setRequestInterception(True)
        page.on('request', lambda response: asyncio.ensure_future(get_urls(response)))
        await page.goto(main_url.strip())
        await browser.close()
    asyncio.get_event_loop().run_until_complete(main())
    print(urls)

run_script(sys.argv[1])