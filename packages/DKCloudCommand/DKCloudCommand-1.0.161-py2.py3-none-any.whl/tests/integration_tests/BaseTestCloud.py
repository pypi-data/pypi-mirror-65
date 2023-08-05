import json
import os
import six
import tempfile
import time
import uuid

from datetime import datetime, timedelta
from os.path import expanduser

from DKCommon.DKPathUtils import is_windows_os

from .DKCloudAPIMock import DKCloudAPIMock
from DKCloudCommand.modules.DKActiveServingWatcher import DKActiveServingWatcherSingleton
from DKCloudCommand.modules.DKCloudAPI import DKCloudAPI
from DKCloudCommand.modules.DKCloudCommandConfig import DKCloudCommandConfig
from DKCloudCommand.modules.DKCloudCommandRunner import DKCloudCommandRunner
from DKCloudCommand.modules.DKFileHelper import DKFileHelper
from ..DKCommonUnitTestSettings import DKCommonUnitTestSettings

EMAIL = 'unittests@datakitchen.io'
EMAIL_SUFFIX = '+dk@datakitchen.io'
EMAIL_DOMAIN = 'datakitchen.io'

VAULT_ADDR = os.environ['VAULT_ADDR']
VAULT_ROOT_TOKEN = os.environ['VAULT_TOKEN']


class WaitLoop:

    def __init__(self, sleep=5, timeout=120):
        self.sleep = sleep
        self.then = datetime.now() + timedelta(seconds=timeout)

    def __bool__(self):
        time.sleep(self.sleep)
        return datetime.now() < self.then


