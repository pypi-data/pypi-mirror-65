import psutil


class DiskPartitionUsage():
    def __init__(self):
        self.metrics = []

    def retrieve(self):
        for partition in psutil.disk_partitions():
            usage = (psutil.disk_usage(partition.mountpoint))
            metric = {
                "device": partition.device,
                "mountpoint": partition.mountpoint,
                "fstype": partition.fstype,
                "opts": partition.opts,
                "total": usage.total,
                "free": usage.free,
                "used": usage.used,
                "used_percent": usage.percent
            }
            self.metrics.append(metric)

        return {'disk': self.metrics}


class DiskIOMetrics():
    @classmethod
    def retrieve(self):
        disk_metrics = psutil.disk_io_counters()
        return {
            'read_count': disk_metrics.read_count,
            'write_count': disk_metrics.write_count,
            'read_bytes': disk_metrics.read_bytes,
            'write_bytes': disk_metrics.write_bytes,
            'read_time': disk_metrics.read_time,
            'write_time': disk_metrics.write_time,
        }


class DiskIndividualIOMetrics():
    @classmethod
    def retrieve(self):
        disk_metrics = psutil.disk_io_counters(perdisk=True)
        metrics = {}
        for key, value in disk_metrics.items():
            metrics[key] = {
                'read_count': value.read_count,
                'write_count': value.write_count,
                'read_bytes': value.read_count,
                'write_bytes': value.read_count,
                'read_time': value.read_time,
                'write_time': value.write_time,
                'read_merged_count': value.read_merged_count,
                'write_merged_count': value.write_merged_count,
                'busy_time': value.busy_time,

            }
        return metrics
