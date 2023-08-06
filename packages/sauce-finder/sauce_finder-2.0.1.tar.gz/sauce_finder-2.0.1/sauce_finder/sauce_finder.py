#!/usr/bin/env python
import requests
import re
from sys import argv
from getopt import getopt
from getopt import GetoptError
import os
from urllib.parse import urlparse
import webbrowser


def main():
    args = get_args(argv[1:])
    get_match(args)


def get_args(args):
    # If no args given, show usage
    if len(args) < 1:
        usage_text()
        exit(0)
    # check if --help is written
    if args[0] == '--help':
        help_text()
    # Parse arguments
    try:
        opts, args = getopt(args, 'dhov')
    except GetoptError as e:
        print(e)
        help_text()
        exit(0)

    ret = {
        "download": False,
        "browser": False,
        "verbose": False,
        "img_url": ""
    }

    # Get options
    for opt, arg in opts:
        if opt == '-d':
            ret["download"] = True
        elif opt == '-o':
            ret["browser"] = True
        elif opt == '-v':
            ret["verbose"] = True
        elif opt == '-h':
            help_text()
    # Get url
    ret["img_url"] = args[0]
    return ret


def check_url(args):
    # Check that the url is direct link to a image
    response = requests.head(args["img_url"])
    if re.search(r'image', response.headers["content-type"]):
        return True
    return False


def get_match(args, api_mode=False):

    download = args["download"] or False
    browser = args["browser"] or False
    verbose = args["verbose"] or False
    img_url = args["img_url"] or None

    def _print(a):
        if not api_mode:
            print(a)

    if not check_url(args):
        if api_mode:
            raise Exception("URL is not a direct link to an image")
        else:
            print('URL is not direct link to a image.')
            exit(0)

    data = {'file': '(binary)', 'url': img_url}
    response = requests.post('https://danbooru.iqdb.org/', data).text

    if api_mode:
        return _match_api(response)
    return _match_script(response, verbose, download, browser)


def _match_script(response, verbose=False, download=False, browser=False):
    print('')

    if re.search(r'No relevant matches', response):
        print('No relevant matches, but here\'s possible matches:')
        similarity = re.findall(r'([0-9]{1,3})% similarity', response)
        url = re.findall(r'(?:https?://)?danbooru.donmai.us\/posts\/[0-9]+', response)
        url = [f"https://{x}" if not x.startswith("http") else x for x in url]
        if verbose:
            size = re.findall(r'([0-9]+)×([0-9]+)', response)
            rating = re.findall(r'\[.*\]', response)
        n = 0
        for i in url:
            print('_'*50)
            if verbose:
                print('Possible match found, with {sim}% similarity\n'
                      '{rating}, {width}x{height}\n'
                      '{url}'.format(sim=similarity[n], url=i,
                                     rating=rating[n + 1],
                                     width=size[n + 1][0],
                                     height=size[n + 1][1]))
            else:
                print('Possible match found, with {sim}% similarity\n'
                      '{url}'.format(sim=similarity[n], url=i))
            print('_'*50)
            print('\n')
            n += 1
        if download:
            print('Downloading first possible match')
            download_img(url[0])
        if browser:
            print('Opening first possible match')
            webbrowser.open(url[0])
    else:
        similarity = re.search(r'([0-9]{1,3})% similarity', response).group(1)
        url = re.search(r'(?:https?://)?danbooru.donmai.us\/posts\/[0-9]+', response).group()
        if not url.startswith("http"):
            url = f'https://{url}'
        if verbose:
            size = re.findall(r'([0-9]+)×([0-9]+)', response)
            rating = re.findall(r'\[.*\]', response)[1]
            print('Match found, with {sim}% similarity\n{rating}, {width}x'
                  '{height}\n{url}'.format(sim=similarity, rating=rating,
                                           width=size[1][0], height=size[1][1],
                                           url=url))
        else:
            print('Match found, with {sim}%'
                  ' similarity\n{url}'.format(sim=similarity, url=url))
        if download:
            print('Downloading image')
            download_img(url)
        if browser:
            webbrowser.open(url)


def _match_api(response):
    if re.search(r'No relevant matches', response):
        ret = {
            "type": "possible",
            "found": []
        }
        similarity = re.findall(r'([0-9]{1,3})% similarity', response)
        url = re.findall(r'(?:https?://)?danbooru.donmai.us\/posts\/[0-9]+', response)
        url = [f"https://{x}" if not x.startswith("http") else x for x in url]
        size = re.findall(r'([0-9]+)×([0-9]+)', response)
        rating = re.findall(r'\[.*\]', response)
        n = 0
        for i in url:
            ret["found"].append({
                "link": i,
                "similarity": similarity[n],
                "rating": rating[n+1],
                "size": {
                    "width": size[n+1][0],
                    "height": size[n+1][1]
                }
            })

            n += 1
        return ret
    else:
        ret = {
            "type": "definite"
        }

        similarity = re.search(r'([0-9]{1,3})% similarity', response).group(1)
        url = re.search(r'(?:https?://)?danbooru.donmai.us\/posts\/[0-9]+', response).group()
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


def download_img(url):
    if not url.startswith("http"):
        url = f"https://{url}"
    response = requests.get(url).text
    image_element = re.search(r'id=\"image\"', response).start()
    parsed_html = response[image_element:]
    img_url = re.search(r'src=\"(.*)\"', parsed_html).group(1)
    img_name = os.path.basename(urlparse(img_url).path)
    response = requests.get(img_url)
    with open(img_name, 'wb') as f:
        f.write(response.content)
    print('Image saved as {}'.format(img_name))


def help_text():
    # Print help text and exit
    usage_text()
    print('\n'
          'sauce_finder is script to find and download anime images.\n\n'
          '-d\t\tDownload mathced image.\n'
          '-o\t\tOpen mathced image in browser.\n'
          '-v\t\tBe more verbose.\n'
          '-h, --help\tPrint this help text and exit.\n\n'
          'Programmed by @Miicat_47')
    exit(0)


def usage_text():
    # Print usage (also part of help_text)
    print('Usage: sauce_finder [OPTIONS] [IMG_URL]')


if __name__ == '__main__':
    main()
