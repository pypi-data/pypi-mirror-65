#     Copyright 2020. ThingsBoard
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.

import time
import string
import random
from threading import Thread
from re import match, fullmatch, search, sub
import ssl
from paho.mqtt.client import Client
from thingsboard_gateway.connectors.connector import Connector, log
from thingsboard_gateway.connectors.mqtt.json_mqtt_uplink_converter import JsonMqttUplinkConverter
from thingsboard_gateway.tb_utility.tb_utility import TBUtility


class MqttConnector(Connector, Thread):
    def __init__(self, gateway, config, connector_type):
        super().__init__()
        self.__log = log
        self.config = config
        self._connector_type = connector_type
        self.statistics = {'MessagesReceived': 0,
                           'MessagesSent': 0}
        self.__gateway = gateway
        self.__broker = config.get('broker')
        self.__mapping = config.get('mapping')
        self.__server_side_rpc = config.get('serverSideRpc', [])
        self.__service_config = {"connectRequests": [], "disconnectRequests": []}
        self.__attribute_updates = config.get("attributeUpdates")
        self.__get_service_config(config)
        self.__sub_topics = {}
        client_id = ''.join(random.choice(string.ascii_lowercase) for _ in range(23))
        self._client = Client(client_id)
        self.setName(config.get("name", self.__broker.get("name", 'Mqtt Broker ' + ''.join(random.choice(string.ascii_lowercase) for _ in range(5)))))
        if "username" in self.__broker["security"]:
            self._client.username_pw_set(self.__broker["security"]["username"],
                                         self.__broker["security"]["password"])
        if "caCert" in self.__broker["security"] or self.__broker["security"].get("type", "none").lower() == "tls":
            ca_cert = self.__broker["security"].get("caCert")
            private_key = self.__broker["security"].get("privateKey")
            cert = self.__broker["security"].get("cert")
            if ca_cert is None:
                self._client.tls_set_context(ssl.SSLContext(ssl.PROTOCOL_TLSv1_2))
            else:
                try:
                    self._client.tls_set(ca_certs=ca_cert,
                                         certfile=cert,
                                         keyfile=private_key,
                                         cert_reqs=ssl.CERT_REQUIRED,
                                         tls_version=ssl.PROTOCOL_TLSv1_2,
                                         ciphers=None)
                except Exception as e:
                    self.__log.error("Cannot setup connection to broker %s using SSL. Please check your configuration.\nError: ",
                                     self.get_name())
                    self.__log.exception(e)
                self._client.tls_insecure_set(False)
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message
        self._client.on_subscribe = self._on_subscribe
        self.__subscribes_sent = {}  # For logging the subscriptions
        self._client.on_disconnect = self._on_disconnect
        # self._client.on_log = self._on_log
        self._connected = False
        self.__stopped = False
        self.daemon = True

    def is_connected(self):
        return self._connected

    def open(self):
        self.__stopped = False
        self.start()

    def run(self):
        try:
            while not self._connected and not self.__stopped:
                try:
                    self._client.connect(self.__broker['host'],
                                         self.__broker.get('port', 1883))
                    self._client.loop_start()
                    if not self._connected:
                        time.sleep(1)
                except Exception as e:
                    self.__log.exception(e)
                    time.sleep(10)

        except Exception as e:
            self.__log.exception(e)
            try:
                self.close()
            except Exception as e:
                self.__log.exception(e)
        while True:
            if self.__stopped:
                break
            time.sleep(.01)

    def close(self):
        self.__stopped = True
        try:
            self._client.disconnect()
        except Exception as e:
            log.exception(e)
        self._client.loop_stop()
        self.__log.info('%s has been stopped.', self.get_name())

    def get_name(self):
        return self.name

    def __subscribe(self, topic):
        message = self._client.subscribe(topic)
        try:
            self.__subscribes_sent[message[1]] = topic
        except Exception as e:
            self.__log.exception(e)

    def _on_connect(self, client, userdata, flags, result_code, *extra_params):
        result_codes = {
            1: "incorrect protocol version",
            2: "invalid client identifier",
            3: "server unavailable",
            4: "bad username or password",
            5: "not authorised",
        }
        if result_code == 0:
            self._connected = True
            self.__log.info('%s connected to %s:%s - successfully.', self.get_name(), self.__broker["host"], self.__broker.get("port", "1883"))
            self.__log.debug("Client %s, userdata %s, flags %s, extra_params %s", str(client), str(userdata), str(flags), extra_params)
            for mapping in self.__mapping:
                try:
                    converter = None
                    if mapping["converter"]["type"] == "custom":
                        module = TBUtility.check_and_import(self._connector_type, mapping["converter"]["extension"])
                        if module is not None:
                            self.__log.debug('Custom converter for topic %s - found!', mapping["topicFilter"])
                            converter = module(mapping)
                        else:
                            self.__log.error("\n\nCannot find extension module for %s topic.\nPlease check your configuration.\n", mapping["topicFilter"])
                    else:
                        converter = JsonMqttUplinkConverter(mapping)
                    if converter is not None:
                        regex_topic = TBUtility.topic_to_regex(mapping.get("topicFilter"))
                        if not self.__sub_topics.get(regex_topic):
                            self.__sub_topics[regex_topic] = []

                        self.__sub_topics[regex_topic].append({converter: None})
                        # self._client.subscribe(TBUtility.regex_to_topic(regex_topic))
                        self.__subscribe(mapping["topicFilter"])
                        self.__log.info('Connector "%s" subscribe to %s',
                                        self.get_name(),
                                        TBUtility.regex_to_topic(regex_topic))
                    else:
                        self.__log.error("Cannot find converter for %s topic", mapping["topicFilter"])
                except Exception as e:
                    self.__log.exception(e)
            try:
                for request in self.__service_config:
                    if self.__service_config.get(request) is not None:
                        for request_config in self.__service_config.get(request):
                            self.__subscribe(request_config["topicFilter"])
            except Exception as e:
                self.__log.error(e)

        else:
            if result_code in result_codes:
                self.__log.error("%s connection FAIL with error %s %s!", self.get_name(), result_code, result_codes[result_code])
            else:
                self.__log.error("%s connection FAIL with unknown error!", self.get_name())

    def _on_disconnect(self, *args):
        self.__log.debug('"%s" was disconnected. %s', self.get_name(), str(args))

    def _on_log(self, *args):
        self.__log.debug(args)

    def _on_subscribe(self, _, __, mid, granted_qos):
        try:
            if granted_qos[0] == 128:
                self.__log.error('"%s" subscription failed to topic %s subscription message id = %i', self.get_name(), self.__subscribes_sent.get(mid), mid)
            else:
                self.__log.info('"%s" subscription success to topic %s, subscription message id = %i', self.get_name(), self.__subscribes_sent.get(mid), mid)
                if self.__subscribes_sent.get(mid) is not None:
                    del self.__subscribes_sent[mid]
        except Exception as e:
            self.__log.exception(e)

    def __get_service_config(self, config):
        for service_config in self.__service_config:
            if config.get(service_config):
                self.__service_config[service_config] = config[service_config]

    def _on_message(self, client, userdata, message):
        self.statistics['MessagesReceived'] += 1
        content = TBUtility.decode(message)

        # Check if message topic exists in mappings "i.e., I'm posting telemetry/attributes"
        regex_topic = [regex for regex in self.__sub_topics if fullmatch(regex, message.topic)]
        if regex_topic:
            try:
                for regex in regex_topic:
                    if self.__sub_topics.get(regex):
                        for converter_value in range(len(self.__sub_topics.get(regex))):
                            if self.__sub_topics[regex][converter_value]:
                                for converter in self.__sub_topics.get(regex)[converter_value]:
                                    converted_content = converter.convert(message.topic, content)
                                    if converted_content:
                                        try:
                                            self.__sub_topics[regex][converter_value][converter] = converted_content
                                        except Exception as e:
                                            self.__log.exception(e)
                                        self.__gateway.send_to_storage(self.name, converted_content)
                                        self.statistics['MessagesSent'] += 1
                                    else:
                                        continue
                            else:
                                self.__log.error('Cannot find converter for the topic:"%s"! Client: %s, User data: %s', message.topic, str(client), str(userdata))
                                return None
            except Exception as e:
                log.exception(e)
            return None

        # Check if message topic is matched by an existing connection request handler
        if self.__service_config.get("connectRequests"):
            for request in self.__service_config["connectRequests"]:

                # Check that the current connection request handler defines a topic filter (mandatory)
                if request.get("topicFilter") is None:
                    continue

                found_device_name = None
                found_device_type = 'default'

                # Extract device name and type from regexps, if any.
                # This cannot be postponed because message topic may contain wildcards
                if request.get("deviceNameJsonExpression"):
                    found_device_name = TBUtility.get_value(request["deviceNameJsonExpression"], content)
                if request.get("deviceNameTopicExpression"):
                    device_name_expression = request["deviceNameTopicExpression"]
                    device_name_match = search(device_name_expression, message.topic)
                    if device_name_match is not None:
                        found_device_name = device_name_match.group(0)
                if request.get("deviceTypeJsonExpression"):
                    found_device_type = TBUtility.get_value(request["deviceTypeJsonExpression"], content)
                if request.get("deviceTypeTopicExpression"):
                    device_type_expression = request["deviceTypeTopicExpression"]
                    found_device_type = search(device_type_expression, message.topic)

                # Check if request topic matches with message topic before of after regexp substitution
                if message.topic not in request.get("topicFilter"):
                    sub_topic = message.topic
                    # Substitute device name (if defined) in topic
                    if found_device_name is not None:
                        sub_topic = sub(found_device_name, "+", sub_topic)
                    # Substitute device type in topic
                    sub_topic = sub(found_device_type, "+", sub_topic)
                    # If topic still not matches, this is not the correct handler

                    if sub_topic not in request.get("topicFilter"):
                        continue

                # I'm now sure that this message must be handled by this connection request handler
                if found_device_name is None:
                    self.__log.error("Device name missing from connection request")
                    return None

                # Note: device must be added even if it is already known locally: else ThingsBoard
                # will not send RPCs and attribute updates
                self.__gateway.add_device(found_device_name, {"connector": self}, device_type=found_device_type)
                return None

        # Check if message topic is matched by an existing disconnection request handler
        if self.__service_config.get("disconnectRequests"):
            for request in self.__service_config["disconnectRequests"]:
                # Check that the current disconnection request handler defines a topic filter (mandatory)
                if request.get("topicFilter") is None:
                    continue

                found_device_name = None
                found_device_type = 'default'

                # Extract device name and type from regexps, if any.
                # This cannot be postponed because message topic may contain wildcards
                if request.get("deviceNameJsonExpression"):
                    found_device_name = TBUtility.get_value(request["deviceNameJsonExpression"], content)
                if request.get("deviceNameTopicExpression"):
                    device_name_expression = request["deviceNameTopicExpression"]
                    device_name_match = search(device_name_expression, message.topic)
                    if device_name_match is not None:
                        found_device_name = device_name_match.group(0)
                if request.get("deviceTypeJsonExpression"):
                    found_device_type = TBUtility.get_value(request["deviceTypeJsonExpression"], content)
                if request.get("deviceTypeTopicExpression"):
                    device_type_expression = request["deviceTypeTopicExpression"]
                    found_device_type = search(device_type_expression, message.topic)

                # Check if request topic matches with message topic before of after regexp substitution
                if message.topic not in request.get("topicFilter"):
                    sub_topic = message.topic
                    # Substitute device name (if defined) in topic
                    if found_device_name is not None:
                        sub_topic = sub(found_device_name, "+", sub_topic)
                    # Substitute device type in topic
                    sub_topic = sub(found_device_type, "+", sub_topic)
                    # If topic still not matches, this is not the correct handler

                    if sub_topic not in request.get("topicFilter"):
                        continue

                # I'm now sure that this message must be handled by this connection request handler
                if found_device_name is None:
                    self.__log.error("Device name missing from disconnection request")
                    return None

                if found_device_name in self.__gateway.get_devices():
                    self.__log.info("Device %s of type %s disconnected", found_device_name, found_device_type)
                    self.__gateway.del_device(found_device_name)
                else:
                    self.__log.info("Device %s is already disconnected", found_device_name)
                return None

        if message.topic in self.__gateway.rpc_requests_in_progress:
            self.__gateway.rpc_with_reply_processing(message.topic, content)
        else:
            self.__log.debug("Received message to topic \"%s\" with unknown interpreter data: \n\n\"%s\"",
                             message.topic,
                             content)

    def on_attributes_update(self, content):
        if self.__attribute_updates:
            for attribute_update in self.__attribute_updates:
                if match(attribute_update["deviceNameFilter"], content["device"]):
                    for attribute_key in content["data"]:
                        if match(attribute_update["attributeFilter"], attribute_key):
                            try:
                                topic = attribute_update["topicExpression"]\
                                        .replace("${deviceName}", content["device"])\
                                        .replace("${attributeKey}", attribute_key)\
                                        .replace("${attributeValue}", content["data"][attribute_key])
                            except KeyError as e:
                                log.exception("Cannot form topic, key %s - not found", e)
                                raise e
                            try:
                                data = attribute_update["valueExpression"]\
                                        .replace("${attributeKey}", attribute_key)\
                                        .replace("${attributeValue}", content["data"][attribute_key])
                            except KeyError as e:
                                log.exception("Cannot form topic, key %s - not found", e)
                                raise e
                            self._client.publish(topic, data).wait_for_publish()
                            self.__log.debug("Attribute Update data: %s for device %s to topic: %s", data, content["device"], topic)
                        else:
                            self.__log.error("Cannot find attributeName by filter in message with data: %s", content)
                else:
                    self.__log.error("Cannot find deviceName by filter in message with data: %s", content)
        else:
            self.__log.error("Attribute updates config not found.")

    def server_side_rpc_handler(self, content):
        for rpc_config in self.__server_side_rpc:
            if search(rpc_config["deviceNameFilter"], content["device"]) \
                    and search(rpc_config["methodFilter"], content["data"]["method"]) is not None:
                # Subscribe to RPC response topic
                if rpc_config.get("responseTopicExpression"):
                    topic_for_subscribe = rpc_config["responseTopicExpression"] \
                        .replace("${deviceName}", content["device"]) \
                        .replace("${methodName}", content["data"]["method"]) \
                        .replace("${requestId}", str(content["data"]["id"])) \
                        .replace("${params}", content["data"]["params"])
                    if rpc_config.get("responseTimeout"):
                        timeout = time.time()*1000+rpc_config.get("responseTimeout")
                        self.__gateway.register_rpc_request_timeout(content,
                                                                    timeout,
                                                                    topic_for_subscribe,
                                                                    self.rpc_cancel_processing)
                        # Maybe we need to wait for the command to execute successfully before publishing the request.
                        self._client.subscribe(topic_for_subscribe)
                    else:
                        self.__log.error("Not found RPC response timeout in config, sending without waiting for response")
                # Publish RPC request
                if rpc_config.get("requestTopicExpression") is not None\
                        and rpc_config.get("valueExpression"):
                    topic = rpc_config.get("requestTopicExpression")\
                        .replace("${deviceName}", content["device"])\
                        .replace("${methodName}", content["data"]["method"])\
                        .replace("${requestId}", str(content["data"]["id"]))\
                        .replace("${params}", content["data"]["params"])
                    data_to_send = rpc_config.get("valueExpression")\
                        .replace("${deviceName}", content["device"])\
                        .replace("${methodName}", content["data"]["method"])\
                        .replace("${requestId}", str(content["data"]["id"]))\
                        .replace("${params}", content["data"]["params"])
                    try:
                        self._client.publish(topic, data_to_send)
                        self.__log.debug("Send RPC with no response request to topic: %s with data %s",
                                         topic,
                                         data_to_send)
                        if rpc_config.get("responseTopicExpression") is None:
                            self.__gateway.send_rpc_reply(device=content["device"], req_id=content["data"]["id"], success_sent=True)
                    except Exception as e:
                        self.__log.exception(e)

    def rpc_cancel_processing(self, topic):
        self._client.unsubscribe(topic)

