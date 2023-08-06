from __future__ import absolute_import
from __future__ import print_function
import os
import requests
import logging
from prometheus_client import CollectorRegistry, Gauge, Counter, push_to_gateway

logging.basicConfig(level=logging.DEBUG)


def get_url(pushgateway_url, myelin_installation_namespace, port):
    return f"http://{pushgateway_url}.{myelin_installation_namespace}.svc.cluster.local:{port}"


class MetricClient(object):

    def __init__(self, port=9091):
        self.port = port
        self.namespace = os.environ["NAMESPACE"]
        self.myelin_installation_namespace = os.environ["MYELIN_NAMESPACE"]
        self.task_id = os.environ["TASK_ID"]
        self.axon_name = os.environ["AXON_NAME"]
        self.pushgateway_url = os.environ["PUSHGATEWAY_URL"]
        self.registry = CollectorRegistry()
        self.url = get_url(self.pushgateway_url, self.myelin_installation_namespace, self.port)
        self.metrics = {}

    def get_metric(self, name):
        metric = "{}_{}".format(name, self.axon_name)
        return metric.replace("-", "__")

    def post_update(self, metric, value, job_name=None):
        job = job_name if job_name else self.task_id
        internal_metric = self.get_metric(metric)
        if internal_metric in self.metrics:
            g = self.metrics[internal_metric]
        else:
            g = Gauge(internal_metric, '', registry=self.registry)
            self.metrics[internal_metric] = g
        g.set(value)
        push_to_gateway(self.url, job=job, registry=self.registry, grouping_key={"pod": ""})

    def post_increment(self, metric, amount=1, job_name=None):
        job = job_name if job_name else self.task_id
        internal_metric = self.get_metric(metric)
        if internal_metric in self.metrics:
            c = self.metrics[internal_metric]
        else:
            c = Counter(internal_metric, '', registry=self.registry)
            self.metrics[internal_metric] = c
        c.inc(amount=amount)
        push_to_gateway(self.url, job=job, registry=self.registry, grouping_key={"pod": ""})

    def post_hpo_result(self, config_id, config, budget, loss, info_map):
        train_controller_url = os.environ['TRAIN_CONTROLLER_URL']
        logging.info("train_controller_url: %s" % train_controller_url)

        result_dict = ({
            'loss': loss,
            'info': info_map
        })
        result = {'result': result_dict, 'exception': None}
        res_post = {'result': result, 'budget': budget, 'config_id': self.build_config_id(config_id), 'config': config}
        print('request: %s' % res_post)
        response = requests.post("%s/submit_result" % train_controller_url, json=res_post)
        print('response: %s' % response.status_code)
        if response.status_code != 200:
            raise Exception("reporting HP failed, error: %s" % response.text)

    @staticmethod
    def build_config_id(config_id):
        return [int(x) for x in config_id.split("_")]