class BaseTestCloud(DKCommonUnitTestSettings):

    if is_windows_os():
        _TEMPFILE_LOCATION = 'c:\\temp'
    else:
        _TEMPFILE_LOCATION = '/var/tmp'

    SLEEP_TIME = 5

    _cr_config = DKCloudCommandConfig()

    # cr_config_dict = dict()
    _branch = 'kitchens-plus'
    _api = None
    _use_mock = True
    _start_dir = None  # the tests change directories so save the starting point

    def setUp(self):
        print('{}.{} - setUp'.format(self.__class__.__name__, self._testMethodName))

        self._start_dir = os.getcwd()  # save directory

        # check context is correct
        home = expanduser('~')
        dk_context_path = os.path.join(home, '.dk', '.context')
        dk_context = DKFileHelper.read_file(dk_context_path).strip()

        self.assertEquals(
            'test', dk_context,
            '{HOME}/.dk/.context needs to be set to "test" in order to safely run the tests'
        )

        # Setup temp folder
        dk_temp_folder = os.path.join(home, '.dk')
        dk_customer_temp_folder = os.path.join(dk_temp_folder, dk_context)
        self._cr_config.set_dk_temp_folder(dk_temp_folder)
        self._cr_config.init_ignore_file(None)
        self._cr_config.set_dk_customer_temp_folder(dk_customer_temp_folder)
        self._cr_config.set_context(dk_context.strip())

        # get the connection info
        config_file_location = self._cr_config.get_config_file_location()
        self.assertTrue(self._cr_config.init_from_file(config_file_location))

        # Check configuration
        message = 'Configure %s as true at {HOME}/.dk/general-config.json' % self._cr_config.DK_CHECK_WORKING_PATH
        self.assertTrue(
            self._cr_config._config_dict[DKCloudCommandConfig.DK_CHECK_WORKING_PATH], message
        )

        message = 'Configure %s as true at {HOME}/.dk/general-config.json' % self._cr_config.DK_SKIP_RECIPE_CHECKER
        self.assertTrue(self._cr_config.get_skip_recipe_checker(), message)

        try:
            use_mock = os.path.expandvars('${USE_MOCK}').strip()
        except Exception:
            use_mock = None

        if use_mock == 'True':
            self._use_mock = True
        else:
            self._use_mock = False

        if self._use_mock is True:
            self._api = DKCloudAPIMock(self._cr_config)
        else:
            self._api = DKCloudAPI(self._cr_config)

        # connect / authenticate
        self.assertIsNotNone(self._api.login())

        # Used to ensure test kitchens are removed after testing, even if assertions fail
        self._kitchens_to_delete = []

    def tearDown(self):
        os.chdir(self._start_dir)  # restore directory
        # In case test_active_serving_watcher fails
        DKActiveServingWatcherSingleton().stop_watcher()

        # Remove test kitchens
        for kitchen in self._kitchens_to_delete:
            response = None
            try:
                response = self._delete_and_clean_kitchen(kitchen)
            except Exception:
                pass
            finally:
                if response:
                    print(response.get_message())

    # helpers ---------------------------------
    def _get_response_details(self, rc):
        return 'message: %s\npayload: %s\n' % (rc.get_message(), rc.get_payload())

    def _delete_and_clean_kitchen(self, kitchen_name):
        return DKCloudCommandRunner.delete_kitchen(self._api, kitchen_name)

    def _create_test_kitchen(self, kitchen_name, name_prefix=None):
        test_kitchen = name_prefix + "-" if name_prefix is not None else ''
        test_kitchen += "%s-%s" % (kitchen_name, str(uuid.uuid4())[:8])
        self._kitchens_to_delete.append(test_kitchen)
        rs = DKCloudCommandRunner.create_kitchen(self._api, kitchen_name, test_kitchen)
        self.assertTrue(rs.ok(), self._get_response_details(rs))
        print("created test kitchen {}".format(test_kitchen))
        return test_kitchen

    def _get_recipe_to_disk(self, kitchen_name, recipe_name):
        temp_dir, kitchen_dir = self._make_kitchen_dir(kitchen_name, change_dir=True)
        self._tmpdirs.append(temp_dir)
        recipe_dir = os.path.join(kitchen_dir, recipe_name)
        rs = DKCloudCommandRunner.get_recipe(
            self._api, kitchen_name, recipe_name, start_dir=kitchen_dir
        )
        self.assertTrue(rs.ok(), rs.get_message())
        print("checked out recipe {} to {}".format(recipe_name, recipe_dir))
        return temp_dir, recipe_dir

    def _make_kitchen_dir(self, kitchen_name, change_dir=True):
        temp_dir = tempfile.mkdtemp(prefix='unit-tests', dir=self._TEMPFILE_LOCATION)
        kitchen_dir = os.path.join(temp_dir, kitchen_name)
        os.mkdir(kitchen_dir)
        if change_dir:
            os.chdir(kitchen_dir)
        plug_dir = os.path.join(kitchen_dir, '.dk')
        os.mkdir(plug_dir)
        with open(os.path.join(plug_dir, 'KITCHEN_META'), 'w') as kitchen_file:
            kitchen_file.write(kitchen_name)
        os.mkdir(os.path.join(plug_dir, 'recipes'))
        return temp_dir, kitchen_dir

    def _make_recipe_dir(self, recipe_name, kitchen_name, change_dir=True):
        temp_dir, kitchen_dir = self._make_kitchen_dir(kitchen_name, change_dir)
        recipes_meta_dir = os.path.join(os.path.join(kitchen_dir, '.dk'), 'recipes')
        recipe_meta_dir = os.path.join(recipes_meta_dir, recipe_name)
        os.makedirs(recipe_meta_dir)
        with open(os.path.join(recipe_meta_dir, 'RECIPE_META'), 'w') as recipe_file:
            recipe_file.write(recipe_name)
        recipe_dir = os.path.join(temp_dir, kitchen_name, recipe_name)
        os.mkdir(recipe_name)
        if change_dir:
            os.chdir(recipe_dir)
        return temp_dir, kitchen_dir, recipe_dir

    def _add_new_file_in_remote(
            self, kitchen_name, recipe_name, file_name, recipe_dir=None, file_content=None
    ):
        return self._update_file_in_remote(
            kitchen_name, recipe_name, file_name, recipe_dir, file_content
        )

    def _update_file_in_remote(
            self, kitchen_name, recipe_name, file_name, recipe_dir=None, file_content=None
    ):
        if recipe_dir is None:
            temp_dir, recipe_dir = self._get_recipe_to_disk(kitchen_name, recipe_name)
        file_path = os.path.join(recipe_dir, file_name)

        # make path if not exist
        head, tail = os.path.split(file_path)
        if not os.path.isdir(head):
            os.makedirs(head)

        # add a new line to file
        with open(file_path, 'ab') as modify_file:
            if file_content is None:
                file_content = u'now is %s\n' % time.time()
            modify_file.write(file_content.encode('utf-8'))
            modify_file.flush()

        # update recipe to remote
        rs = DKCloudCommandRunner.update_all_files(
            self._api, kitchen_name, recipe_name, recipe_dir, "add new line"
        )
        self.assertTrue(rs.ok(), rs.get_message())
        return recipe_dir, file_path

    def _delete_file_in_remote(self, kitchen_name, recipe_name, file_name):
        rs = DKCloudCommandRunner.delete_file(
            self._api, kitchen_name, recipe_name, 'delete %s' % file_name, file_name
        )
        self.assertTrue(rs.ok(), rs.get_message())

    def _add_new_file_in_local(self, recipe_dir, file_name, file_content=None):
        return self.update_file_in_local(recipe_dir, file_name, file_content)

    def _update_file_in_local(self, recipe_dir, file_name, file_content=None):
        file_path = os.path.join(recipe_dir, file_name)
        with open(file_path, 'w') as f:
            if file_content is None:
                file_content = 'now it %s' % time.time()

            if six.PY3:
                f.write(file_content)
            else:
                f.write(file_content.encode('utf-8'))

        return file_path

    def _delete_file_in_local(self, recipe_dir, file_name):
        file_path = os.path.join(recipe_dir, file_name)
        os.remove(file_path)
        return file_path

    @staticmethod
    def _get_unit_test_guid():
        file_name = 'my_unitest_guid.txt'
        if os.path.isfile(file_name):
            with open('my_unitest_guid.txt', 'r') as f:
                myguid = f.read()
            f.closed
            return myguid
        else:
            newguid = str(uuid.uuid4())[:8]
            with open(file_name, 'w') as f:
                f.write(newguid)
            f.closed
            return newguid

    def _add_my_guid(self, base_branch, delete_branch_on_teardown=True):
        test_kitchen_name = base_branch + '_ut_' + self._get_unit_test_guid()
        if delete_branch_on_teardown:
            self._kitchens_to_delete.append(test_kitchen_name)
        return test_kitchen_name

    def _get_run_variation(self):
        if 'cloud.datakitchen.io' in self._cr_config.get_ip():
            variation_name = 'variation-test-production05'
            print('Running production recipe.')
        else:
            variation_name = 'variation-test'
        return variation_name

    def _get_run_variation_for_recipe(self, recipe_name, repeater=False):
        if recipe_name == 'parallel-recipe-test':
            if 'cloud.datakitchen.io' in self._cr_config.get_ip():
                if repeater is True:
                    variation_name = 'variation-test-production05-repeat'
                else:
                    variation_name = 'variation-test-production05-now'
                print('Running production recipe.')
            else:
                if repeater is True:
                    variation_name = 'variation-test-repeat'
                else:
                    variation_name = 'variation-test'
            return variation_name
        elif recipe_name == 'simple':
            if 'cloud.datakitchen.io' in self._cr_config.get_ip():
                variation_name = 'simple-variation-now'
                print('Running production recipe.')
            else:
                variation_name = 'simple-variation-now-vagrant'
            return variation_name
        elif recipe_name == 'test-everything-recipe':
            if 'cloud.datakitchen.io' in self._cr_config.get_ip():
                variation_name = 'variation-morning-prod05'
                print('Running production recipe.')
            else:
                variation_name = 'variation-morning-vagrant'
            return variation_name

    def _get_the_dict(self, t):
        self.assertIsNotNone(t)
        self.assertTrue(isinstance(t, six.string_types))
        try:
            rd = json.loads(t)
        except ValueError:
            rd = None
            self.assertTrue(False)
        return rd

    def _get_the_json_str(self, d):
        self.assertIsNotNone(d)
        self.assertTrue(isinstance(d, dict))
        try:
            rs = json.dumps(d, indent=4, separators=(', ', ': '))
        except ValueError:
            rs = None
            self.assertTrue(False)
        return rs
