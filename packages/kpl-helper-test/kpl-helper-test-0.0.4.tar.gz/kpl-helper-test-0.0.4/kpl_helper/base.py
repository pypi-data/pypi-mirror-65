import requests
from requests.adapters import HTTPAdapter
import logging
import sys
import os
import json

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger("kpl-helper")

session = requests.Session()
session.mount('http://', HTTPAdapter(max_retries=3))
session.mount('https://', HTTPAdapter(max_retries=3))


class _BaseConfig:
    def __init__(self):
        self._inner = os.getenv("KPL_INNER")
        self._input_root = os.getenv("KPL_INPUT_ROOT")
        input_keys = os.getenv("KPL_INPUT_KEYS")
        self._input_keys = json.loads(input_keys) if input_keys else []
        self._output_root = os.getenv("KPL_OUTPUT_ROOT", "/")
        output_keys = os.getenv("KPL_OUTPUT_KEYS")
        self._output_keys = json.loads(output_keys) if output_keys else []
        self._parameter = os.getenv("KPL_PARAMETER")
        self._metric_api = os.getenv("KPL_METRIC_API")
        self._metric_token = os.getenv("KPL_METRIC_TOKEN")

    def get_inner(self):
        return False if self._inner is None else True

    def get_input_root(self):
        return self._input_root

    def get_input_num(self):
        return len(self._input_keys)

    def get_input_keys(self):
        return self._input_keys

    def get_output_root(self):
        return self._output_root

    def get_output_num(self):
        return len(self._output_keys)

    def get_output_keys(self):
        return self._output_keys

    def get_parameter(self):
        return self._parameter

    def get_metric_api(self):
        return self._metric_api

    def get_metric_token(self):
        return self._metric_token

    def get_cluster(self):
        pass


__base_config = None


def get_config():
    if __base_config is None:
        raise Exception("Please call ready() function before using helper package.")
    return __base_config


def ready():
    print("kpl helper is ready for using.")
    global __base_config
    __base_config = _BaseConfig()


def done():
    print("execute kpl done()")
    config = get_config()
    output_num = config.get_output_num()
    if output_num == 0:
        return
    summary_dir = os.path.join(config.get_output_root(), "summary")
    if not os.path.exists(summary_dir):
        os.makedirs(summary_dir)
    output_keys = config.get_output_keys()
    with open("{}/outputs.json".format(summary_dir), "w") as fo:
        json.dump({
            "output": [{
                "name": output_keys[i],
                "uuid": "{}".format(i)
            } for i in range(output_num)],
        }, fo)


class _MsgType:
    NewMetric = "NewMetric"
    MetricData = "MetricData"


class _ResultType:
    SCALAR_RESULT = 'scalar_result'  # 用于如Rank1，Rank5，LFW，MegaFace测试协议输出的单精度值测试结果
    CURVE_RESULT = 'curve_result'  # 用于如ROC测试协议输出的测试曲线
    PROGRESS = 'progress'


def _send_metric(body):
    if not get_config().get_inner():
        return
    if len(get_config().get_metric_api()) == 0 or len(get_config().get_metric_token()) == 0:
        raise Exception("You should run your algorithm inner SeeTaaS or AutoDL platform")
    try:
        if not isinstance(body, list):
            body = [body]
        resp = session.post('{}/uploadTaskMetrics'.format(get_config().get_metric_api()),
                            json={
                                "token": get_config().get_metric_token(),
                                "items": body
                            },
                            timeout=5)
        if resp.status_code != 200:
            logger.error("send metrics http code: {}. content: {}".format(resp.status_code, resp.content))
    except requests.RequestException as e:
        logger.error('Could not reach metric api. detail: {}'.format(e))


def _send_result(result_type, name, value):
    if not get_config().get_inner():
        return
    if len(get_config().get_metric_api()) == 0 or len(get_config().get_metric_token()) == 0:
        raise Exception("You should run your algorithm inner SeeTaaS or AutoDL platform")
    try:
        resp = session.post('{}/updateTaskAttribute'.format(get_config().get_metric_api()),
                            json={
                                "token": get_config().get_metric_token(),
                                "type": result_type,
                                "name": name,
                                "value": value
                            },
                            timeout=5)
        if resp.status_code != 200:
            logger.error("send evaluate result http code: {}. content: {}".format(resp.status_code, resp.content))
    except requests.RequestException as e:
        logger.error('Could not reach evaluate result api. detail: {}'.format(e))
