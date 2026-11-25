# DataFoundry.py
# A MicroPython to make working with Data Foundry easier
# Written by Diede van Marle

import urequests
import json
import network
import gc

class DataFoundry:
    def __init__(self, instance, deviceID=None):
        self.instance = instance
        self.deviceID = deviceID
        self.url = 'https://{}'.format(self.instance)

    def IoTDataset(self, datasetID, token):
        return(IoTDataset(self, datasetID, token))

    def EntityDataset(self, datasetID, token):
        return(EntityDataset(self, datasetID, token))

    def AIFoundry(self, api_token, model="hermes-2-pro-llama-3-8b", temperature=1):
        return(AIFoundry(self, api_token, model, temperature))

class AIFoundry:
    def __init__(self, parent, api_token, model, temperature):
        self.parent = parent
        self.api_token = api_token
        self.api_url = (self.parent.url)
        self.model = model
        self.temperature = temperature

    def text(self, prompt):
        header = {
            'Content-Type':'application/json',
            'Authorization': f'Bearer {self.api_token}',
        }
        payload={
            "messages": [{"role": "user", "content": prompt}],
            'tempertature': self.temperature,
            'model':self.model,
        }
        print("*** DFLIB: Sending {} with model {} and headers {}".format(payload, self.model, header))

        url = f"{self.api_url}/v1/chat/completions"

        response = urequests.post(
            url = url,
            headers = header,
            data = json.dumps(payload)
        )
        result = json.loads(response.text)
        return(result["choices"][0]["message"]["content"])

class IoTDataset:
    def __init__(self, parent, datasetID, token):
        self.parent = parent
        self.datasetID = datasetID
        self.token = token
        self.datasetURL = (
            self.parent.url +
            '/api/v1/datasets/ts/{}'.format(self.datasetID)
        )

    def send(self, data=None):
        header = {
            'Content-Type':'application/json',
            'activity' : 'ACTIVITY',
            'api_token': self.token,
            'device_id': self.parent.deviceID,
        }

        requesturl = self.datasetURL
        print("*** DFLIB: Sending request to {}".format(requesturl))

        internalPost(
            urlInput = requesturl,
            headerInput = header,
            dataInput = data
        )

class EntityDataset:
    def __init__(self, parent, datasetID, token):
        self.parent = parent
        self.datasetID = datasetID
        self.token = token
        self.datasetURL = (
            self.parent.url +
            '/api/v1/datasets/entity/{}'.format(self.datasetID)
    )

    def add(self, resource, data, token):
        header = {
            'Content-Type':'application/json',
            'api_token': self.token,
            'device_id': self.parent.deviceID,
            'resource_id':resource,
            'token': token
        }

        requesturl = self.datasetURL
        print("*** DFLIB: Sending request to {}".format(requesturl))

        internalPost(
            urlInput = requesturl,
            headerInput = header,
            dataInput = data
        )

    def put(self, resource, data, token):
        header = {
            'Content-Type':'application/json',
            'api_token': self.token,
            'device_id': self.parent.deviceID,
            'resource_id':resource,
            'token': token
        }

        requesturl = self.datasetURL
        print("*** DFLIB: Sending request to {}".format(requesturl))

        internalPut(
            urlInput = requesturl,
            headerInput = header,
            dataInput = data
        )

    def get(self, resource, token):
        header = {
            'Content-Type':'application/json',
            'api_token': self.token,
            'device_id': self.parent.deviceID,
            'resource_id':resource,
            'token': token
        }

        requesturl = self.datasetURL
        print("*** DFLIB: Sending request to {}".format(requesturl))

        result = internalGet(
            urlInput = requesturl,
            headerInput = header
        )

        return result

    def delete(self, resource, token):
        header = {
            'Content-Type':'application/json',
            'api_token': self.token,
            'device_id': self.parent.deviceID,
            'resource_id':resource,
            'token': token
        }

        requesturl = self.datasetURL
        print("*** DFLIB: Sending request to {}".format(requesturl))

        result = internalDelete(
            urlInput = requesturl,
            headerInput = header
        )

        return result

def internalPost(urlInput, headerInput, dataInput):
    try:
        response = urequests.post(
            url = urlInput,
            headers = headerInput,
            data = json.dumps(dataInput),
        )

        response_text = response.text
        status = response.status_code
        print("*** DF Library: ", response_text)
        # Now close it after reading
        response.close()
        gc.collect()
        # # Check if request was successful
        if status >= 200 and status < 300:
            print("*** DF Library: request sent successfully")
        else:
            print("failed")

    except Exception as e:
        print("*** DF Library: Error sending data, ", e)

def internalGet(urlInput, headerInput):
    try:
        response = urequests.get(
            url = urlInput,
            headers = headerInput,
            data = {},
        )

        response_text = response.text
        status = response.status_code
        print("*** DF Library - Response: ", response_text)
        # Now close it after reading

        gc.collect()
        # # Check if request was successful
        if status >= 200 and status < 300:
            print("*** DF Library: request sent successfully")
            return(response.text)
        else:
            print("failed")
        response.close()
    except Exception as e:
        print("*** DF Library: Error sending data, ", e)

def internalPut(urlInput, headerInput, dataInput):
    try:
        response = urequests.put(
            url = urlInput,
            headers = headerInput,
            data = json.dumps(dataInput),
        )

        response_text = response.text
        status = response.status_code
        print("*** DF Library: ", response_text)
        # Now close it after reading
        response.close()
        gc.collect()
        # # Check if request was successful
        if status >= 200 and status < 300:
            print("*** DF Library: request sent successfully")
        else:
            print("failed")

    except Exception as e:
        print("*** DF Library: Error sending data, ", e)

def internalDelete(urlInput, headerInput):
    try:
        response = urequests.delete(
            url = urlInput,
            headers = headerInput,
            data = {},
        )

        response_text = response.text
        status = response.status_code
        print("*** DF Library: ", response_text)
        # Now close it after reading
        response.close()
        gc.collect()
        # # Check if request was successful
        if status >= 200 and status < 300:
            print("*** DF Library: request sent successfully")
        else:
            print("failed")

    except Exception as e:
        print("*** DF Library: Error sending data, ", e)
