import unittest
from pprint import pprint

from agent import CPUMetrics, CPUCoreMetrics, CPUModelMetrics
from agent import DiskPartitionUsage, DiskIOMetrics, DiskIndividualIOMetrics
from agent import iNodeMetrics
from agent import LoadAvgMetrics
from agent import OpenFilesLinuxMetrics
from agent import ProcessStats


class TestCPUCollector(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_get_cpu_metrics(self):
        res = CPUMetrics().retrieve()
        if (res.get('steal_time')):
            assert True


class TestDeviceInodeMetrics(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_get_inode_metrics(self):
        res = iNodeMetrics().retrieve()
        print(res)


class TestOpenFileMetrics(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_get_open_files_metrics(self):
        res = OpenFilesLinuxMetrics().retrieve()
        print(res)


class TestLoadAvgMetrics(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_get_metrics(self):
        res = LoadAvgMetrics().retrieve()
        print(res)


class TestCPUCoreMetrics(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_get_metrics(self):
        res = CPUCoreMetrics().retrieve()

        print(res)


class TestCPUModelMetrics(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_get_metrics(self):
        res = CPUModelMetrics().retrieve()

        print(res)


class TestDiskUsageMetrics(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_get_metrics(self):
        metrics = DiskPartitionUsage().retrieve()
        print(metrics)


class TestDiskIOMetrics(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_get_metrics(self):
        metrics = DiskIOMetrics().retrieve()
        print(metrics)


class TestDiskIOIndividualMetrics(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_get_individual_metrics(self):
        metrics = DiskIndividualIOMetrics.retrieve()
        print(metrics)


class TestProcessStatsMetrics(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_get_individual_metrics(self):
        metrics = ProcessStats.retrieve()
        pprint(metrics)
