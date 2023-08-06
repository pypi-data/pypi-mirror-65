#!/usr/bin/env python
import requests
import re
from sys import argv
from getopt import getopt
from getopt import GetoptError
import os
from urllib.parse import urlparse
import webbrowser


img_url = ''
download = False
browser = False
verbose = False


def main():
    get_args(argv[1:])
    if not check_url():
        print('URL is not direct link to a image.')
        exit(0)
    get_match()


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
    # Get options
    for opt, arg in opts:
        if opt == '-d':
            global download
            download = True
        elif opt == '-o':
            global browser
            browser = True
        elif opt == '-v':
            global verbose
            verbose = True
        elif opt == '-h':
            help_text()
    # Get url
    global img_url
    img_url = args[0]


def check_url():
    # Check that the url is direct link to a image
    response = requests.head(img_url)
    if re.search(r'image', response.headers["content-type"]):
        return True
    return False


def get_match():
    data = {'file': '(binary)', 'url': img_url}
    response = requests.post('http://danbooru.iqdb.org/', data).text

    print('')

    if re.search(r'No relevant matches', response):
        print('No relevant matches, but here\'s possible matches:')
        similarity = re.findall(r'([0-9]{1,3})% similarity', response)
        url = re.findall(r'danbooru.donmai.us\/posts\/[0-9]+', response)
        if verbose:
            size = re.findall(r'([0-9]+)×([0-9]+)', response)
            rating = re.findall(r'\[.*\]', response)
        n = 0
        for i in url:
            print('_'*50)
            i = 'http://{}'.format(i)
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
        url = re.search(r'danbooru.donmai.us\/posts\/[0-9]+', response).group()
        url = 'http://{}'.format(url)
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


def download_img(url):
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
