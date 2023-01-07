from dataclasses import dataclass
from re import match


@dataclass
class CPFTools:
    cpf: str
    regex_pattern: str = r'\d{3}\.\d{3}\.\d{3}-\d{2}'

    def calculate_numbers(self):
        return [int(digit) for digit in self.cpf if digit.isdigit()]

    def sum_of_products(self, first_digit: bool = True) -> int:
        """Returns the sum of products for the specified digit."""
        digit = 9
        if not first_digit:
            digit = 10

        numbers = self.calculate_numbers()
        result = sum(
            a * b for a, b in zip(numbers[0:digit], range(digit + 1, 1, -1))
        )
        return result

    def check_regex_pattern(self, regex_pattern: str | bool = False):
        response = True
        pattern = self.regex_pattern
        if not self.regex_pattern:
            pattern = regex_pattern
        if not match(pattern, self.cpf):
            response = False
        return response

    def check_int(self):
        """Checks if the CPF has 11 integers or if they are all the same."""
        response = True
        numbers = self.calculate_numbers()
        if len(numbers) != 11 or len(set(numbers)) == 1:
            response = False
        return response

    def check_first_digit(self) -> bool:
        """Validation of the first check digit"""
        response = True
        numbers = self.calculate_numbers()
        sum_of_products = self.sum_of_products(first_digit=True)
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[9] != expected_digit:
            response = False
        return response

    def check_second_digit(self):
        """Validation of the first check digit."""
        response = True
        numbers = self.calculate_numbers()
        sum_of_products = self.sum_of_products(first_digit=False)
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[10] != expected_digit:
            response = False
        return response


class CPFValidator:
    def __init__(self, cpf: str | int):
        self.cpf = cpf

        self.tool = CPFTools(cpf=cpf)
        self._cpf_status: bool = True
        self.message: str = 'Valid CPF.'

    @property
    def cpf_status(self):
        return self._cpf_status

    @cpf_status.setter
    def cpf_status(self, value: bool):
        self._cpf_status = value

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value: bool):
        self._message = value

    # ----- VALIDATION ----- """
    def __check_str(self):
        if type(self.cpf) == str:
            self.cpf_status = self.tool.check_regex_pattern()
            self.message = 'Fail Str'

    def __check_int(self):
        """Checks if the CPF has 11 integers or if they are all the same."""
        if self.cpf_status:
            if not self.tool.check_int():
                self.cpf_status = False
                self.message = 'Int Fail'

    def __check_first_digit(self):
        """Validation of the first check digit"""
        if not self.tool.check_first_digit():
            self.cpf_status = False
            self.message = 'First Digit Fail'

    def __check_second_digit(self):
        """Validation of the first check digit."""
        if not self.tool.check_second_digit():
            self.cpf_status = False
            self.message = 'Second Digit Fail'

    def validate(self):
        if type(self.cpf) == str:
            self.__check_str()
        self.__check_int()
        self.__check_first_digit()
        self.__check_second_digit()
        return self.cpf_status, self.message
