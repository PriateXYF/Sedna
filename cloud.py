# coding: utf-8

from leancloud import Engine
from leancloud import LeanEngineError
from api.common import common_checkin

engine = Engine()

@engine.define
def checkin(**params):
    return common_checkin(params['id'])