#!/usr/bin/env python3

from setuptools import setup

if __name__ == '__main__':
    setup(
        name='parlai_internal',
        version='0.0.1',
        description='internal parlai, yo',
        url='https://github.com/fairinternal/ParlAI-Internal',
        scripts=['bin/sweep-results', 'bin/shiplot'],
    )
