
from apminsight import constants
from .wrapper import default_wrapper
from apminsight.util import is_non_empty_string
from apminsight.agentfactory import get_agent

class CursorProxy():

    def __init__(self, cursor, conn):
        self.cursor = cursor
        self.conn = conn
        self.check_and_wrap('execute')  
        self.check_and_wrap('executemany')  
        
    def __getattr__(self, key):
        return getattr(self.cursor, key)

    def check_and_wrap(self, attr):
        if hasattr(self.cursor, attr):
            actual = getattr(self.cursor, attr)
            attr_info = {
                constants.method_str : attr,
                constants.component_str : self.conn.comp,
                constants.extract_info : self.extract_query,
                constants.is_db_tracker : True
            }
            wrapper = default_wrapper(actual, 'Cursor', attr_info)
            setattr(self, attr, wrapper)

    def extract_query(self, tracker, args=(), kwargs={}, return_value=None):
        tracker.set_info(self.conn.host_info)
        threshold = get_agent().get_threshold()
        if threshold.is_sql_capture_enabled() is not True:
            return

        if isinstance(args, (list, tuple)) and len(args)>0:
            if is_non_empty_string(args[0]):
                tracker.set_info({'query' : args[0]})


class ConnectionProxy():

    def __init__(self, conn, comp, host_info):
        self.conn = conn
        self.comp = comp
        self.host_info = host_info

    def cursor(self, *args, **kwargs):
        real_cursor = self.conn.cursor(*args, **kwargs)
        return CursorProxy(real_cursor, self)

    def __getattr__(self, key):
        return getattr(self.conn, key)

    @staticmethod
    def get_host_info(method_info, conn_kwargs):
        host_info = {}
        if constants.host in conn_kwargs:
            host_info[constants.host] = conn_kwargs[constants.host]
        elif constants.default_host in method_info:
            host_info[constants.host] = conn_kwargs[constants.host]

        if constants.port in conn_kwargs:
            host_info[constants.port] = str(conn_kwargs[constants.port])
        elif constants.default_port in method_info:
            host_info[constants.port] = method_info[constants.default_port]

        return host_info

    @staticmethod
    def instrument_conn(original, module, method_info):
        def conn_wrapper(*args, **kwargs):
            conn = original(*args, **kwargs)
            if conn is not None:
                comp = method_info.get(constants.component_str, '')
                host_info = ConnectionProxy.get_host_info(method_info, kwargs)
                conn = ConnectionProxy(conn, comp, host_info)
                
            return conn

        return conn_wrapper

