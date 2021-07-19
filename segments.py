import json
import requests
import logging
import threading

API_KEY = "<Insert Edge Impulse API Key here from the Dashboard > Keys"
projectId = "<Your project ID, can be found at Edge Impulse dashboard"


headers = {
    "Accept": "application/json",
    "x-api-key": API_KEY
}

def segment(tid, ids):
    for sampleId in ids:
        url1 = "https://studio.edgeimpulse.com/v1/api/{}/raw-data/{}/find-segments".format(projectId, sampleId)
        payload1 = {
            "shiftSegments": True,
            "segmentLengthMs": 1500
        }
        response1 = requests.request("POST", url1, json=payload1, headers=headers)
        resp1 = json.loads(response1.text)
        segments = resp1["segments"] 
        
        if len(segments) == 0:
            continue

        payload2 = {"segments": segments}
        url2 = "https://studio.edgeimpulse.com/v1/api/{}/raw-data/{}/segment".format(projectId, sampleId)
        response2 = requests.request("POST", url2, json=payload2, headers=headers)
    
        logging.info('{} {} {}'.format(tid, sampleId, response2.text))

 
if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    querystring = {"category":"testing", "excludeSensors":"true"}
    url = "https://studio.edgeimpulse.com/v1/api/{}/raw-data".format(projectId)
    response = requests.request("GET", url, headers=headers, params=querystring)

    resp = json.loads(response.text)
    id_list = list(map(lambda s: s["id"], resp["samples"]))
    div = 8
    n = int(len(id_list) / div)
    threads = list()

    for i in range(div):
        if i ==  (div - 1):
            ids = id_list[n*i: ]
        else:
            ids = id_list[n*i: n*(i+1)]

        x = threading.Thread(target=segment, args=(i, ids))
        threads.append(x)
        x.start()

    for thread in threads:
        thread.join()

    logging.info("Finished")
