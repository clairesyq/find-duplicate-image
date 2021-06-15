import concurrent.futures
import json
import requests

url = "https://a28-04-05-9200.proxy.op-mobile.opera.com/transcode_parser_result-*/_search"
str = "{\"size\":500,\"query\":{\"filtered\":{\"filter\":{\"bool\":{\"must\":[{\"range\":{\"@timestamp\":{\"gte\":1623296178181,\"lte\":1623297078181,\"format\":\"epoch_millis\"}}},{\"range\":{\"no_of_pictures\":{\"gt\":1}}}]}}}},\"_source\":{\"includes\":[\"url\",\"pictures\"]}}"
rsp = requests.request("POST", url, data=str)
rsp_dict = json.loads(rsp.text)
web_dict_list = rsp_dict['hits']['hits']

# not multithreading version
# for i in range(len(web_dict_list)):
#     web_dict = web_dict_list[i]
#     web_str = json.dumps(web_dict)

#     headers = {'Content-type': 'application/json'}
#     Response = requests.request(
#         "POST", "http://127.0.0.1:5000/findDup", headers=headers, json=web_str)
#     print(Response.text)

# multi-threading requests


def request_post(web_dict):
    web_str = json.dumps(web_dict)
    headers = {'Content-type': 'application/json'}
    Response = requests.request(
        "POST", "http://127.0.0.1:5000/findDup", headers=headers, json=web_str)
    print(Response.text)
    # return Response.text


with concurrent.futures.ThreadPoolExecutor() as executor:
    res = [executor.submit(request_post, data) for data in web_dict_list]
    concurrent.futures.wait(res)
