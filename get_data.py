import re
import json
from time import sleep

from bs4 import BeautifulSoup
from datetime import datetime, date, time
from tqdm import tqdm
import requests
from parser_config import *
from parser import Parser
requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ":HIGH:!DH:!aNULL"
try:
    requests.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += (
        ":HIGH:!DH:!aNULL"
    )
except AttributeError:
    pass









def set_payload_map_dynamic(payload, period, subject):
    # set period
    payload["p_json"]["pageItems"]["itemsToSubmit"][0]["v"] = period
    # set subject
    payload["p_json"]["pageItems"]["itemsToSubmit"][1]["v"] = subject

    payload["p_json"] = json.dumps(payload["p_json"])

    return payload


def generate_template_date(year: int, month: str, day: int):
    """
    Generates date in Russian Language
    """
    d = date(year, month, day)
    date_string = d.strftime("%w, %d %B, %Y")

    # change day of week from number to ru_name
    day_number = re.search("(.*?),", date_string).group(1)
    date_string = date_string.replace(
        day_number, week_days[day_number], 1
    )

    # change month name from eng to ru
    for key in months_translate.keys():
        date_string = date_string.replace(key, months_translate[key])

    return date_string


def set_headers_request_description(cookie, referer):

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-GB,en-US;q=0.9,en-BY;q=0.8,en;q=0.7,ru;q=0.6",
        "Connection": "keep-alive",
        #     "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": cookie,
        #     "Host": "115.xn--90ais",
        #     "Origin": "https://115.xn--90ais",
        "Referer": referer,
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua": '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Linux",
    }

    return headers


def get_request_description(html_doc):

    soup = BeautifulSoup(html_doc, "html.parser")

    request_status = (
        soup.select_one("div.current_problem_status > span").contents[0].strip()
    )
    request_status_date = (
        soup.select_one("div.current_problem_status_date").contents[0].strip()
    )
    user_comment = (
        soup.select_one("div.t-Region-body > div:nth-child(2)")
        .contents[1]
        .replace("\r", "")
        .replace("\n", " ")
        .strip()
    )
    organization_comment = (
        soup.select_one("div.t-Region-body > div:nth-child(3)").contents[1].strip()
    )
    request_regdate = soup.select_one("div.current_problem_regdate").contents[1].strip()
    request_moddate = soup.select_one("div.current_problem_moddate").contents[1].strip()
    try:
        rating = soup.find("input", {"id": "P35_RATING"}).get("value")
    except AttributeError:
        rating = None
    adress = (
        soup.select_one("span.current_problem_address ")
        .contents[0]
        .replace("\n", " ")
        .strip()
    )

    request_description = {
        "status": request_status,
        "status_date": request_status_date,
        "user_comment": user_comment,
        "organization_comment": organization_comment,
        "request_regdate": request_regdate,
        "request_moddate": request_moddate,
        "rating": rating,
        "adress": adress,
    }

    return request_description


def get_params_list_from_infotext(info_string):

    link_host = "https://115.xn--90ais/portal/"
    try:
        number = re.search("Заявка № (.*?)<br>", info_string).group(1)
    except AttributeError:
        number = None
    try:
        district = re.search("Адрес: </b>(.*?),", info_string).group(1)
    except AttributeError:
        district = None
    try:
        malfunction_type = re.search("Вид неисправности: </b>(.*?)<br>", info_string).group(
        1
    )
    except AttributeError:
        malfunction_type = None
    try:
        performer = re.search("<b> Исполнитель: </b>(.*?)<br>", info_string).group(1)
    except AttributeError:
        performer = ""
    link = link_host + re.search('<a href="(.*?)">', info_string).group(1)

    lst = {
        "number": number,
        "district": district,
        "malfunction_type": malfunction_type,
        "performer": performer,
        "application_card_link": link,
    }

    return lst


def get_main_info_from_requests_list(list_of_raw_requests):
    main_list = []

    for request in range(len(list_of_raw_requests["row"])):

        info_string = list_of_raw_requests["row"][request]["INFOTEXT"]

        dct = get_params_list_from_infotext(info_string)

        main_list.append(dct)

    return main_list


def get_raw_requests(url, headers, payload):
    with requests.Session() as s:
        s.headers.update(headers)

        r = s.post(url=url, data=payload)
        try:
            list_of_raw_requests = r.json()
        except ValueError:
            print("ERROR")
            print(r.text)

    return list_of_raw_requests


def get_extra_info_content(url, cookie, referer):

    headers = set_headers_request_description(cookie=cookie, referer=referer)
    with requests.Session() as s:
        s.headers.update(headers)

        r = s.get(url=url, headers=headers)

        request_description = get_request_description(r.text)

    return request_description


def main():

    headers = Parser.get_headers_map(cookie=cookie, referer=referer)
    payload = Parser.get_payload_map_static(
        # you can remove params but also you can send yours,
        # this function has default params

        # p_instance=p_instance,
        # p_request=p_request,
        # x02=x02,
        # x03=x03,
        # x04=x04,
        # x05=x05,



        # protected=protected, # use me pls
        # salt=salt, # use me pls
    )

    for period in tqdm(list_of_dates_2020):

        period_temp_list = []

        for subject in tqdm(subjects):

            category_req_dict = {"category": subjects[subject]}
            payload = set_payload_map_dynamic(payload, period, subject)
            # get json with all requests from this period and subject
            list_of_raw_requests = get_raw_requests(url, headers, payload)
            # get main like a json list with params
            list_with_main_info = get_main_info_from_requests_list(list_of_raw_requests)
            # set new headers for getting extra info

            for request in range(len(list_with_main_info)):
                url = list_with_main_info[request]["application_card_link"]

                request_description = get_extra_info_content(
                    url=url, cookie=cookie, referer=referer
                )

                list_with_main_info[request] = {
                    **list_with_main_info[request],
                    **request_description,
                    **category_req_dict,
                }

                del list_with_main_info[request]["application_card_link"]

                sleep(1)

            # final version of request list
            list_of_requests = list_with_main_info
            # save final results
            # set old var
            payload = Parser.get_payload_map_static(
                # p_instance=p_instance,
                # p_request=p_request,
                # x02=x02,
                # x03=x03,
                # x04=x04,
                # x05=x05,
                # protected=protected, # use me pls
                # salt=salt, # use me pls
            )
            url = "https://115.xn--90ais/portal/wwv_flow.ajax" # use me pls
            headers = Parser.get_headers_map(cookie=cookie, referer=referer) # use me pls
            period_temp_list.extend(list_of_requests)

        with open(path / f"{period}.json", "w", encoding="utf8") as f:
            json.dump(period_temp_list, f, ensure_ascii=False)


if __name__ == "__main__":
    main()
