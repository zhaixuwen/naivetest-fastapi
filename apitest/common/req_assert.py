# -*- coding: utf-8 -*-
import json

from requests import Response
from typing import Optional
from deepdiff import DeepDiff
from utils import logger


def handle_assert(resp: Response, expected_code: int, post_assert_json: Optional[dict]) -> dict:
    if expected_code:
        try:
            assert resp.status_code == expected_code
        except AssertionError:
            logger.error('Request assert=>校验状态码异常！')
            f = '期望状态码是{},实际状态码是{}'.format(expected_code, resp.status_code)
            return {
                'result': 'error',
                'detail': f
            }
    if post_assert_json:
        expected_json = json.loads(post_assert_json.get('expected_json'))
        ignore_paths = str(post_assert_json.get('ignore_paths')).strip().split(',')
        try:
            result = DeepDiff(expected_json, resp.json(), exclude_paths=ignore_paths, ignore_order=True)
        except Exception as e:
            logger.error(e)
            return {'result': 'error', 'detail': 'Json对比处理异常！'}
        try:
            assert result == {}
        except AssertionError:
            logger.error('Request assert=>Json校验异常！')
            return {
                'result': 'error',
                'detail': '响应Json与期望Json值不符，请检查！',
                'expected_json': expected_json,
                'factual_json': resp.json()
            }
    return {'result': 'success', 'detail': '校验通过！'}
