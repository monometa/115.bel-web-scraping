# import mailbox
# import urllib3
# import time
# import sys
from sqlite3 import paramstyle
# from urllib import response
import requests
import json
from bs4 import BeautifulSoup
import csv
from time import sleep
from pathlib import Path
# from tqdm import tqdm

requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ":HIGH:!DH:!aNULL"
try:
    requests.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += (
        ":HIGH:!DH:!aNULL"
    )
except AttributeError:
    # no pyopenssl support used / needed / available
    pass


url = "https://115.xn--90ais/portal/wwv_flow.ajax"

headers = {
    "Accept": "text/plain, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-GB,en-US;q=0.9,en-BY;q=0.8,en;q=0.7,ru;q=0.6",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": "OracleMapsPlugin_R230481754811300191_112436741479372=12#3510297900052315#7043126665926469#3857; ORA_WWV_APP_10901=ORA_WWV-eTtce3zq3M5Z-WeyPOH5M1rL; ORA_WWV_RAC_INSTANCE=1; ai_user=Yq0/qds2joAOnrIdk05PEv|2022-10-20T14:47:43.541Z",
    "Host": "115.xn--90ais",
    "Origin": "https://115.xn--90ais",
    "Referer": "https://115.xn--90ais/portal/f?p=10901:STATS:7914683460867::NO:::",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "sec-ch-ua": '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Linux",
}

data = {
    "p_flow_id": "10901",
    "p_flow_step_id": "13",
    "p_instance": "7914683460867",
    "p_debug": "",
    "p_request": "PLUGIN=29TCeEOiRsUI88In6qKHqASnSdh7H7V5dIKy7mUnsZZCdMgpz5ui6e5tc_WPL0yr",
}


def get_regions_txt_f(province='', district=''):

    json_params = {
        "pageItems": {
            "itemsToSubmit": [{"n": "P13_PROVINCE", "v": province}],
            "protected": "DUFwSW271qPCfgvRTLmbJA",
            "rowVersion": "",
        },
        "salt": "239991567622198998431068489647954241642",
    }

    print(province)

    p = Path('.')
    filename = f"{p}/province_{province}_disticts.txt"

    with requests.Session() as s:
        s.headers.update(headers)

        r = s.post(url=url, data=data, json=json_params)
        print(r.url)
        text_d = r.text

        with open(filename, "w+", encoding="utf8") as f:
            json.dump(text_d, f, ensure_ascii=False)

    return filename

def transform_txt_f_2_html(filename):
    with open(filename) as f:
        lines = f.readlines()
        flow_string = lines[0]
        flow_string = flow_string[1:-1]
        flow_string = flow_string.replace('\\n',"")
        flow_string = flow_string.replace('\\',"")

    html_filename = f'{filename[:-4]}.html'

    with open (html_filename, 'w') as f:
        f.writelines(flow_string)

    return html_filename

def extract_regions_from_html_save_2_csv(html_filename):

    data_piece = {}

    with open (html_filename, 'r') as f:
        content = f.read()
        soup = BeautifulSoup(content, 'html.parser')

        for option in soup.find_all('option'):
            data_piece[option['value']] = option.text

    with open(f'{html_filename[:-4]}csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in data_piece.items():
            writer.writerow([key, value])


def main():
    # provinces = ['21', '41', '78', '124', '170', '251', '207']

    # for province in (provinces):
    #     PROVINCE_NUMBER = province
    #     print(province)
    #     regions_txt_f = get_regions_txt_f(PROVINCE_NUMBER)
    #     regions_html_f = transform_txt_f_2_html(regions_txt_f)
    #     extract_regions_from_html_save_2_csv(regions_html_f)

    PROVINCE_NUMBER = '21'
    # regions_txt_f = get_regions_txt_f(PROVINCE_NUMBER)
    # regions_html_f = transform_txt_f_2_html(regions_txt_f)
    # extract_regions_from_html_save_2_csv(regions_html_f)


if __name__ == "__main__":
    main()
