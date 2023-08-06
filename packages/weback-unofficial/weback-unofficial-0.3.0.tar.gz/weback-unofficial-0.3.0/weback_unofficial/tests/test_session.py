from unittest import TestCase

from weback_unofficial.client import WebackApi
from weback_unofficial.vacuum import CleanRobot
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
        # devices = self.client.device_list()
        # device_name = devices[0]['Thing_Name']

        # # via client
        # resp = self.client.publish_device_msg(device_name, {"working_status": "AutoClean"})
        # print(resp)

        # # via boto3
        # time.sleep(5)
        # client = session.client('iot-data')
        # topic = f"$aws/things/{device_name}/shadow/update"
        # payload = {
        #     'state': {
        #         'desired': {
        #             "working_status": "BackCharging"
        #         }
        #     }
        # }
        # resp = client.publish(topic=topic, qos = 0, payload = json.dumps(payload))
        # print(resp)

    def test_device_description(self):
        session = self.client.get_session()
        devices = self.client.device_list()
        print(devices)
        device_name = devices[0]['Thing_Name']

        desc = self.client.get_device_description(device_name)
        print(desc)

        shadow = self.client.get_device_shadow(device_name)
        print(shadow)

    def test_vacuum_class(self):
        session = self.client.get_session()
        devices = self.client.device_list()
        device_name = devices[0]['Thing_Name']
        vacuum = CleanRobot(device_name, self.client)
        self.assertIsInstance(vacuum.battery_level, int)
        print(vacuum.state)
        print(vacuum.current_mode)

        vacuum.turn_on()
        print(vacuum.state)
        print(vacuum.current_mode)

        time.sleep(1)
        vacuum.stop()
        print(vacuum.state)
        print(vacuum.current_mode)

        time.sleep(1)
        vacuum.return_home()
        print(vacuum.state)
        print(vacuum.current_mode)