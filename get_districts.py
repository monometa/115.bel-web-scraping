from bs4 import BeautifulSoup
import requests
import json
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

path = Path('./districts')

url = "https://115.xn--90ais/portal/wwv_flow.ajax"

headers = {
    "Accept": "text/plain, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-GB,en-US;q=0.9,en-BY;q=0.8,en;q=0.7,ru;q=0.6",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    # Cookie - changeable / required
    "Cookie": "OracleMapsPlugin_R230481754811300191_112436741479372=12#3510297900052315#7043126665926469#3857; OracleMapsPlugin_R761175865244051364_117010452400746=16#3042289909025283#7122950744367010#3857; OracleMapsPlugin_R230481754811300191_117010452400746=8#3015307456802929#7053064102975974#3857; ORA_WWV_APP_10901=ORA_WWV-rY96uJQUZWm6T6KR2QkM30WY; ORA_WWV_RAC_INSTANCE=2; ai_user=Yq0/qds2joAOnrIdk05PEv|2022-10-20T14:47:43.541Z",
    "Host": "115.xn--90ais",
    "Origin": "https://115.xn--90ais",
    # Referer - changeable / undefined
    "Referer": "https://115.xn--90ais/portal/f?p=10901:STATS:106524610439182::NO:::",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "sec-ch-ua": '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Linux",
}

def get_regions_txt_f(province='', district=''):

    json_params = {
        "pageItems": {
            "itemsToSubmit": [{"n": "P13_PROVINCE", "v": province}],
            # protected - changeable / required (90%)
            "protected": "331wi9jOlFUppgAc4MbRdw",
            "rowVersion": "",
        },
        # salt changeable / required (90%)
        "salt": "252192007786642650144639477077550855919",
    }

    data = {
        "p_flow_id": "10901",
        "p_flow_step_id": "13",
        # p_instance - changeable / undefined
        "p_instance": "106524610439182",
        "p_debug": "",
        # p_request - changeable / required (90%)
        "p_request": "PLUGIN=X9tUoFzmtW_35JWIrmauluaMeQgblFtsAzvuZtx9gCrZTKDqzzYXwJ65hombTjdt",
        "p_json": json.dumps(json_params)
    }

    # print(province)

    filename = f"{province}.txt"

    with requests.Session() as s:
        s.headers.update(headers)

        r = s.post(url=url, data=data)
        print(r.url)
        text_d = r.text

        with open(path / filename, "w+", encoding="utf8") as f:
            json.dump(text_d, f, ensure_ascii=False)
    
    return filename

def transform_txt_f_2_html(filename):
    with open(path / filename) as f:
        lines = f.readlines()
        flow_string = lines[0]
        flow_string = flow_string[1:-1]
        flow_string = flow_string.replace('\\n',"")
        flow_string = flow_string.replace('\\',"")

    Path.unlink(path / filename) 

    html_filename = f'{filename[:-4]}.html'

    with open (path / html_filename, 'w') as f:
        f.writelines(flow_string)
    
    return html_filename

def extract_regions_from_html_save_2_csv(html_filename):

    data_piece = {}

    with open (path / html_filename, 'r') as f:
        content = f.read()
        soup = BeautifulSoup(content, 'html.parser')

        for option in soup.find_all('option'):
            data_piece[option['value']] = option.text
    
    Path.unlink(path / html_filename) 

    with open(path / f'{html_filename[:-4]}csv', 'w') as csv_file:  
        writer = csv.writer(csv_file)
        for key, value in data_piece.items():
            writer.writerow([key, value])


def main():
    provinces = ['21', '41', '78', '124', '170', '251', '207']

    for province in (provinces):
        PROVINCE_NUMBER = province
        # print(province)
        regions_txt_f = get_regions_txt_f(PROVINCE_NUMBER)
        regions_html_f = transform_txt_f_2_html(regions_txt_f)
        extract_regions_from_html_save_2_csv(regions_html_f)
        sleep(2)

if __name__ == "__main__":
    main()
