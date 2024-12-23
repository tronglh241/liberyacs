import datetime

import pytest

from .case import Case


class FileNotFoundCase(Case):
    config_file = 'tests/configs/nonexist_file.yml'
    evaluate = True

    def check(self):
        with pytest.raises(FileNotFoundError):
            self.load_config()


class RegularCase(Case):
    config_file = 'tests/configs/regular.yml'
    evaluate = True

    def check(self):
        config = self.load_config()

        assert config.num_int == 10
        assert config.num_float == 1.23
        assert config.string == 'This is a string.'

        assert config.list[:4] == [1, 1.1, 10, 1.23]
        assert config.list[4].sub_dict.num_int == 20
        assert config.list[4].sub_dict.num_float == 2.34

        assert config.datetime_object.year == 2024
        assert config.datetime_object.month == 12
        assert config.datetime_object.day == 24
        assert config.datetime_object.hour == 12
        assert config.datetime_object.minute == 12
        assert config.datetime_object.second == 12

        assert config.date_object.year == 2024
        assert config.date_object.month == 12
        assert config.date_object.day == 24

        assert config.dt_object == datetime.MINYEAR


class NotEvalCase(Case):
    config_file = 'tests/configs/not_eval.yml'
    evaluate = False

    def check(self):
        config = self.load_config()

        assert config.num_int == 10
        assert config.num_float == 1.23
        assert config.string == "'This is a string.'"

        assert config.list[:4] == [1, 1.1, 'num_int', 'num_float']
        assert config.list[4].sub_dict.num_int == 20
        assert config.list[4].sub_dict.num_float == 2.34
