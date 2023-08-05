import datetime
import json
import sys
import unittest
import requests
import psutil
import platform
import uptime

from collectors.cpu_stats.cpu import CPUModelMetrics, CPUName, CPUMetrics, CPUContextMetrics, CPUCoreMetrics
from collectors.disk_stats.disk_stats import DiskPartitionUsage, DiskIOMetrics, DiskIndividualIOMetrics
from collectors.inode_stats.inode import iNodeMetrics
from collectors.load_avg.load_avg import LoadAvgMetrics
from collectors.open_files.open_files_linux import OpenFilesLinuxMetrics
from collectors.process_stats.process_stats import ProcessStats
from collectors.utilities.hostname import get_hostname, host_ip_addr


class TestMetrics(unittest.TestCase):
    def setUp(self) -> None:
        self.token = 'e55e6e03-b27a-4acf-aa81-16dd6fe388ee'
        self.server_id = 'e9c8ac51-ec34-43cc-8371-94f2be81f9a9'

    def test_it_metrics(self):
        host = 'http://localhost:5000'
        url = host + '/metrics'
        headers = {
            'authorization': self.token,
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
            # 'threads': psutil.
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
            'agent_version': '0.0.1',
            'server_id': self.server_id,

        }
        print(post_fields)
        print(json.dumps(post_fields))

        res = requests.post(url, json=post_fields, headers=headers)
        # request = Request(url, urlencode(post_fields).encode(), headers=headers)
        # # TODO Handle errors
        # res = urlopen(request)
        # json = res.read().decode()

        # print(json)
