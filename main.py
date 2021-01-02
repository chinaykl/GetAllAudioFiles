import re
import sys
from typing import List

import requests


def identify_domain_name(url: str) -> str:
    pattern = "^http[s]*://\S+?/"
    all_result = re.findall(pattern, url)
    result = None
    if len(all_result) != 0:
        result = all_result[0]
        print("Identified Domain Name:" + result)
    return result


def analyse_useful_lines_from_url(url: str, encoding: str, pattern: str) -> List[str]:
    response = requests.get(url)
    response.encoding = encoding
    text = response.text
    useful_lines = re.findall(pattern, text)
    print(str(len(useful_lines)) + " Useful Lines Found")
    return useful_lines


def analyse_useful_info_from_str(origin: str, pattern: str) -> str:
    print("Original String:" + origin)
    useful_info_list = re.findall(pattern, origin)
    result = None
    if len(useful_info_list) != 0:
        result = useful_info_list[0]
        print("Useful String:" + result)
    return result


def analyse_useful_info_from_url(url: str, encoding: str, pattern: str) -> str:
    response = requests.get(url)
    response.encoding = encoding
    text = response.text
    useful_info_list = re.findall(pattern, text)
    result = None
    if len(useful_info_list) != 0:
        result = useful_info_list[0]
        print("Useful String:" + result)
    return result


def main(url: str) -> str:
    result = -1
    home_url = identify_domain_name(url)
    if home_url is None:
        print("Input URL ERROR")
        return result

    href_lines = analyse_useful_lines_from_url(url, "gbk", '''<a href='/down/\S+' target="_blank">\S+</a>''')
    if len(href_lines) == 0:
        print("No Useful Page Found")
        return result

    down_page_urls = []
    for line in href_lines:
        path = analyse_useful_info_from_str(line, "(?<=<a href='/)[^'].*[^'](?=' )")
        print(home_url + path)
        down_page_urls.append(home_url + path)

    down_urls = []
    for line in down_page_urls:
        down_url = analyse_useful_info_from_url(line, "gbk", "http:/\S+.mp3")
        print(down_url)
        down_urls.append(down_url)

    if len(down_urls) != 0:
        result = 0
    return result


if __name__ == '__main__':
    print("Start")
    if len(sys.argv) != 2:
        print("Input Arg Num Error")
        exit(-1)
    error_number = main(sys.argv[1])
    print("End")
    exit(error_number)
