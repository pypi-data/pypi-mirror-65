#!/usr/bin/env python3
import platform
import logging
import uptime
import requests
import sys
import datetime
import psutil
import time
import threading
import configparser

from collectors import __version__
from pathlib import Path

from collectors.cpu_stats.cpu import CPUModelMetrics, CPUName, CPUMetrics, CPUContextMetrics, CPUCoreMetrics
from collectors.disk_stats.disk_stats import DiskPartitionUsage, DiskIOMetrics, DiskIndividualIOMetrics
from collectors.inode_stats.inode import iNodeMetrics
from collectors.load_avg.load_avg import LoadAvgMetrics
from collectors.open_files.open_files_linux import OpenFilesLinuxMetrics
from collectors.process_stats.process_stats import ProcessStats
from collectors.utilities.hostname import get_hostname, host_ip_addr

# logging configuration

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# config details

config_file_path = "/etc/infra-agent/infra-agent.config"

# Check if config file is present
config_file = Path(config_file_path)
if not config_file.is_file():
    print('Config file missing!')
    sys.exit(1)

config = configparser.ConfigParser()
config.read(config_file_path)

host = ''
token = ''
server_id = ''

if config.has_option('infra_agent', 'server_id'):
    server_id = config.get('infra_agent', 'server_id')
if config.has_option('infra_agent', 'token'):
    token = config.get('infra_agent', 'token')
if config.has_option('infra_agent', 'host'):
    host = config.get('infra_agent', 'host')

StartTime = time.time()

if not host:
    host = 'http://localhost:5000'

if not token:
    print('token is required in infra-agent.config, see -h for more info')
    sys.exit(1)

if not server_id:
    print('server_id is required in infra-agent.config, see -h for more info')
    sys.exit(1)

url = host + '/measurements'
headers = {'authorization': token}


def action():
    host = 'https://agent-metrics.cstuinternal.com'
    url = host + '/metrics'
    headers = {
        'authorization': token,
        'Content-Type': 'application/json'
    }
    post_fields = {
        'hostname': get_hostname(),
        'host_ip_addr': host_ip_addr(),
        'platform': sys.platform,
        'system': platform.system(),
        'release': platform.release(),
        'version': platform.version(),
        'processor': platform.processor(),
        'machine': platform.machine(),
        'model': CPUModelMetrics().retrieve(),
        'distro': CPUName.retrieve(),
        'uptime': uptime.uptime(),
        'time': datetime.datetime.utcnow().replace(microsecond=0).isoformat() + 'Z',
        'load': psutil.cpu_percent(interval=1, percpu=False),
        'cores': psutil.cpu_count(),
        'memory': psutil.virtual_memory()._asdict(),
        'swap_memory': psutil.swap_memory()._asdict(),
        'disk': psutil.disk_usage('/')._asdict(),
        'cpu_metrics': CPUMetrics().retrieve(),
        'cpu_context_stats': CPUContextMetrics.retrieve(),
        'individual_cpu_metrics': CPUCoreMetrics().retrieve(),
        'disk_partition_metrics': DiskPartitionUsage().retrieve(),
        'disk_io_metrics': DiskIOMetrics.retrieve(),
        'individual_disk_io_metrics': DiskIndividualIOMetrics.retrieve(),
        'inode_metrics': iNodeMetrics().retrieve(),
        'open_file_metrics': OpenFilesLinuxMetrics().retrieve(),
        'load_metrics': LoadAvgMetrics().retrieve(),
        'process_stats': ProcessStats.retrieve(),
        'agent_version': __version__,
        'server_id': server_id
    }
    res = requests.post(url, json=post_fields, headers=headers)
    if res.status_code in [200, 301]:
        log.info('metrics sent to server!')
    log.info('update ! -> time : {:.1f}s'.format(time.time() - StartTime))


class setInterval:
    def __init__(self, interval, action):
        self.interval = interval
        self.action = action
        self.stopEvent = threading.Event()
        thread = threading.Thread(target=self.__setInterval)
        thread.start()

    def __setInterval(self):
        nextTime = time.time() + self.interval
        while not self.stopEvent.wait(nextTime - time.time()):
            nextTime += self.interval
            self.action()

    def cancel(self):
        self.stopEvent.set()


def main():
    # send the first action
    action()
    # run the worker to execute after interval
    inter = setInterval(60.0, action)
    log.info('just after setInterval -> time : {:.1f}s'.format(time.time() - StartTime))


if __name__ == '__main__':
    main()
