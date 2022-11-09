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


payload_json_params = {
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
