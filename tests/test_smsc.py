# flake8: noqa

import datetime
import logging

import os
import pytest
import requests_mock
from furl import furl

from smsc import (
    SMSC, SMSMessage, SendResponse, CostResponse, StatusResponse, BalanceResponse, ViberMessage, FlashMessage, Status,
    SendError, GetCostError, GetStatusError, GetBalanceError
)

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
log = logging.getLogger(__name__)
URL = 'https://smsc.ru/sys/'


@pytest.fixture
def client():
    return SMSC(login=os.environ['SMSC_LOGIN'], password=os.environ['SMSC_PASSWORD'],
                sender=os.environ.get('SMSC_SENDER', None))


@pytest.fixture
def params():
    return {'login': os.environ['SMSC_LOGIN'], 'psw': os.environ['SMSC_PASSWORD'],
            'sender': os.environ.get('SMSC_SENDER', None)}


def test_client():
    assert os.environ.get('SMSC_LOGIN')
    assert os.environ.get('SMSC_PASSWORD')
    client2 = SMSC(login=os.environ['SMSC_LOGIN'], password=os.environ['SMSC_PASSWORD'],
                   sender=os.environ.get('SMSC_SENDER', None))
    assert str(client2) == "<SMSC login='%s' sender='%s'>" % (
        os.environ['SMSC_LOGIN'], os.environ.get('SMSC_SENDER', None))


def test_message_sms():
    message = SMSMessage(text='test')
    assert message is not None
    assert isinstance(message, SMSMessage)
    assert str(message) == "<SMSMessage text=test format=None>"
    assert message.text == 'test'
    assert message.format is None
    enc = message.encode()
    assert isinstance(enc, dict)
    assert 'mes' in enc
    assert enc['mes'] is not None
    assert enc['mes'] == 'test'
    assert len(enc.keys()) == 1


# noinspection PyShadowingNames
def test_sms_simple(client: SMSC, params: dict):
    assert os.environ.get('PHONE')
    to = os.environ['PHONE']
    message_text = 'test'
    f = furl(URL).add(path="send.php").add(params).add({'phones': to, 'mes': message_text, 'cost': 2})
    with requests_mock.Mocker() as m:
        m.get(f.url, json={'cnt': 1, 'id': 1, 'cost': 1.44},
              headers={'Content-Type': 'application/json; charset=utf-8'})
        res = client.send(to=os.environ['PHONE'], message=SMSMessage(text='test'))
    assert res is not None
    assert isinstance(res, SendResponse)
    assert str(res) == "<SendResponse id=1 count=1 cost=1.44>"
    assert res.message_id == 1
    assert res.count == 1
    assert res.cost == 1.44


# noinspection PyShadowingNames
def test_sms_simple_fail(client: SMSC, params: dict):
    assert os.environ.get('PHONE')
    to = os.environ['PHONE']
    message_text = 'test'
    f = furl(URL).add(path="send.php").add(params).add({'phones': to, 'mes': message_text, 'cost': 2})
    with requests_mock.Mocker() as m:
        m.get(f.url, json={}, headers={'Content-Type': 'application/json; charset=utf-8'}, status_code=404)
        with pytest.raises(SendError):
            client.send(to=os.environ['PHONE'], message=SMSMessage(text='test'))


# noinspection PyShadowingNames
def test_sms_cost(client: SMSC, params: dict):
    assert os.environ.get('PHONE')
    to = os.environ['PHONE']
    message_text = 'test'
    f = furl(URL).add(path="send.php").add(params).add({'phones': to, 'mes': message_text, 'cost': 1})
    with requests_mock.Mocker() as m:
        m.get(f.url, json={'cnt': 1, 'cost': 1.44}, headers={'Content-Type': 'application/json; charset=utf-8'})
        res = client.get_cost(to=os.environ['PHONE'], message=SMSMessage(text='test'))
    assert res is not None
    assert isinstance(res, CostResponse)
    assert str(res) == "<CostResponse count=1 cost=1.44>"
    assert res.count == 1
    assert res.cost == 1.44


# noinspection PyShadowingNames
def test_sms_cost_fail(client: SMSC, params: dict):
    assert os.environ.get('PHONE')
    to = os.environ['PHONE']
    message_text = 'test'
    f = furl(URL).add(path="send.php").add(params).add({'phones': to, 'mes': message_text, 'cost': 1})
    with requests_mock.Mocker() as m:
        m.get(f.url, json={}, headers={'Content-Type': 'application/json; charset=utf-8'}, status_code=404)
        with pytest.raises(GetCostError):
            client.get_cost(to=os.environ['PHONE'], message=SMSMessage(text='test'))


