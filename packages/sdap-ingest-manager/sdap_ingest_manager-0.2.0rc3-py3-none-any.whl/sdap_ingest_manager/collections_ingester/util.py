import configparser
import os
import sys
import logging
import hashlib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BLOCK_SIZE = 65536





def full_path(relative_path):
    sdap_ingest_manager_home = os.path.join(sys.prefix, '.sdap_ingest_manager')
    return os.path.join(sdap_ingest_manager_home,
                        relative_path)


def md5sum_from_filepath(file_path):
    hasher = hashlib.md5()
    with open(file_path.strip(), 'rb') as afile:
        buf = afile.read(BLOCK_SIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCK_SIZE)
    return hasher.hexdigest()


def read_local_configuration():
    print("====config====")
    config = configparser.ConfigParser()
    candidates = [full_path('sdap_ingest_manager.ini.default'),
                  full_path('sdap_ingest_manager.ini')]
    found_files = config.read(candidates)
    logger.info(f"successfully read configuration from {found_files}")
    return config