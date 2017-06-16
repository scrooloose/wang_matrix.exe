from unittest import TestCase

from wangmatrix.partition import main as partition_main


class TestPartition(TestCase):
    def test_main(self):
        partition_main()
