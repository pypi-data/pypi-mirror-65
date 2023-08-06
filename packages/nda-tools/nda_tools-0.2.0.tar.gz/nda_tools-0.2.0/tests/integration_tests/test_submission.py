import logging

from NDATools.Submission import Submission
from NDATools.clientscripts.vtcmd import configure, parse_args, submit_package, resume_submission
from NDATools import *
from tests import test_build_package

from unittest import TestCase
try:
    import mock
except ImportError:
    from mock import patch


class TestSubmission(TestCase):
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s:%(levelname)s:%(message)s")

    def test_submission_success(self):
        package_results, validation_results, config = test_build_package.TestBuildPackage.test_build_package_success(self)
        associated_files = validation_results[1]
        package_id = package_results[0]
        full_file_path = package_results[1]

        submit_package(package_id=package_id, full_file_path=full_file_path, associated_files=associated_files,
                       threads=1, batch=False, config=config)

    def test_submission_resume(self):
        package_results, validation_results, config = test_build_package.TestBuildPackage.test_build_package_success(self)
        package_id = package_results[0]
        full_file_path = package_results[1]

        # vtcmd.submit_package
        submission = Submission.Submission(id=package_id, full_file_path=full_file_path, thread_num=1, batch_size=False,
                                           allow_exit=True, config=config)
        print('Requesting submission for package: {}'.format(submission.package_id))
        submission.submit()
        if submission.submission_id:
            print('Submission ID: {}'.format(str(submission.submission_id)))

        # Send command line args but with -r
        test_directory = r'test_files/image03_manifest'

        testargs = ['-r', str(submission.submission_id), '-l', test_directory]
        with mock.patch.object(sys, 'argv', testargs):
            args = parse_args()
            config = configure(args)

            # vtcmd.resume_submission
            resume_submission(submission.submission_id, batch=False, config=config)

    def test_s3_submission(self):
        package_results, validation_results, config = test_build_package.TestBuildPackage.test_s3_build_package(self)
        associated_files = validation_results[1]
        package_id = package_results[0]
        full_file_path = package_results[1]

        submit_package(package_id=package_id, full_file_path=full_file_path, associated_files=associated_files,
                       threads=1, batch=False, config=config)
