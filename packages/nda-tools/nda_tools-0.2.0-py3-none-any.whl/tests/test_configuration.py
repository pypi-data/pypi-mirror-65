import logging
import sys

import NDATools

from NDATools.clientscripts.vtcmd import configure, parse_args
from unittest import TestCase
try:
    import mock
except ImportError:
    from mock import patch


class TestConfiguration(TestCase):
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s:%(levelname)s:%(message)s")

    def setUp(self):
        self.test_file = r'test_files/image03_manifest/image03_w_populated_manifest_empty_image_file.csv'
        self.test_directory = r'test_files/image03_manifest'
        self.test_manifest_directory = r'test_files/image03_manifest'
        self.test_title = 'nda-tools-configuration-integration-test'
        self.test_description = 'nda-tools-configuration-integration-test'

    def test_manifest_skip_file_check(self):
        test_file = r'test_files/image03_manifest/image03_w_populated_manifest_empty_image_file_windows-path.csv'

        test_collection_id = 1860

        testargs = ['files', test_file, '-l', self.test_directory, '-m', self.test_manifest_directory, '-b', '-t',
                    self.test_title, '-d', self.test_description, '-c', str(test_collection_id),
                    '--skipLocalAssocFileCheck']

        with mock.patch.object(sys, 'argv', testargs):
            args = parse_args()
            config = configure(args)
            self._check_endpoints(config)
            self.assertEqual(
                args.files[0].encode('unicode-escape').decode(),
                test_file.encode('unicode-escape').decode())
            self.assertTrue(config.manifest_path)
            self.assertTrue(args.buildPackage)
            self.assertEqual(config.title, self.test_title)
            self.assertEqual(config.description, self.test_description)
            self.assertEqual(config.collection_id, test_collection_id)
            self.assertTrue(config.skip_local_file_check)

    def test_resume_submission_flags(self):
        test_file = r'test_files/image03_manifest/image03_w_populated_manifest_empty_image_file_windows-path.csv'
        worker_threads = 1

        testargs = ['files', test_file, '-r', '--hideProgress', '-wt', str(worker_threads)]

        with mock.patch.object(sys, 'argv', testargs):
            args = parse_args()
            config = configure(args)
            self._check_endpoints(config)
            self.assertEqual(
                args.files[0].encode('unicode-escape').decode(),
                test_file.encode('unicode-escape').decode())
            self.assertFalse(config.skip_local_file_check, config.skip_local_file_check)
            self.assertTrue(args.resume, args.resume)
            self.assertTrue(config.hideProgress, config.hideProgress)
            self.assertFalse(config.manifest_path, config.manifest_path)
            self.assertEqual(args.workerThreads, worker_threads)

    def test_csv_filelist(self):
        test_file = r'test_files/MultipleDataTypes/image03.csv'
        test_directory = r'test_files/MultipleDataTypes/image03'
        test_collection_id = 1860

        testargs = ['files', test_file, '-l', test_directory, '-b', '-t', self.test_title, '-d', self.test_description,
                    '-c', str(test_collection_id)]

        with mock.patch.object(sys, 'argv', testargs):
            args = parse_args()
            config = configure(args)
            self._check_endpoints(config)
            self.assertEqual(
                args.files[0].encode('unicode-escape').decode(),
                test_file.encode('unicode-escape').decode())
            self.assertTrue(args.buildPackage)
            self.assertEqual(config.title, self.test_title)
            self.assertEqual(config.description, self.test_description)
            self.assertEqual(config.collection_id, test_collection_id)
            self.assertFalse(config.manifest_path)

    def test_s3(self):
        test_file = r'test_files/MultipleDataTypes/image03_mixed_file_size_test_case_stage.csv'
        test_s3_bucket = 'NDAR_Central_1_dev'
        test_s3_bucket_prefix = 'submission_23596'
        test_collection_id = 17

        testargs = ['files', test_file, '-s3', test_s3_bucket, '-pre', test_s3_bucket_prefix, '-b',
                    '-c', str(test_collection_id)]

        with mock.patch.object(sys, 'argv', testargs):
            args = parse_args()
            config = configure(args)
            self._check_endpoints(config)
            self.assertEqual(
                args.files[0].encode('unicode-escape').decode(),
                test_file.encode('unicode-escape').decode())
            self.assertEqual(config.source_bucket, test_s3_bucket)
            self.assertEqual(config.source_prefix, test_s3_bucket_prefix)
            self.assertTrue(args.buildPackage)
            self.assertEqual(config.collection_id, test_collection_id)
            self.assertFalse(config.manifest_path)

    def test_s3_resume(self):
        test_submission_id = 23607
        test_s3_bucket = 'NDAR_Central_1_dev'
        test_s3_bucket_prefix = 'submission_23596'
        test_collection_id = 17

        testargs = ['files', '-r', str(test_submission_id), '-s3', test_s3_bucket, '-pre', test_s3_bucket_prefix, '-b',
                    '-c', str(test_collection_id)]

        with mock.patch.object(sys, 'argv', testargs):
            args = parse_args()
            config = configure(args)
            self._check_endpoints(config)
            self.assertTrue(args.resume, args.resume)
            self.assertTrue(args.files[0], test_submission_id)
            self.assertEqual(config.source_bucket, test_s3_bucket)
            self.assertEqual(config.source_prefix, test_s3_bucket_prefix)
            self.assertTrue(args.buildPackage)
            self.assertEqual(config.collection_id, test_collection_id)
            self.assertFalse(config.manifest_path, msg='Manifest')

    def _check_endpoints(self, config):
        logging.debug('Checking endpoint configuration...')
        self.assertTrue(config.datamanager_api is not None or config.datamanager_api != "", config.datamanager_api)
        self.assertTrue(config.validation_api is not None or config.validation_api != "", config.validation_api)
        self.assertTrue(config.submission_package_api is not None or config.submission_package_api != "", config.submission_package_api)
        self.assertTrue(config.submission_api is not None or config.submission_api != "", config.submission_api)
        self.assertTrue(config.validationtool_api is not None or config.validationtool_api != "", config.validationtool_api)
        self.assertTrue(config.validation_results is not None or config.validation_results != "", config.validation_results)
        self.assertTrue(config.submission_packages is not None or config.submission_packages != "", config.submission_packages)
