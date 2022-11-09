from payload_params import *

class Parser:

    def get_headers_map(cookie, referer):

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

    def get_payload_map_static(
        p_instance=p_instance,
        p_request=p_request,
        some_payload_params=p_request,
        # protected=protected, salt=salt - do not used!
        ) -> dict:
        


        data = {
            "p_flow_id": "10901",
            "p_flow_step_id": "19",
            # p_instance - changeable / undefined
            "p_instance": p_instance,
            "p_debug": "",
            # p_request - changeable / required (90%)
            "p_request": p_request,
            "x01": "3857",
            "x02": some_payload_params['x02'],
            "x03": some_payload_params['x02'],
            "x04": some_payload_params['x02'],
            "x05": some_payload_params['x02'],
            "x06": "N",
            "x07": "11",
            "x10": "FOIDATA",
            "p_json": payload_json_params,
        }

        return data
