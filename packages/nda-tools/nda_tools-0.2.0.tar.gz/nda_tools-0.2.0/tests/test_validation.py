import logging

from NDATools.clientscripts.vtcmd import configure, parse_args, main, validate_files
from NDATools import *
from unittest import TestCase
try:
    import mock
except ImportError:
    from mock import patch


class TestValidation(TestCase):
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s:%(levelname)s:%(message)s")

    def test_manifest_validation_only_success(self):
        test_file = r'test_files/image03_manifest/image03_w_populated_manifest_empty_image_file.csv'
        test_directory = r'test_files/image03_manifest'
        test_manifest_directory = r'test_files/image03_manifest'
        worker_threads = 1

        testargs = ['files', test_file, '-l', test_directory, '-m', test_manifest_directory, '-wt', str(worker_threads)]

        with mock.patch.object(sys, 'argv', testargs):
            args = parse_args()
            config = configure(args)
            self.assertEqual(
                args.files[0].encode('unicode-escape').decode(),
                test_file.encode('unicode-escape').decode())
            self.assertTrue(config.manifest_path)
            self.assertFalse(args.buildPackage)
            self.assertFalse(config.skip_local_file_check)
            main()

    def test_manifest_validation_build_package_config(self):
        test_file = r'test_files/image03_manifest/image03_w_populated_manifest_empty_image_file.csv'
        test_directory = r'test_files/image03_manifest'
        test_manifest_directory = r'test_files/image03_manifest'
        test_title = 'nda-tools-validation-integration-test'
        test_description = 'nda-tools-validation-integration-test'
        test_collection_id = 1860
        worker_threads = 1

        testargs = ['files', test_file, '-l', test_directory, '-m', test_manifest_directory, '-b', '-t',
                    test_title, '-d', test_description, '-c', str(test_collection_id), '--skipLocalAssocFileCheck',
                    '-wt', str(worker_threads)]

        with mock.patch.object(sys, 'argv', testargs):
            args = parse_args()
            config = configure(args)
            w = False
            bp = False
            validation_results = validate_files(args.files, w, bp, threads=args.workerThreads, config=config)
            self.assertIsNotNone(validation_results[0])
            self.assertIsNotNone(validation_results[1])
            logging.debug(validation_results)
            return validation_results, config

    def test_s3_validation(self):
        test_file = r'test_files/MultipleDataTypes/image03_mixed_file_size_test_case_stage.csv'
        test_s3_bucket = 'NDAR_Central_1_dev'
        test_s3_prefix = 'submission_23596'
        test_title = 'nda-tools-validation-integration-test'
        test_description = 'nda-tools-validation-integration-test'
        test_collection_id = 17
        worker_threads = 1

        testargs = ['files', test_file, '-s3', test_s3_bucket, '-pre', test_s3_prefix, '-b', '-t', test_title,
                    '-d', test_description,'-c', str(test_collection_id), '-wt', str(worker_threads)]

        with mock.patch.object(sys, 'argv', testargs):
            args = parse_args()
            config = configure(args)
            w = False
            bp = False
            validation_results = validate_files(args.files, w, bp, threads=args.workerThreads, config=config)
            self.assertIsNotNone(validation_results[0])
            self.assertIsNotNone(validation_results[1])
            print(validation_results)
            logging.debug(validation_results)
            return validation_results, config
