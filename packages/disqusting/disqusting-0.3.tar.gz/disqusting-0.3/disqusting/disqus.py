from datetime import datetime
from typing import Iterable

import requests


def iso(date: str) -> datetime:
    return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")


class Disqus:
    def __init__(self, api_key: str, forum: str):
        """Instantiate a discus api connection

        :param api_key The API key from your disqus account / application page
        :param forum The short name of the forum you want to scrape
        """
        self.api_key = api_key
        self.forum = forum

    def get(self, endpoint, **options) -> dict:
        """Get a single result or page

        :param endpoint the endpoint without .json, e.g. forums/listThreads
        :param options A dict with all other options/arguments for the call
        """
        opts = dict(api_key=self.api_key, forum=self.forum)
        opts.update(options)
        url = f"https://disqus.com/api/3.0/{endpoint}.json"
        r = requests.get(url, opts)
        r.raise_for_status()
        return r.json()

    def get_all(self, endpoint, **options) -> Iterable[dict]:
        """Iterate over all pages of results (result must contain a cursor)

        :param endpoint the endpoint without .json, e.g. forums/listThreads
        :param options A dict with all other options/arguments for the call
        """
        while True:
            r = self.get(endpoint, **options)
            yield from r["response"]
            if not r["cursor"]["hasNext"]:
                break
            options["cursor"] = r["cursor"]["id"]
            print(r["cursor"], len(r["response"]), r["response"][0]["createdAt"], "-", r["response"][-1]["createdAt"])

    def list_threads(self, from_date: datetime) -> Iterable[dict]:
        """List all threads in the current forum"""
        # the since arguments works as "until", so get everything until we hit the date specified
        for t in disq.get_all("forums/listThreads"):
            timestamp = iso(t["createdAt"], )
            if timestamp < from_date:
                break
            yield t

    def thread_details(self, post_url: str) -> dict:
        """Get details of a single thread"""
        thread = f"link:{post_url}"
        return self.get("threads/details", thread=thread)["response"]

    def thread_posts(self, post_url: str) -> Iterable[dict]:
        """List all posts in a thread"""
        thread = f"link:{post_url}"
        return self.get_all("threads/listPosts", thread=thread)

