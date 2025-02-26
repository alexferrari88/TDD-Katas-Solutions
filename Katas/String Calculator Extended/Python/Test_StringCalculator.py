﻿import pytest
from .StringCalculator import StringCalculator, Error
from .Logger import Logger
from .Webservice import Webservice


class TestStringCalculator:
    logger = Logger()
    web_service = Webservice()
    string_calculator = StringCalculator(logger, web_service)

    def test_should_return_0_for_empty_string(self):
        assert self.string_calculator.add("") == 0

    def test_should_return_two_numbers_sum(self):
        assert self.string_calculator.add("1,2") == 3

    def test_should_return_multiple_numbers_sum(self):
        assert self.string_calculator.add("1,2,3,4") == 10

    def test_should_return_numbers_sum_when_separated_with_new_lines(self):
        assert self.string_calculator.add("1\n2,3") == 6

    def test_should_return_numbers_sum_with_custom_delimiter(self):
        assert self.string_calculator.add("//;\n1;2") == 3

    def test_should_throw_exception_for_negative_num(self):
        with pytest.raises(Error) as excinfo:
            self.string_calculator.add("-1")
        assert "negatives not allowed: -1" == str(excinfo.value)

    def test_should_throw_exception_for_multiple_negative_num(self):
        with pytest.raises(Error) as excinfo:
            self.string_calculator.add("-1,2,3,-4,5")
        assert "negatives not allowed: -1,-4" == str(excinfo.value)

    def test_should_ignore_numbers_bigger_than_1000(self):
        assert self.string_calculator.add("1001,2") == 2

    def test_should_return_numbers_sum_with_custom_delimiter_of_any_length(self):
        assert self.string_calculator.add("//[***]\n1***2***3") == 6

    def test_should_return_number_sum_with_multiple_custom_delimiters(self):
        assert self.string_calculator.add("//[*][%]\n1*2%3") == 6

    def test_should_return_number_sum_with_multiple_custom_delimiters_longer_than_1_char(
        self,
    ):
        assert self.string_calculator.add("//[***][%%%]\n1***2%%%3") == 6

    def test_should_use_the_logger(self, mocker):
        logger = mocker.Mock()
        string_calculator_logger = StringCalculator(logger, Webservice())
        _ = string_calculator_logger.add("//[*][%]\n1*2%3")
        logger.write.assert_called()
        logger.write.assert_called_with(6)

    def test_logger_exception_should_notify_web_service(self, mocker):
        ERROR_MSG = "An error occurred"
        logger = mocker.Mock()
        logger.write.side_effect = Exception(ERROR_MSG)
        web_service = mocker.Mock()
        string_calculator = StringCalculator(logger, web_service)
        _ = string_calculator.add("//[*][%]\n1*2%3")

        web_service.notify.assert_called()
        assert ERROR_MSG in str(web_service.notify.call_args[0])

    def test_should_print_output_in_console(self, capsys):
        want = self.string_calculator.add("//[*][%]\n1*2%3")
        got = capsys.readouterr()
        assert got.out == str(want) + "\n"