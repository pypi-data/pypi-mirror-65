import logging

import NDATools

from NDATools.clientscripts.vtcmd import build_package
from tests import test_validation

from unittest import TestCase


class TestBuildPackage(TestCase):
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s:%(levelname)s:%(message)s")

    def test_build_package_success(self):
        validation_results, config = test_validation.TestValidation.test_manifest_validation_build_package_config(self)
        logging.debug(validation_results)

        uuid = validation_results[0]
        associated_files = validation_results[1]

        package_results = build_package(uuid, associated_files, config=config)
        self.assertIsNotNone(package_results[0])
        self.assertIsNotNone(package_results[1])
        logging.debug(package_results)

        return package_results, validation_results, config

    def test_s3_build_package(self):
        validation_results, config = test_validation.TestValidation.test_s3_validation(self)
        logging.debug(validation_results)

        uuid = validation_results[0]
        associated_files = validation_results[1]

        package_results = build_package(uuid, associated_files, config=config)
        self.assertIsNotNone(package_results[0])
        self.assertIsNotNone(package_results[1])
        logging.debug(package_results)

        return package_results, validation_results, config
