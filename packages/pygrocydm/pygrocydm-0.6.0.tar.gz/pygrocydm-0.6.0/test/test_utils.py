from datetime import datetime
from unittest import TestCase

import pygrocydm.utils as utils


class TestUtils(TestCase):
    @staticmethod
    def test_parse_date_valid():
        date_str = "2019-05-04T11:31:04.563Z"
        date_obj = utils.parse_date(date_str)

        assert isinstance(date_obj, datetime)

    @staticmethod
    def test_parse_date_no_data():
        date_str = None
        date_obj = utils.parse_date(date_str)

        assert date_obj is None

    @staticmethod
    def test_parse_int_valid():
        int_str = "2"
        int_number = utils.parse_int(int_str)

        assert isinstance(int_number, int)

    @staticmethod
    def test_parse_int_no_data():
        int_str = None
        int_number = utils.parse_int(int_str)

        assert int_number is None

    @staticmethod
    def test_parse_int_error():
        int_str = "string"
        int_number = utils.parse_int(int_str)

        assert int_number is None

    @staticmethod
    def test_parse_float_valid():
        float_str = "2.01"
        float_number = utils.parse_float(float_str)

        assert isinstance(float_number, float)

    @staticmethod
    def test_parse_float_no_data():
        float_str = None
        float_number = utils.parse_float(float_str)

        assert float_number is None

    @staticmethod
    def test_parse_float_error():
        float_str = "string"
        float_number = utils.parse_float(float_str)

        assert float_number is None

    @staticmethod
    def test_parse_bool_true_valid():
        bool_str = "1"
        bool_value = utils.parse_bool(bool_str)

        assert isinstance(bool_value, bool)

    @staticmethod
    def test_parse_bool_false_valid():
        bool_str = "0"
        bool_value = utils.parse_bool(bool_str)

        assert isinstance(bool_value, bool)

    @staticmethod
    def test_parse_bool_no_data():
        bool_str = None
        bool_value = utils.parse_bool(bool_str)

        assert bool_value is None

    @staticmethod
    def test_parse_bool_error():
        bool_str = "string"
        bool_value = utils.parse_bool(bool_str)

        assert bool_value is None
