
import os
import apminsight
import apminsight.constants as constants
from apminsight.logger import agentlogger
from apminsight.util import is_empty_string, is_non_empty_string

class Configuration:

    def __init__(self, info):
        self.license_key = os.getenv(constants.license_key_env, '')
        self.app_name = get_app_name(info)
        self.app_port = os.getenv(constants.apm_app_port, '80')
        self.collector_host = get_collector_host(self.license_key)
        self.collector_port = get_collector_port()
        self.agent_version = apminsight.version
        payload_config = os.getenv(constants.apm_print_payload, '')
        self.print_payload = False if is_empty_string(payload_config) else True
        self.installed_path = apminsight.installed_path

    def is_configured_properly(self):
        if is_empty_string(self.license_key):
            return False
       
        return True

    def update_collector_info(self, collector_info):
        if collector_info is None:
            return

        try:
            self.collector_host = collector_info.get('host', self.collector_host)
            self.collector_port = collector_info.get('port', self.collector_port)
        except Exception:
            agentlogger.exception('while updating collector info')
            

    def get_license_key(self):
        return self.license_key

    def get_app_name(self):
        return self.app_name

    def get_collector_host(self):
        return self.collector_host

    def get_collector_port(self):
        return self.collector_port

    def get_agent_version(self):
        return self.agent_version

    def get_installed_dir(self):
        return self.installed_path

    def is_payload_print_enabled(self):
        return self.print_payload
    

def get_collector_host(license_key):
    if is_empty_string(license_key):
        return ''

    host = os.getenv(constants.apm_collector_host, '')
    if is_non_empty_string(host):
        return host
    
    if license_key.startswith('eu_'):
        return constants.eu_collector_host

    if license_key.startswith('cn_'):
        return constants.cn_collector_host

    if license_key.startswith('in_'):
        return constants.ind_collector_host

    if license_key.startswith('au_'):
        return constants.aus_collector_host 

    return constants.us_collector_host


def get_app_name(info):
    if 'appname' in info and is_non_empty_string(info['appname']):
        return info['appname']
        
    return os.getenv(constants.apm_app_name, 'Python-Application')

def get_collector_port():
    port = os.getenv(constants.apm_collector_port, None)
    if port is not None:
        return port

    return constants.ssl_port

