import sense_core as sd
import logging
from sense_push.common import PUSH_ACTION_UPDATE


def init_config(module='sense_push', module_name=''):
    sd.log_init_config(module, sd.config('log_path'), monit_queue='rabbit_monit', use_module_name=module_name)
    logging.getLogger("pika").propagate = False


def build_push_message(action, database, table, data):
    if action == PUSH_ACTION_UPDATE:
        data = data.get('after')
        if not data:
            sd.log_error("build_push_message failed with table={0} data={1}".format(table, data))
            return None
    return dict(
        action=action,
        db=database,
        table=table,
        data=data,
    )
