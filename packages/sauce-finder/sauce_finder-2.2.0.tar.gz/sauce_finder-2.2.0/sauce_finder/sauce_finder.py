#!/usr/bin/env python
import re

import requests


def get_match(url):
    data = {'file': '(binary)', 'url': url}
    response = requests.post('https://danbooru.iqdb.org/', data).text

    return _match_api(response)


def _match_api(response):
    if re.search(r'No relevant matches', response):
        ret = {
            "type": "possible",
            "found": []
        }
        similarity = re.findall(r'([0-9]{1,3})% similarity', response)
        url = re.findall(r'(?:https?://)?danbooru.donmai.us/posts/[0-9]+',
                         response)
        url = [f"https://{x}" if not x.startswith("http") else x for x in url]
        size = re.findall(r'([0-9]+)×([0-9]+)', response)
        rating = re.findall(r'\[.*\]', response)
        n = 0
        for i in url:
            ret["found"].append({
                "link": i,
                "similarity": similarity[n],
                "rating": rating[n + 1],
                "size": {
                    "width": size[n + 1][0],
                    "height": size[n + 1][1]
                }
            })

            n += 1
        return ret
    else:
        ret = {
            "type": "definite"
        }

        similarity = re.search(r'([0-9]{1,3})% similarity', response)
        if similarity:
            similarity = similarity.group(1)
        url = re.search(r'(?:https?://)?danbooru.donmai.us/posts/[0-9]+',
                        response).group()
        if not url.startswith("http"):
            url = f'https://{url}'
        size = re.findall(r'([0-9]+)×([0-9]+)', response)
        rating = re.findall(r'\[.*\]', response)[1]

        ret["found"] = {
            "link": url,
            "similarity": similarity,
            "rating": rating,
            "size": {
                "width": size[1][0],
                "height": size[1][1]
            }
        }

        return ret


def check_url(value: str) -> bool:
    """
    Check that the url is direct link to a image

    :param value: URL to check
    :type value: str
    :return: True only if 'image' is anywhere in the content-type
             of the URL headers.
    :rtype: bool
    """
    return "image" in requests.head(value).headers["content-type"]
