import json
from http import HTTPStatus

from django.test import Client, TestCase


class TaskRobotTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        self.guest_client = Client()

    def test_url_avail(self):
        """Проверяем недоступность методов URL-адреса."""
        address = "/add_robot/"
        request_types = ["put", "delete", "patch"]
        with self.subTest(address=address):
            for req in request_types:
                response = getattr(self.guest_client, req)(address)
                self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST.value)

    def test_create_robot(self):
        """Проверяем запись робота в БД"""
        address = "/add_robot/"
        test_cases = [
            {
                "model": "X5",
                "version": "LT",
                "serial": "22",
                "created": "2023-01-01 00:00:01",
            },
            {"version": "LT", "serial": "22", "created": "2023-01-01 00:00:01"},
            {},
            {
                "model": "X5",
                "version": "LT",
                "created": "22",
                "serial": "2023-01-01 00:00:01",
            },
        ]

        with self.subTest(address=address):
            for inx in range(1, len(test_cases)):
                response = self.guest_client.post(
                    address,
                    data=json.dumps(test_cases[inx]),
                    content_type="application/json",
                )
                self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST.value)
        with self.subTest(address=address):
            response = self.guest_client.post(
                address, data=json.dumps(test_cases[0]), content_type="application/json"
            )
            self.assertEqual(response.status_code, HTTPStatus.CREATED.value)
