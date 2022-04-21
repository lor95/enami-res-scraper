import asyncio
from pyppeteer import launch
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlopen, Request
from fontTools.ttLib import woff2, TTFont
import logging
import sys
import os
import re

logging.basicConfig(level=logging.INFO, format="%(asctime)s: %(message)s")

FONT_SPECIFIER_NAME_ID = 4


def get_font_name(font: TTFont) -> str:
    name = ""
    for record in font["name"].names:
        if b"\x00" in record.string:
            name_str = record.string.decode("utf-16-be")
        else:
            name_str = record.string.decode("utf-8")
        if record.nameID == FONT_SPECIFIER_NAME_ID and not name:
            name = name_str
        if name:
            break
    return name


def download_file(path: str, urls: list, key: str = "img"):
    for url in urls:
        f_ = None
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        filename = os.path.basename(urlparse(url).path)
        full_path = os.path.join(path, filename)
        dirname = os.path.dirname(full_path)
        try:
            f = urlopen(req).read()
            with open(full_path, "wb") as file:
                file.write(f)
            if key == "font":
                font = TTFont(full_path)
                _, ext = os.path.splitext(full_path)
                f_ = get_font_name(font)
                if re.match(r".*woff.*", full_path, re.IGNORECASE):
                    with open(full_path, mode="rb") as infile:
                        with open(os.path.join(dirname, f"{f_}.ttf"), mode="wb") as outfile:
                            woff2.decompress(infile, outfile)
                else:
                    os.rename(full_path, os.path.join(dirname, f"{f_}{ext}"))
                os.remove(full_path)
                full_path = os.path.join(dirname, f"{f_}{ext}")
            logging.info(f"Downloaded {full_path}")
        except Exception:
            logging.warning(f"Cannot download {url}")
            with open(os.path.join(dirname, "errors.txt"), "a") as file:
                file.write(f"{url}\n")



def run_script(main_url, download_path):
    p_url = urlparse(main_url)
    list_of_font_format = ["woff", "woff2", "otf", "ttf"]
    list_of_img_format = ["png", "jpg", "jpeg", "svg"]
    RES_PATH = os.path.join(
        download_path,
        "resources",
        p_url.netloc.replace("/", "_") + p_url.path.replace("/", "_"),
    )
    Path(RES_PATH).mkdir(parents=True, exist_ok=True)
    Path(RES_PATH, "fonts").mkdir(exist_ok=True)
    Path(RES_PATH, "images").mkdir(exist_ok=True)

    font_urls = set()
    img_urls = set()

    async def get_urls(interceptedRequest):
        url = interceptedRequest.url
        if re.match(f".*({'|'.join(list_of_font_format)}).*", url, re.IGNORECASE):
            font_urls.add(url)
        if re.match(f".*({'|'.join(list_of_img_format)}).*", url, re.IGNORECASE):
            img_urls.add(url)
        await interceptedRequest.continue_()

    async def main():
        browser = await launch()
        page = await browser.newPage()
        await page.setRequestInterception(True)
        page.on("request", lambda response: asyncio.ensure_future(get_urls(response)))
        await page.goto(main_url.strip())
        await browser.close()

    logging.info("Checking for data to download...")
    asyncio.get_event_loop().run_until_complete(main())
    logging.info("Download start!")
    download_file(os.path.join(RES_PATH, "fonts"), list(font_urls), key="font")
    download_file(os.path.join(RES_PATH, "images"), list(img_urls), key="img")
    logging.info("Exiting.")


run_script(sys.argv[1], sys.argv[2])
