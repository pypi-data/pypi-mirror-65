import unittest
import os
import sys
from pathlib import Path
import logging
import filecmp
from sdap_ingest_manager.collections_ingester import collection_ingestion
from sdap_ingest_manager.collections_ingester import util


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestUnitMgr(unittest.TestCase):

    def setUp(self):
        logger.info("\n===== UNIT TESTS =====")
        super().setUp()
        self.collection_config_template = util.full_path("resources/dataset_config_template.yml")

        self.target_granule_list_file = util.full_path("tmp/granule_list/target_granule_list_file.lst")
        self.target_dataset_config_file = util.full_path("tmp/dataset_config/dataset_config_file.yml")

        self.history_file = os.path.join(Path(__file__).parent.absolute(),
                                         "../data/avhrr-oi-analysed-sst.csv")
        self.history_file_not_existing = os.path.join(Path(__file__).parent.absolute(),
                                         "../data/avhrr-oi-analysed-sst.csv.not_existing")
        self.granule_file_pattern = os.path.join(Path(__file__).parent.absolute(),
                                                 "../data/avhrr_oi/*.nc")
        self.expected_dataset_configuration_file = os.path.join(Path(__file__).parent.absolute(),
                                                                "../data/dataset_config_file_ok.yml")

    def test_create_granule_list(self):
        logger.info("test create_granule_list")
        collection_ingestion.create_granule_list(self.granule_file_pattern,
                                                 self.history_file,
                                                 self.target_granule_list_file
                                                 )
        line_number = 0
        with open(self.target_granule_list_file, 'r') as f:
            for _ in f:
                line_number += 1

        self.assertEqual(1, line_number)

        os.remove(self.target_granule_list_file)

    def test_create_granule_list_no_history(self):
        logger.info("test create_granule_list")
        collection_ingestion.create_granule_list(self.granule_file_pattern,
                                                 self.history_file_not_existing,
                                                 self.target_granule_list_file
                                                 )
        line_number = 0
        with open(self.target_granule_list_file, 'r') as f:
            for _ in f:
                line_number += 1

        self.assertEqual(2, line_number)

        os.remove(self.target_granule_list_file)


    def test_create_dataset_config(self):
        logger.info("test create_dataset_config")
        collection_ingestion.create_dataset_config("avhrr-oi-analysed-sst",
                                                  "analysed_sst",
                                                   self.collection_config_template,
                                                   self.target_dataset_config_file)

        self.assertTrue(filecmp.cmp(self.expected_dataset_configuration_file, self.target_dataset_config_file),
                        "the dataset configuration file created does not match the expected results")

        os.remove(self.target_dataset_config_file)

    def tearDown(self):
        logger.info("tear down test results")


if __name__ == '__main__':
    unittest.main()
