import unittest
from unittest import mock

import requests


class Response:

    def __init__(self, url, json=None, text=None):
        if not (json or text):
            raise ValueError()

        self.__url = url

        if text:
            self.__text = text
            self.__json = json.loads(text)
        else:
            self.__text = json.dumps(json)
            self.__json = json

    @property
    def url(self):
        return self.__url

    @property
    def text(self):
        return self.__text

    def json(self, **kwargs):
        return self.__json


class MockedRequests:

    @staticmethod
    def get(url, text=None, json=None):
        return Response(url=url, text=text, json=json)


class MyGreatClassTestCase(unittest.TestCase):
    # We patch 'requests.get' with our own method. The mock object is passed in to our test case method.
    mocker = MockedRequests.get()

    @mock.patch('requests.get', side_effect=mocker.get)
    def test_fetch(self, mock_get):
        print(requests.get("uwu.com"))
        self.assertEqual(requests.get("uwu.com"), {"uwu": True})
        # Assert requests.get calls
        # mgc = MyGreatClass()
        # json_data = mgc.fetch_json('http://someurl.com/test.json')
        # self.assertEqual(json_data, {"key1": "value1"})
        # json_data = mgc.fetch_json('http://someotherurl.com/anothertest.json')
        # self.assertEqual(json_data, {"key2": "value2"})
        # json_data = mgc.fetch_json('http://nonexistenturl.com/cantfindme.json')
        # self.assertIsNone(json_data)
        #
        # # We can even assert that our mocked method was called with the right parameters
        # self.assertIn(mock.call('http://someurl.com/test.json'), mock_get.call_args_list)
        # self.assertIn(mock.call('http://someotherurl.com/anothertest.json'), mock_get.call_args_list)
        #
        # self.assertEqual(len(mock_get.call_args_list), 3)


if __name__ == '__main__':
    unittest.main()
