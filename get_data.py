import re
import json
from time import sleep
from pathlib import Path
from bs4 import BeautifulSoup
from datetime import datetime, date, time
from tqdm import tqdm
import requests

requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ":HIGH:!DH:!aNULL"
try:
    requests.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += (
        ":HIGH:!DH:!aNULL"
    )
except AttributeError:
    pass


def set_headers_map(cookie, referer):

    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-GB,en-US;q=0.9,en-BY;q=0.8,en;q=0.7,ru;q=0.6",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": cookie,
        "Host": "115.xn--90ais",
        "Origin": "https://115.xn--90ais",
        "Referer": referer,
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua": '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Linux",
    }

    return headers


def set_payload_map_static(p_instance, p_request, x02, x03, x04, x05, protected, salt):

    json_params = {
        "pageItems": {
            "itemsToSubmit": [
                {"n": "P19_PERIOD", "v": ""},
                {"n": "P19_SUBJECT", "v": ""},
            ],
            "protected": protected,
            "rowVersion": "",
        },
        # salt changeable / required (90%)
        "salt": salt,
    }

    data = {
        "p_flow_id": "10901",
        "p_flow_step_id": "19",
        # p_instance - changeable / undefined
        "p_instance": p_instance,
        "p_debug": "",
        # p_request - changeable / required (90%)
        "p_request": p_request,
        "x01": "3857",
        "x02": x02,
        "x03": x03,
        "x04": x04,
        "x05": x05,
        "x06": "N",
        "x07": "11",
        "x10": "FOIDATA",
        "p_json": json_params,
    }

    return data


def set_payload_map_dynamic(payload, period, subject):
    # set period
    payload["p_json"]["pageItems"]["itemsToSubmit"][0]["v"] = period
    # set subject
    payload["p_json"]["pageItems"]["itemsToSubmit"][1]["v"] = subject

    payload["p_json"] = json.dumps(payload["p_json"])

    return payload


def generate_template_date(year, month, day):

    day_of_week = {
        "1": "Понедельник",
        "2": "Вторник",
        "3": "Среда",
        "4": "Четверг",
        "5": "Пятница",
        "6": "Суббота",
        "0": "Воскресенье",
    }

    months = {
        "January": "Январь",
        "February": "Февраль",
        "March": "Март",
        "April": "Апрель",
        "May": "Май",
        "June": "Июль",
        "July": "Июль",
        "August": "Август",
        "September": "Сентябрь",
        "October": "Октябрь",
        "November": "Ноябрь",
        "December": "Декарь",
    }

    d = date(year, month, day)
    date_string = d.strftime("%w, %d %B, %Y")

    # change day of week from number to ru_name
    day_of_week_number = re.search("(.*?),", date_string).group(1)
    date_string = date_string.replace(
        day_of_week_number, day_of_week[day_of_week_number], 1
    )

    # change month name from eng to ru
    for key in months.keys():
        date_string = date_string.replace(key, months[key])

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
    # init base params
    path = Path("./districts")
    subjects = {
        "1": "Водоснабжение",
        "2": "Водоснабжение. Горячая вода",
        "3": "Водоснабжение. Холодная вода",
        "4": "Отопление",
        "5": "Канализация",
        "6": "Техническое обслуживание лифта",
        "7": "Техническое обслуживание ЗПУ",
        "9": "Общестроительные работы",
        "10": "Бытовые услуги",
        "11": "Электроснабжение",
        "12": "Санитарное состояние и благоустройство территории",
        "13": "Санитарное состояние многоквартирного дома",
        "14": "Кровельные работы",
        "15": "Работы по ремонту стыков",
        "16": "Автомобильные дороги, тротуары",
        "17": "Общественные места (Парки, скверы)",
        "18": "Общественный транспорт, остановки общественного транспорта",
        "19": "Рекламные и информационные конструкции и объявления",
        "20": "Другое",
        "22": "Техническое обслуживание зданий и сооружений",
        "23": "Обращение с ТКО",
        "24": "Газоснабжение",
    }
    # list_of_dates_2020 = []
    # for i in range(1, 13):
    #     list_of_dates_2020.append(generate_template_date(2020, i, 1))

    list_of_dates_2020 = [
        # "Суббота, 01 Февраль, 2020",
        "Воскресенье, 01 Март, 2020",
        "Среда, 01 Апрель, 2020",
        "Пятница, 01 Май, 2020",
        "Понедельник, 01 Июнь, 2020",
        "Среда, 01 Июль, 2020",
        "Суббота, 01 Август, 2020",
        "Вторник, 01 Сентябрь, 2020",
        "Четверг, 01 Октябрь, 2020",
        "Воскресенье, 01 Ноябрь, 2020",
        "Вторник, 01 Декарь, 2020",
    ]

    url = "https://115.xn--90ais/portal/wwv_flow.ajax"
    # dymanic params for header:
    cookie = "OracleMapsPlugin_R761175865244051364_7119351139895=16#3088804855624837#7158895191585507#3857; PORTAL_USER_TOKEN=A1D77B502D160AE2C3873E6B39E222D5D0ED10354CDFA10DFAF2A65DF50717F353B04BD473619F3DC851F6A2F94A7F16ED92CA18B54C49758005B5A7EBFC0699; OracleMapsPlugin_R761175865244051364_11018758419082=16#3121932443289751#7171117959163840#3857; ORA_WWV_APP_10901=ORA_WWV-u1YCkIOAGSnp3yaHnj8xyCCa; ORA_WWV_RAC_INSTANCE=2; ai_user=yIAIFgz6SRFD8GLE51HHnU|2022-11-02T09:35:41.515Z"
    referer = (
        "https://115.xn--90ais/portal/f?p=10901:REQUESTS_MAP:115927250491320::NO:::"
    )
    # dynamic params for payload:
    p_instance = "115927250491320"
    p_request = (
        "PLUGIN=2n2UadweTJ2iF35ot19DKuTm3CTkvhXWXZbrYXj6lJRL1wvPrcosrbj50ZfFU9Ky"
    )
    x02 = "3102635348610169"
    x03 = "7141386464106095"
    x04 = "3151115532970673"
    x05 = "7210179788385880"
    protected = "Mm7hxTRZbhHlDs-EWiTw9g"
    salt = "190908242312673376393190041550545746438"

    headers = set_headers_map(cookie=cookie, referer=referer)
    payload = set_payload_map_static(
        p_instance=p_instance,
        p_request=p_request,
        x02=x02,
        x03=x03,
        x04=x04,
        x05=x05,
        protected=protected,
        salt=salt,
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

                # sleep(1)

            # final version of request list
            list_of_requests = list_with_main_info
            # save final results
            # set old var
            payload = set_payload_map_static(
                p_instance=p_instance,
                p_request=p_request,
                x02=x02,
                x03=x03,
                x04=x04,
                x05=x05,
                protected=protected,
                salt=salt,
            )
            url = "https://115.xn--90ais/portal/wwv_flow.ajax"
            headers = set_headers_map(cookie=cookie, referer=referer)
            period_temp_list.extend(list_of_requests)

        with open(path / f"{period}.json", "w", encoding="utf8") as f:
            json.dump(period_temp_list, f, ensure_ascii=False)


if __name__ == "__main__":
    main()
