from sense_push.util import *
from sense_push.common import *
import sense_core as sd
import pymysql
from sense_push.core.data import PushDataHandler
import datetime

class SensePushManager(object):

    def __init__(self, queue_label=None, db_label=None, queue_configs=None, db_config=None, database=None, queue=None):

        if not db_config:
            db_config = dict()
        if database:
            db_config['database'] = database
        if not queue_configs:
            queue_config = dict()
            queue_config['queue'] = queue
            queue_configs = [
                self._build_config(queue_label, queue_config, ['host', 'port', 'user', 'pass', 'password'])]
        self.db_config = self._build_config(db_label, db_config,
                                            ['host', 'port', 'user', 'pass', 'database', 'password'])
        self.queue_configs = queue_configs

    def _build_sql(self, table, build_sql, offset, limit):
        if build_sql is not None:
            return build_sql(table, offset, limit)
        if limit <= 0:
            return "select * from {}".format(table)
        return "select * from {0} limit {1},{2}".format(table, offset, limit)

    def _build_config(self, label, config, keys):
        if not label:
            return config
        if not config:
            config = dict()
        for key in keys:
            if key in config:
                continue
            config[key] = sd.config(label, key, '')
        return config

    def push_table_all_data(self, table, build_sql=None, limit=0):
        offset = 0
        queue_configs = self.queue_configs
        db_config = self.db_config
        handler = PushDataHandler(database=db_config['database'], table=table, queue_configs=queue_configs)
        while True:
            sql = self._build_sql(table, build_sql, offset, limit)
            items = self.fetch_by_sql(db_config, sql)
            sd.log_info("size={0} for sql={1}".format(len(items), sql))
            for item in items:
                for key in item.keys():
                    value = item[key]
                    if type(value) == datetime.datetime:
                        item[key] = str(value)
                handler.insert_data(item)
            if len(items) < limit or limit <= 0:
                break
            offset += limit
        sd.log_info("done push_table_all_data for {0}".format(table))

    def fetch_by_sql(self, config, sql):
        conn = pymysql.connect(host=config['host'], user=config['user'],
                               password=config['pass'],
                               charset='utf8', database=config['database'],
                               port=int(config['port']))
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)
        items = cursor.fetchall()
        cursor.close()
        conn.close()
        return items
