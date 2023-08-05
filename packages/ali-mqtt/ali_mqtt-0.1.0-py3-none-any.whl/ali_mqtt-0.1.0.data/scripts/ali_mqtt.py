import hashlib
import hmac
import time

__version__ = '0.1.0'


def generate_keys(_product_key, _device_name, _device_secret, _method='hmacsha1'):
    _timestamp = str(int(round(time.time() * 1000)))
    _broker = "{0}.iot-as-mqtt.cn-shanghai.aliyuncs.com".format(_product_key)
    _username = "{0}&{1}".format(_device_name, _product_key)
    _password_rule = "clientId{0}.{1}deviceName{1}productKey{0}timestamp{2}"
    _client_id_rule = "{0}.{1}|timestamp={2},_v=qiezi,securemode=2,signmethod={3}|"
    _raw_password = _password_rule.format(_product_key, _device_name, _timestamp)
    _client_id = _client_id_rule.format(_product_key, _device_name, _timestamp, _method)
    _password = ''
    if _method == 'hmacsha1':
        _password = hmac.new(
            bytes(_device_secret, encoding='utf-8'),
            bytes(_raw_password, encoding='utf-8'),
            hashlib.sha1
        ).hexdigest()
    elif _method == 'hmacmd5':
        _password = hmac.new(
            bytes(_device_secret, encoding='utf-8'),
            bytes(_raw_password, encoding='utf-8'),
            hashlib.md5
        ).hexdigest()
    elif _method == 'hmacsha256':
        _password = hmac.new(
            bytes(_device_secret, encoding='utf-8'),
            bytes(_raw_password, encoding='utf-8'),
            hashlib.sha256
        ).hexdigest()
    return _broker, _client_id, _username, _password
