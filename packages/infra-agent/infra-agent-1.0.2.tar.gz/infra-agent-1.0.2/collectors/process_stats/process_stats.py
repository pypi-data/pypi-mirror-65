import psutil


def get_list_of_process_sort_by_memory():
    '''
    Get list of running process sorted by Memory Usage
    '''
    list_of_process_objects = []
    # Iterate over the list
    for proc in psutil.process_iter():
        try:
            # Fetch process details as dict
            pinfo = proc.as_dict(attrs=['pid', 'name', 'username', 'status'])
            # if pinfo['status'] == psutil.STATUS_RUNNING:
            pinfo['vms'] = proc.memory_info().vms / (1024 * 1024)
            individual_process = psutil.Process(pid=pinfo['pid'])
            with individual_process.oneshot():
                pinfo['memory'] = dict(individual_process.memory_info()._asdict())
                pinfo['memory_percent'] = individual_process.memory_percent()
                pinfo['cpu'] = dict(individual_process.cpu_times()._asdict())
                pinfo['cpu_percent'] = individual_process.cpu_percent()
                pinfo['cpu_num'] = individual_process.cpu_num()
                pinfo['threads'] = individual_process.num_threads()
                pinfo['fds'] = individual_process.num_fds()
                pinfo['num_ctx_switches'] = dict(individual_process.num_ctx_switches()._asdict())
                pinfo['io_counters'] = dict(individual_process.io_counters()._asdict())
            list_of_process_objects.append(pinfo)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    # Sort list of dict by key vms i.e. memory usage
    list_of_process_objects = sorted(list_of_process_objects, key=lambda procObj: procObj['vms'], reverse=True)

    return list_of_process_objects


class ProcessStats():
    @classmethod
    def retrieve(self):
        processes = get_list_of_process_sort_by_memory()[:15]
        return {'processes': processes}
