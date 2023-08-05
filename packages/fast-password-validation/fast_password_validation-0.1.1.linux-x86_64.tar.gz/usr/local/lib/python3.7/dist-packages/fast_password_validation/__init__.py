# -*- coding: utf-8 -*-

from typing import Tuple

VERSION: Tuple[int, int, int] = (0, 1, 1)

__title__ = 'fast_password_validation'
__version_info__ = VERSION
__version__ = '.'.join([str(a) for a in VERSION])
__author__ = 'Paweł Krawczyk'
__license__ = 'GPLv3'
__copyright__ = 'Copyright 2012-2020 Paweł Krawczyk'

from pathlib import Path

from django.core.exceptions import ValidationError
from importlib.resources import read_binary
from django.utils.translation import gettext as _


class FastCommonPasswordValidator:
    """
    Validate whether the password is a listed common password. If called without parameters, will use built-in
    list of 20000 common  passwords (lowercase and deduplicated) by
    [Royce Williams](https://gist.github.com/roycewilliams/281ce539915a947a23db17137d91aeb7).
    If called with a file name, it will load passwords one-per-line and use for subsequent checks. Internally, the list
    is stored in a Bloom filter with 4x lookup speed gain and 30% memory savings over the Django built-in
    ` django.contrib.auth.password_validation.CommonPasswordValidator`.
    """

    # noinspection PickleLoad
    def __init__(self, password_list_path: str = None, error_rate:float = 0.001):
        from bloom_filter import BloomFilter
        import pickle

        self.bloom: BloomFilter
        if password_list_path is None:
            # just load the built-in 20k list
            self.bloom = pickle.loads(read_binary('fast_password_validation', 'common-passwords.dat'))
        else:
            self.bloom = BloomFilter(max_elements=self._count_lines(password_list_path), error_rate=error_rate)
            self._load_passwords(password_list_path)

    @staticmethod
    def _count_lines(filename: str) -> int:
        """
        Count lines in the password file to provide correct size estimate to Bloom filter
        """
        with Path(filename).open() as f:
            return sum(1 for line in f.readlines()) + 100

    def _load_passwords(self, filename: str) -> None:
        with Path(filename).open() as f:
            line:str
            for line in f.readlines():
                line = line.strip()
                if len(line) > 0:
                    self.bloom.add(line)

    def validate(self, password: str, user=None) -> None:
        # if password.lower().strip() in self.bloom:
        if password.strip() in self.bloom:
            raise ValidationError(
                _("This password is too common."), code='password_too_common',
            )

    @staticmethod
    def get_help_text() -> str:
        return _('Your password can’t be a commonly used password.')