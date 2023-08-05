# -*- coding: utf-8 -*-
import random

from django.core.exceptions import ValidationError

from fast_password_validation import FastCommonPasswordValidator

# random sample from the common passwords file
COMMON_PASSWORDS = ['november19',
                    '123456789w',
                    'spotty',
                    'nadia1',
                    'giraffe1',
                    'aerosmith1',
                    'danny1',
                    'notebook1',
                    'liquid',
                    'quake3',
                    'can',
                    'pink12',
                    'nelly',
                    'stalker',
                    'bloodz1',
                    '1453',
                    'uzumymw',
                    'hayabusa',
                    'july19',
                    'rooney1',
                    'tabitha1',
                    '1234567g',
                    '741258',
                    'jayson',
                    'america13',
                    'capetown',
                    'volkswagen',
                    'chennai',
                    'monkey14',
                    'primavera',
                    'lunaluna',
                    'tweety2',
                    'oooooooo',
                    'tater1',
                    'catman',
                    'password77',
                    'peters',
                    'calderon',
                    '20002000',
                    'gonzalez1',
                    'raziel',
                    'dragon8',
                    'popcorn123',
                    'froggie1',
                    'alexandru',
                    'element2',
                    'almost1',
                    'philips',
                    'my4kids',
                    'shiloh1',
                    'sharingan',
                    'chevy350',
                    'gunners',
                    'berger',
                    '29694419',
                    'king',
                    'richie1',
                    'pictures',
                    'jamaica1',
                    'giulia']

fpv = FastCommonPasswordValidator()

# test for false negatives
for p in COMMON_PASSWORDS:
    try:
        fpv.validate(p)
    except ValidationError:
        pass
    else:
        # lack of exception is test failure here
        raise ValueError('Password should have been blocked')

# test for false positives
for i in range(1, 1000):
    p = str(random.getrandbits(random.randint(10,100)))
    # an exception is test failure here
    fpv.validate(p)
