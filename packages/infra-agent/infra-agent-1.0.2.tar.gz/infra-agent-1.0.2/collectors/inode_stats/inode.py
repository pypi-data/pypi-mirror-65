"""
Author :  Azhar
Language:  Python
"""

import os
import json
import psutil


class iNodeMetrics():
    def __init__(self):
        self.metrics = {
            'device': {
                'total_inode_files': 0,
                'total_inode_free': 0,
                'total_inode_used': 0,
                'total_inode_used_percentage': 0,

            }
        }

    def retrieve(self):
        inode_files = 0
        inode_free = 0
        total_inode_files = 0
        total_inode_free = 0

        for partition in psutil.disk_partitions(True):
            if partition.fstype == 'tmpfs':
                try:
                    inode_statistics = os.statvfs(partition.mountpoint)

                    # get the inode statistics
                    inode_used_percentage = 0
                    inode_files += inode_statistics.f_files
                    inode_free += inode_statistics.f_ffree
                    inode_used = inode_files - inode_free

                    # set the total and other metrics against inode parition

                    self.metrics["{}".format(partition.mountpoint)] = {}
                    self.metrics["{}".format(partition.mountpoint)]['inode_total'] = inode_files
                    self.metrics["{}".format(partition.mountpoint)]['inode_used'] = inode_used
                    self.metrics["{}".format(partition.mountpoint)]['inode_free'] = inode_free
                    # if the total percentage is greater than 0 then check its percentage that is being used.

                    if inode_files > 0:
                        inode_used_percentage = "{:.2f}".format((inode_used * 100.0) / inode_files)
                    self.metrics["{}".format(partition.mountpoint)]['inode_used_percentage'] = inode_used_percentage

                    # update the total inode value
                    total_inode_files += inode_files
                    total_inode_free += inode_free

                except PermissionError:
                    # Added due to the Docker containers make the permission error
                    pass

        total_inode_used = total_inode_files - total_inode_free
        self.metrics['device']['total_inode_files'] = total_inode_files
        self.metrics['device']['total_inode_free'] = total_inode_free
        self.metrics['device']['total_inode_used'] = total_inode_used
        total_inode_used_percentage = 0
        if total_inode_files:
            total_inode_used_percentage = "{:.2f}".format((total_inode_used * 100.0) / inode_files)
        self.metrics['device']['total_inode_used_percentage'] = total_inode_used_percentage
        return self.metrics
