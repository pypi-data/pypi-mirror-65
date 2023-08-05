# -*- coding: utf8 -*-

import argparse
import asyncio
import logging
from datetime import datetime

from crawl_wx.crawl import WXCrawl


def cmd():
    parser = argparse.ArgumentParser(description="crawl wx")
    parser.add_argument("--curl_file", required=True, dest="curl_request")
    parser.add_argument("--output", required=True, dest="output_dir")
    parser.add_argument("--end_at", type=lambda s: datetime.strptime(s, '%Y-%m-%d %H:%M:%S'), help="end at")
    parser.add_argument("--log_level", default="INFO", dest="log_level")
    parser.add_argument("--store_url", action="store_true", help="only store content urls")
    args = parser.parse_args()
    log_level = getattr(logging, args.log_level, "INFO")
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    with open(args.curl_request) as f:
        curl_request = f.read()
    spider = WXCrawl(curl_request=curl_request, output=args.output_dir, tick=1,
                     end_at=args.end_at, store_url=args.store_url)
    asyncio.get_event_loop().run_until_complete(spider.run())


if __name__ == "__main__":
    cmd()
