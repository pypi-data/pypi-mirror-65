# -*- coding:utf-8 -*-
import paho.mqtt.client
import json
import urllib.parse
import urllib.request
import uuid
import threading
import time
from aiotcloud import pyword
from queue import Queue

DATA = 0
SUBSCRIBE = 1
UNSUBSCRIBE = 2
PUBLISH = 3
CONNECT_ERROR = 4
LOST_CONNECTED = 5
MESSAGE = 6
SYSTEM_INFO = 7
CONNECTED = 8
DEVICE_INFO = 9
DEVICE_DATA = 10


class Data:
    def __init__(self, type, raw_data):
        self.raw_data = raw_data
        self.dics = None
        if isinstance(raw_data, str):
            if type is DEVICE_INFO:
                isJson = self.is_json(raw_data)
                if isJson:
                    self.dics = json.loads(raw_data)
                else:
                    raw_data = raw_data.replace("hard_id\":", "hard_id\":\"")
                    raw_data = raw_data.replace(",\"device_id", "\",\"device_id")
                    if self.is_json(raw_data):
                        self.dics = json.loads(raw_data)
            elif type is DATA:
                if self.is_json(raw_data):
                    self.dics = json.loads(raw_data)

    def get(self, name):
        if self.dics is None:
            return "null"
        elif name in self.dics.keys():
            return self.dics[name]
        else:
            return "null"

    def raw(self):
        return self.raw_data

    def is_json(self, myjson):
        try:
            json_object = json.loads(myjson)
        except ValueError as e:
            return False
        return True


class Device:
    def __init__(self):
        self.name = "ESP8266"
        self.baut = 115200
        self.topic = ""
        self.did = 0
        self.hid = ""

        # self.status = 0
        # self.last_msg = ""
        # self.last_msg_time = ""

        self.iot_client = None
        self._on_data = None
        self._on_msg = None

        self.encode = "UTF-8"

        self.led_status = [0, 0, 0, 0, 0]
        self.io_status = [0, 0, 0, 0]

    # led toggle default led is led0
    def led_toggle(self, led=0):
        if led < 2:
            self.led_status[led] = (self.led_status[led] + 1) % 2
            self.send_control("l" + str(led) + str(self.led_status[led]))

    def led_on(self, led):
        self.send_control("l" + str(led) + '1')

    def led_off(self, led):
        self.send_control("l" + str(led) + '0')

    # # io toggle default io is io0
    def io_toggle(self, io=0):
        if io < 4:
            self.led_status[io] = (self.led_status[io] + 1) % 2
            self.send_control("o" + str(io + 1) + str(self.led_status[io]))

    def io_on(self, io=0):
        self.send_control("o" + str(io + 1) + '1')

    def io_off(self, io=0):
        self.send_control("p" + str(io + 1) + '0')

    @property
    def on_data(self):
        return self._on_data

    @on_data.setter
    def on_data(self, func):
        self._on_data = func

    @property
    def on_msg(self):
        return self.on_msg

    @on_msg.setter
    def on_msg(self, func):
        self._on_msg = func

    def get_pubtopic(self):
        return "/esp8266/sub" + self.topic

    def get_subtopic(self):
        return "/esp8266/pub" + self.topic

    def get_controltopic(self):
        return "/esp8266/control" + self.topic

    def send(self, data):
        if self.did > 0:
            self.iot_client.mqtt_client.publish(self.get_pubtopic(), data)

    def send_control(self, data):
        if self.did > 0:
            self.iot_client.mqtt_client.publish(self.get_controltopic(), data)

    def text(self, t_text, x=0, y=0, size=16):
        pyword.text(t_text, x, y, 16, self.iot_client, self.did)

    def text_clear(self, len=0, x=0, y=0, size=64):
        pyword.clear(len, x, y, size, client=self.iot_client, did=self.did)

    # def send(self, device_id, data):
    #     topic = self.devices_reverse[device_id]
    #     if topic is not None:
    #         self.mqtt_client.publish(topic, data)
    #
    # def send_control(self, device_id, data):
    #     topic = self.devices_control[device_id]
    #     if topic is not None:
    #         self.mqtt_client.publish(topic, data)


