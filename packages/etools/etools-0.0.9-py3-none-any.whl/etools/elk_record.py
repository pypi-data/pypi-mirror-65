import time
import uuid
import json
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from etools.utils import get_host_ip


class ElkRecord:
    class CommonInfo:
        def __init__(self, sn, env):
            self.sn = sn
            self.env = env
            self.host = get_host_ip()

    logger = None
    common_info = None

    @classmethod
    def enabled(cls):
        return cls.logger is not None and cls.common_info is not None

    @classmethod
    def init(cls, service_name, env, log_filename):
        cls.common_info = cls.CommonInfo(service_name, env)
        logger = logging.getLogger("__elk__")
        logger.setLevel(logging.INFO)
        handler = RotatingFileHandler(
                log_filename, maxBytes=100 * 1024 * 1024, backupCount=10)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter("%(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = False
        cls.logger = logger

    def __init__(self,
                 rid=None,
                 uri=None,
                 domain=None,
                 client_ip=None,
                 user_agent=None,
                 method=None,
                 request_body=None):
        self.log_id = self.generate_uuid()
        self.rid = rid or self.generate_uuid()
        self.access_time = time.time()
        self.uri = uri
        self.domain = domain
        self.client_ip = client_ip
        self.user_agent = user_agent
        self.method = method
        self.request_body = request_body
        if not isinstance(self.request_body, str):
            self.request_body = json.dumps(self.request_body, ensure_ascii=False)
        self.cost = None
        self.status = None
        self.response_body = None

    def generate_uuid(self):
        return str(uuid.uuid1()).replace("-", "")

    def end(self, response, status_code=None):
        self.cost = (time.time() - self.access_time) * 1000
        self.access_time = datetime.strftime(
                datetime.fromtimestamp(self.access_time),
                "%Y-%m-%d %H:%M:%S.%f")
        self.response_body = response
        if not isinstance(self.response_body, str):
            self.response_body = json.dumps(self.response_body, ensure_ascii=False)
        self.status_code = status_code
        self.logger.info(json.dumps({
            "sn": self.common_info.sn,
            "env": self.common_info.env,
            "host": self.common_info.host,
            "logId": self.log_id,
            "rid": self.rid,
            "access_time": self.access_time,
            "uri": self.uri,
            "domain": self.domain,
            "clientIp": self.client_ip,
            "userAgent": self.user_agent,
            "method": self.method,
            "requestBody": self.request_body,
            "cost": self.cost,
            "status": self.status,
            "responseBody": self.response_body
        }, ensure_ascii=False))
