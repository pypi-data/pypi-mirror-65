import json
import xmltodict


def xml_to_json(xml_str):
    data = xmltodict.parse(xml_str)
    return json.dumps(data)
