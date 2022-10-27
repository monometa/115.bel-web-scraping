import requests

requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ":HIGH:!DH:!aNULL"
try:
    requests.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += (
        ":HIGH:!DH:!aNULL"
    )
except AttributeError:
    pass

url = "https://115.xn--90ais/portal/wwv_flow.ajax"

headers = {
    "Accept": "text/plain, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-GB,en-US;q=0.9,en-BY;q=0.8,en;q=0.7,ru;q=0.6",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Host": "115.xn--90ais",
    # Cookie =  required parameter for a successful request
    "Cookie": "OracleMapsPlugin_R230481754811300191_112436741479372=12#3510297900052315#7043126665926469#3857; ORA_WWV_APP_10901=ORA_WWV-PEwg31l_I4XDT5WUcl_LVTuV; ORA_WWV_RAC_INSTANCE=1; ai_user=Yq0/qds2joAOnrIdk05PEv|2022-10-20T14:47:43.541Z",
    "Origin": "https://115.xn--90ais",
    # "Referer": "https://115.xn--90ais/portal/f?p=10901:STATS:12366086172651::NO:::", # not a constant, probably not important
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "sec-ch-ua": '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Linux",
    "X-Requested-With": "XMLHttpRequest",
}

data = {
    "p_flow_id": "10901",
    "p_flow_step_id": "13",
    "p_instance": "12366086172651",  # not a constant
    "p_debug": "",
    "p_request": "PLUGIN=LMpGhdtMAG0-rBzUHslh53IDGRt8aeaKePjo7Y-HkLKNOhDC9Mpov-Y3MdhcqdNA", # not a constant
}

# Full list of available provinces

province_dict = {
    'Minsk': '21',
    'Brest': '41',
    'Vitebsk': '78',
    'Gomel': '124',
    'Grodno': '170',
    'Mogilev': '207',
    'Minsk-obl': '251',
}

# I think this setting needs to be changed. U can set manually for running some tests 
set_province = province_dict['Mogilev']

json_params = {
        "pageItems": {
            "itemsToSubmit": [{"n": "P13_PROVINCE", "v": set_province}],
            # "protected": "-HcmvJc84xRA_VGWym2lXw", # not a constant
            "rowVersion": "",
        },
        # "salt": "241514531126295724394933485568313279536", # not a constant
    }

with requests.Session() as s:
    s.headers.update(headers)

    r = s.post(url=url, 
        data=data, 
        json=json_params, 
        )

    print(r.text)