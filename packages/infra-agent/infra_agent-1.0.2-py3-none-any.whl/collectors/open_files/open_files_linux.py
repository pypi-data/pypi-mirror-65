class OpenFilesLinuxMetrics():
    def __init__(self):
        self.metrics = {
            "status": True
        }
        self.PROC_FILE_PATH = "/proc/sys/fs/file-nr"

    def retrieve(self):
        try:
            open_nr, free_nr, max = open(self.PROC_FILE_PATH).readline().split("\t")
            open_files = int(open_nr) - int(free_nr)
            self.metrics["open_files"] = open_files
            self.metrics["total_files"] = int(max)

        except Exception as e:
            self.metrics['status'] = False
            self.metrics['exception'] = str(e)
        return self.metrics
