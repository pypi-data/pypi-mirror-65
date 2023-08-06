from .metric_client import MetricClientKubernetes, MetricClient
import os
import myelin.hpo
__all__ = ['MetricClientKubernetes', 'MetricClient']

__MYELIN_CLIENT__ = MetricClient()


def get_loss_metric():
    return os.environ["LOSS_METRIC"]


def post_hpo_result(config_id, config, budget, loss, info_map):
    __MYELIN_CLIENT__.post_hpo_result(config_id, config, budget, loss, info_map)


def publish_result(loss_value, loss_metric):
    __MYELIN_CLIENT__.post_update(loss_metric, loss_value)
    if myelin.hpo.hpo_enabled():
        myelin.hpo.publish_result(loss_value)