# noinspection PyShadowingNames
def test_sms_status(client: SMSC, params: dict):
    assert os.environ.get('PHONE')
    to = os.environ['PHONE']
    msg_id = '1'
    f = furl(URL).add(path="status.php").add(params).add(
        {'phone': to + ',', 'id': msg_id + ',', 'charset': 'utf-8', 'all': 2, 'fmt': 3}).remove('sender')
    with requests_mock.Mocker() as m:
        m.get(f.url, json=[
            {'id': 1, 'send_timestamp': 1495823967, 'message': 'test', 'status_name': 'Доставлено', 'cost': '1.20',
             'phone': '79262138080', 'sender_id': 'avto-disp', 'last_date': '26.05.2017 21:39:32',
             'region': 'г.Москва и Московская область', 'send_date': '26.05.2017 21:39:27',
             'last_timestamp': 1495823972, 'operator': 'МегаФон', 'status': 1, 'country': 'Россия'}],
              headers={'Content-Type': 'application/json; charset=utf-8'})
        res = client.get_status(to=os.environ['PHONE'], msg_id=msg_id)
    assert res is not None
    assert isinstance(res, list)
    assert len(res) == 1
    assert str(res).startswith('[<StatusResponse ')
    assert isinstance(res[0], StatusResponse)
    assert str(res[0]) == "<StatusResponse id=1 status= <Status status=1 name=Доставлено>>"
    assert res[0].status is not None
    assert isinstance(res[0].status, Status)
    assert res[0].status.status_id == 1
    assert res[0].status.name == 'Доставлено'
    assert res[0].data is not None
    assert isinstance(res[0].data, dict)
    for name in ['id', 'message', 'cost', 'phone', 'sender_id', 'last_date', 'region', 'send_date', 'operator',
                 'country']:
        assert name in res[0].data
    for name in ['send_timestamp', 'last_timestamp', 'status', 'status_name']:
        assert name not in res[0].data
    assert isinstance(res[0].data['send_date'], datetime.datetime)


# noinspection PyShadowingNames
def test_sms_status_fail(client: SMSC, params: dict):
    assert os.environ.get('PHONE')
    to = os.environ['PHONE']
    msg_id = '1'
    f = furl(URL).add(path="status.php").add(params).add(
        {'phone': to + ',', 'id': msg_id + ',', 'charset': 'utf-8', 'all': 2, 'fmt': 3}).remove('sender')
    with requests_mock.Mocker() as m:
        m.get(f.url, json={}, headers={'Content-Type': 'application/json; charset=utf-8'}, status_code=404)
        with pytest.raises(GetStatusError):
            client.get_status(to=os.environ['PHONE'], msg_id=msg_id)


# noinspection PyShadowingNames
def test_get_balance(client: SMSC, params: dict):
    f = furl(URL).add(path="balance.php").add(params).remove('sender')
    with requests_mock.Mocker() as m:
        m.get(f.url, json={'balance': '100.01', 'currency': 'RUR'},
              headers={'Content-Type': 'application/json; charset=utf-8'})
        res = client.get_balance()
    assert res is not None
    assert isinstance(res, BalanceResponse)
    assert str(res) == "<BalanceResponse balance=100.01 credit=0.00 currency=RUR>"
    assert res.balance == 100.01
    assert res.credit == 0.0
    assert res.currency == 'RUR'


# noinspection PyShadowingNames
def test_get_balance_fail(client: SMSC, params: dict):
    f = furl(URL).add(path="balance.php").add(params).remove('sender')
    with requests_mock.Mocker() as m:
        m.get(f.url, json={}, headers={'Content-Type': 'application/json; charset=utf-8'}, status_code=404)
        with pytest.raises(GetBalanceError):
            client.get_balance()


# noinspection PyShadowingNames
def test_viber(client: SMSC, params: dict):
    assert os.environ.get('PHONE')
    to = os.environ['PHONE']
    message_text = 'test'
    f = furl(URL).add(path="send.php").add(params).add({'phones': to, 'mes': message_text, 'cost': 2, 'viber': 1})
    with requests_mock.Mocker() as m:
        m.get(f.url, json={'error': "can't to deliver", 'id': 1, 'error_code': 8},
              headers={'Content-Type': 'application/json; charset=utf-8'})
        res = client.send(to=os.environ['PHONE'], message=ViberMessage(text='test'))
    assert res is not None
    assert isinstance(res, SendResponse)
    assert res.error is not None
    assert str(res.error) == 'SMSCError(code=8, error="can\'t to deliver")'


# noinspection PyShadowingNames
def test_flash(client: SMSC, params: dict):
    assert os.environ.get('PHONE')
    to = os.environ['PHONE']
    message_text = 'test'
    f = furl(URL).add(path="send.php").add(params).add({'phones': to, 'mes': message_text, 'cost': 2, 'flash': 1})
    with requests_mock.Mocker() as m:
        m.get(f.url, json={'cnt': 1, 'id': 1, 'cost': 1.44},
              headers={'Content-Type': 'application/json; charset=utf-8'})
        res = client.send(to=os.environ['PHONE'], message=FlashMessage(text='test'))
    assert res is not None
    assert isinstance(res, SendResponse)
    assert str(res) == "<SendResponse id=1 count=1 cost=1.44>"
    assert res.message_id == 1
    assert res.count == 1
    assert res.cost == 1.44


# noinspection PyShadowingNames
def test_sms_options(client: SMSC, params: dict):
    assert os.environ.get('PHONE')
    to = os.environ['PHONE']
    message_text = 'test'
    f = furl(URL).add(path="send.php").add(params).add(
        {'phones': to, 'mes': message_text, 'cost': 2, 'translit': 1, 'tinyurl': 1, 'maxsms': 1})
    with requests_mock.Mocker() as m:
        m.get(f.url, json={'cnt': 1, 'id': 1, 'cost': 1.44},
              headers={'Content-Type': 'application/json; charset=utf-8'})
        res = client.send(to=os.environ['PHONE'], message=SMSMessage(text='test', translit=1, tinyurl=1, maxsms=1))
    assert res is not None
    assert res.error is None
    assert isinstance(res, SendResponse)
    assert str(res) == "<SendResponse id=1 count=1 cost=1.44>"
    assert res.message_id == 1
    assert res.count == 1
    assert res.cost == 1.44
