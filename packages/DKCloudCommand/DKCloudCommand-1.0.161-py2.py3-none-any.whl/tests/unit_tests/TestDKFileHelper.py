import os
import tempfile
import shutil

from datetime import datetime

from DKCommon.DKPathUtils import is_windows_os

from DKCloudCommand.modules.DKFileHelper import DKFileHelper
from ..DKCommonUnitTestSettings import DKCommonUnitTestSettings


class TestDKFileHelper(DKCommonUnitTestSettings):
    _TEMP_FILE_LOCATION = '/var/tmp'

    def setUp(self):
        self.temp_dir = None
        if is_windows_os():
            TestDKFileHelper._TEMP_FILE_LOCATION = 'c:\\temp'
        else:
            TestDKFileHelper._TEMP_FILE_LOCATION = '/var/tmp'

    def tearDown(self):
        if self.temp_dir:
            shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_get_file_date(self):
        # Create a File
        temp_dir = tempfile.mkdtemp(prefix='unit-tests', dir=TestDKFileHelper._TEMP_FILE_LOCATION)
        os.chdir(temp_dir)
        new_file = 'my-test-file.txt'

        new_file2_path = os.path.join(temp_dir, new_file)
        with open(new_file2_path, 'w') as f:
            f.write('my new file 2\n')

        # Get Date
        file_date = DKFileHelper.get_file_date(new_file2_path)

        # Check the date is today
        self.assertIsNotNone(file_date)
        self.assertTrue(datetime.today().date() == file_date)
