from unittest import TestCase

from weback_unofficial.client import WebackApi
import time
import json
import boto3

class TestSession(TestCase):
    def __init__(self, methodName):
        super().__init__(methodName)
        client = WebackApi('+7-9379570101', 'thisiswebackpass')
        sess = client.get_session()
        self.assertIsNotNone(sess)
        self.client = client
        
    def test_device_list(self):
        devices = self.client.device_list()
        # print(devices, type(devices))
        self.assertIsInstance(devices, list)

    def test_device_control(self):
        session = self.client.get_session()
        devices = self.client.device_list()
        device_name = devices[0]['Thing_Name']

        client = session.client('iot-data')
        topic = f"$aws/things/{device_name}/shadow/update"
        payload = {
            'state': {
                'desired': {
                    "working_status": "AutoClean"
                }
            }
        }
        resp = client.publish(topic=topic, qos = 0, payload = json.dumps(payload))
        print(resp)

        time.sleep(5)
        payload = {
            'state': {
                'desired': {
                    "working_status": "BackCharging"
                }
            }
        }
        resp = client.publish(topic=topic, qos = 0, payload = json.dumps(payload))
        print(resp)