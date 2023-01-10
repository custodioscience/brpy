from __future__ import annotations

from typing import Callable

import numpy as np
from dataclasses import dataclass


@dataclass(slots=True)
class CPFValidation:
    digits: str
    array: np.ndarray = None
    ufs: list = None
    is_valid: bool = None
    leading_zeroes: bool = False
    tooltip: str = None
    debug: bool = False

    def __call__(self) -> bool:

        validators: list[Callable] = [
            self._digits_cast,
            self._all_repeated,
            self._leading_condition,
            self._reshape,
            self._validate_first_digit,
            self._validate_second_digit,
        ]

        for validator in validators:
            validator()

            if self.debug:
                self._debug()

            if self.is_valid is False:
                return False

        return self._success()

    def _success(self) -> bool:
        self.tooltip = 'CPF is valid.'
        self.is_valid = True
        if self.debug:
            self._debug()

        return True

    def _debug(self):
        digits = self.digits
        array = self.array
        tooltip = self.tooltip
        log = f'| Digits: {digits} | Array: {array} | Status: {tooltip}'
        print(log)

    def _sum_of_products(self, first_digit: bool = True) -> int:
        """Returns the sum of products for the specified digit."""
        d = 9  # d is digit
        if not first_digit:
            d = 10
        return sum(a * b for a, b in zip(self.array[0:d], range(d + 1, 1, -1)))

    def _digits_cast(self) -> None:
        cpf = self.digits
        cpf_array = np.array([char for char in cpf])
        digits_array = cpf_array[np.char.isdecimal(cpf_array)]
        self.array = digits_array
        self.tooltip = 'Successfully extracted CPF digits.'

    def _all_repeated(self):
        uniques = len(np.unique(self.array))
        if uniques < 2:
            msg = f'Only {uniques} unique digit(s). Invalid CPF.'
            self.is_normalized = False
            self.tooltip = msg
        else:
            self.tooltip = 'CPF contains more than 1 unique digits.'

    def _leading_condition(self):
        size = self.array.size
        zeroes = self.leading_zeroes

        if zeroes:
            if size not in range(3, 12):
                msg = f'{size} digits in the CPF. Impossible to normalize.'
                self.is_valid = False
                self.tooltip = msg

            n_zeroes = 11 - size
            zeroes_array = np.zeros(n_zeroes).astype(np.uint8)
            array = self.array
            self.array = np.append(zeroes_array, [array])
            self.tooltip = f'{n_zeroes} leading zeros added to CPF.'

        if not zeroes:
            if size != 11:
                msg = (
                    f'{size} digits in CPF. Check the leading_zeroes '
                    f'parameter'
                )
                self.is_valid = False
                self.tooltip = msg
        else:
            self.tooltip = '11 digits confirmed in the CPF.'

    def _reshape(self):
        size = self.array.size
        if size != 11:
            msg = f'CPF: must have 11 digits, only {size} founded.'
            self.tooltip = msg
            raise ValueError()

        self.array = np.array(self.array, dtype=np.uint8)
        self.tooltip = 'CPF converted to array successfully.'

    def _validate_first_digit(self):
        """Validation of the first check digit"""
        sum_of_products = self._sum_of_products(first_digit=True)
        expected_digit = (sum_of_products * 10 % 11) % 10
        if self.array[9] != expected_digit:
            self.is_valid = False
            self.tooltip = 'Invalid first verifying digit'
        else:
            self.tooltip = 'First verifying digit of the CPF is valid.'

    def _validate_second_digit(self):
        """Validation of the first check digit."""
        sum_of_products = self._sum_of_products(first_digit=False)
        expected_digit = (sum_of_products * 10 % 11) % 10
        if self.array[10] != expected_digit:
            self.is_valid = False
            self.tooltip = 'Invalid second verifying digit.'
        else:
            self.tooltip = 'Second verifying digit of the CPF is valid.'