class IotClient(threading.Thread):
    def __init__(self, username="", password="", mqtt_address="120.79.0.116", mqtt_port=1883):
        super(IotClient, self).__init__()
        address = mqtt_address
        client_id = "/python/" + str(username)
        self.mqtt_client = paho.mqtt.client.Client(client_id)
        self.mqtt_client.username_pw_set(username, password)
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.on_disconnect = self.on_disconnect
        self.mqtt_client.on_subscribe = self.on_subscribe
        self.mqtt_client.on_publish = self.on_publish

        self.queue = Queue()
        self.mqtt_client.connect(address, mqtt_port, 60)

        self._on_data = None
        self._on_msg = None
        self._callback_mutex = threading.RLock()

        # from did to Device object
        self.devices_map = {}
        # from subtopic to did
        self.devices = {}
        self.devices_control = {}
        self.devices_reverse = {}

        # 调用自己的start方法开始运行
        self.start()

    @property
    def on_data(self):
        return self._on_data

    @on_data.setter
    def on_data(self, func):
        with self._callback_mutex:
            self._on_data = func

    @property
    def on_msg(self):
        return self._on_msg

    @on_msg.setter
    def on_msg(self, func):
        with self._callback_mutex:
            self._on_msg = func

    @staticmethod
    def get_mac_address():
        mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
        return "".join([mac[e:e + 2] for e in range(0, 11, 2)])

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.queue.put((CONNECTED, "连接成功"))
        elif rc == 1:
            self.queue.put((CONNECT_ERROR, "连接失败，原因：不正确的控制协议"))
        elif rc == 2:
            self.queue.put((CONNECT_ERROR, "连接失败，原因：无效的客户端id"))
        elif rc == 3:
            self.queue.put((CONNECT_ERROR, "连接失败，原因：找不到服务器，服务地址或者端口错误"))
        elif rc == 4:
            self.queue.put((CONNECT_ERROR, "连接失败，原因：错误的用户名或密码"))
        elif rc == 5:
            self.queue.put((CONNECT_ERROR, "连接失败，原因：没有认证"))
        """
        The value of rc indicates success or not:
            0: Connection successful
            1: Connection refused - incorrect protocol version
            2: Connection refused - invalid client identifier
            3: Connection refused - server unavailable
            4: Connection refused - bad username or password
            5: Connection refused - not authorised
            6-255: Currently unused.
        """

    def on_message(self, client, userdata, msg):
        data = {'device_id': self.devices[msg.topic], 'topic': msg.topic, 'data': msg.payload}
        str_data = msg.payload.decode()
        if str(str_data).find("hard_id") > 0 and str(str_data).find("runtime") > 0:
            self.queue.put((DEVICE_INFO, data))
        else:
            self.queue.put((DATA, data))

    def on_disconnect(self):
        self.queue.put((LOST_CONNECTED, "连接断开"))

    def on_subscribe(self, client, obj, mid, granted_qos):
        self.queue.put((SUBSCRIBE, "话题订阅成功"))

    def on_publish(self, client, obj, mid):
        self.queue.put((PUBLISH, "消息发送成功"))

    def add_device(self, device_secret, url="http://139.9.131.171/sdk/pyiot", on_data=None, on_msg=None):
        did = device_secret['did']
        secret = device_secret['secret']
        dic = {'did': did,
               'secret': secret}
        dices = [dic]
        text = json.dumps(dices)
        data = {"devices": text}
        encode_data = urllib.parse.urlencode(data)
        data = encode_data.encode()
        response = urllib.request.urlopen(url=url, data=data)
        result = response.read().decode()
        result = json.loads(result)
        if result['error_code'] == 0:
            if len(result['data']['devices']) > 0:
                for device in result['data']['devices']:
                    print("device:" + device['name'] + "   id为：" + str(device['did']) + " add Success")
                    self.mqtt_client.subscribe("/esp8266/pub" + str(device['hid']), 0)
                    self.devices["/esp8266/pub" + str(device['hid'])] = device['did']
                    self.devices_reverse[device['did']] = "/esp8266/sub" + str(device['hid'])
                    self.devices_control[device['did']] = "/esp8266/control" + str(device['hid'])
                    new_device = Device()
                    new_device.baut = device['rate']
                    new_device.did = device['did']
                    new_device.hid = device['hid']
                    new_device.uid = device['uid']
                    new_device.topic = device['topic']
                    new_device.iot_client = self

                    new_device.on_data = on_data
                    new_device.on_msg = on_msg
                    new_device.endmark = device['endmark']
                    new_device.format = device['format']
                    new_device.createtime = device['createtime']

                    # create hash
                    self.devices_map[device['did']] = new_device

                    return new_device

    def send(self, device_id, data):
        topic = self.devices_reverse[device_id]
        if topic is not None:
            self.mqtt_client.publish(topic, data)

    def send_control(self, device_id, data):
        topic = self.devices_control[device_id]
        if topic is not None:
            self.mqtt_client.publish(topic, data)

    def run(self):
        while True:
            self.mqtt_client.loop_start()
            time.sleep(0.25)
            while not self.queue.empty():
                types, data = self.queue.get()

                if types == DATA:
                    if self._on_data is not None:
                        self._on_data(Data(types, data))

                    device = self.devices_map[data['device_id']]
                    if device is not None and device._on_data is not None:
                        data_text = data['data'].decode(device.encode)
                        device._on_data(Data(types, Data(types, data_text)), device)

                elif types == DEVICE_INFO:
                    if self._on_msg is not None:
                        self._on_msg(Data(types, data))

                    device = self.devices_map[data['device_id']]
                    if device is not None and device._on_msg is not None:
                        data_text = data['data'].decode(device.encode)
                        device._on_msg(type, Data(types, data_text), device)

                elif self._on_msg is not None:
                    self._on_msg(types, Data(types, data))
