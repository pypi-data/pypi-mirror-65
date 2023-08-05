"""
Author :  Azhar
Language:  Python
"""
import os
import subprocess
import logging
import psutil
from pip._vendor import distro

from collectors.utilities.process_output import get_subprocess_output

log = logging.getLogger(__name__)


class CPUMetrics():
    def __init__(self):
        self.metrics_list = {
            'user_percentage': '%',
            'system_percentage': '%',
            'nicetime_percentage': '%',
            'idle_percentage': '%',
            'iowait_percentage': '%',
            'hardwareirq_percentage': '%',
            'software_irq': '%',
            'steal_time': '%',

        }

    def retrieve(self):
        # run the command to get the CPU metrics
        cmd = 'top -b -d1 -n1 | grep -i "Cpu(s)"'
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()

        # Wait for the process to terminate, get the return code

        p_status = p.wait()

        # if the response is of bytes, convert to the string.

        if (isinstance(output, bytes)):
            output = output.decode('utf-8')
        info = output.split(',')

        for index, _ in enumerate(info):
            if index == 0:
                cpu_val = _.strip().split(':')[1].strip()
                if '%' in cpu_val:
                    info[index] = cpu_val.split('%')[0]
                else:
                    info[index] = _.strip().split(':')[1].strip().split()[0]
            else:
                cpu_val = _.strip()
                if '%' in cpu_val:
                    info[index] = _.strip().split('%')[0]
                else:
                    info[index] = _.strip().split()[0]

        self.metrics_list['user_percentage'] = info[0]
        self.metrics_list['system_percentage'] = info[1]
        self.metrics_list['nicetime_percentage'] = info[2]
        self.metrics_list['idle_percentage'] = info[3]
        self.metrics_list['iowait_percentage'] = info[4]
        self.metrics_list['hardwareirq_percentage'] = info[5]
        self.metrics_list['software_irq'] = info[6]
        self.metrics_list['steal_time'] = info[7]

        return self.metrics_list


class CPUCoreMetrics():
    def __init__(self):
        self.metrics = {}
        self.CPU_PROC_PATH = '/proc/stat'

    def retrieve(self):
        cpu_time = psutil.cpu_times(True)
        cpu_count = len(cpu_time)
        total_time = psutil.cpu_times()
        for i in range(0, len(cpu_time)):
            metric_name = 'cpu' + str(i)
            self.metrics[metric_name] = {}
            self.metrics[metric_name]["user"] = cpu_time[i].user
            self.metrics[metric_name]["system"] = cpu_time[i].system
            self.metrics[metric_name]["idle"] = cpu_time[i].idle
            self.metrics[metric_name]["nice"] = cpu_time[i].nice
            self.metrics[metric_name]["iowait"] = cpu_time[i].iowait
            self.metrics[metric_name]["irq"] = cpu_time[i].irq
            self.metrics[metric_name]["softirq"] = cpu_time[i].softirq
            self.metrics[metric_name]["steal"] = cpu_time[i].steal
            self.metrics[metric_name]["guest"] = cpu_time[i].guest
            self.metrics[metric_name]["guest_nice"] = cpu_time[i].guest_nice

        return self.metrics


class CPUModelMetrics():
    def __init__(self):
        self.PROC_PATH = '/proc'

    def retrieve(self):
        proc_cpuinfo = os.path.join(self.PROC_PATH, 'cpuinfo')
        output, _, _ = get_subprocess_output(['grep', 'model name', proc_cpuinfo], log)
        model_name_split_lines = (output.splitlines())
        model_name = model_name_split_lines[0]
        return model_name.decode('utf-8').split(":")[1].strip()


class CPUName():
    @classmethod
    def retrieve(self):
        name, version, codename = distro.linux_distribution(full_distribution_name=True)
        return "{} {} {}".format(name, version, codename)


class CPUContextMetrics():
    @classmethod
    def retrieve(cls):
        cpu_stats = psutil.cpu_stats()
        return {
            'ctx_switches': cpu_stats.ctx_switches,
            'interrupts': cpu_stats.interrupts,
            'soft_interrupts': cpu_stats.soft_interrupts,
            'syscalls': cpu_stats.syscalls,
        }
