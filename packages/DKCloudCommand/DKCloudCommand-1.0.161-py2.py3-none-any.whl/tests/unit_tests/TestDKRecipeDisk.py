import os
import pickle
import shutil
import six
import tempfile

from DKCommon.DKPathUtils import normalize, normalize_recipe_dict, WIN

from DKCloudCommand.modules.DKFileHelper import DKFileHelper
from DKCloudCommand.modules.DKKitchenDisk import DKKitchenDisk, DK_DIR
from DKCloudCommand.modules.DKRecipeDisk import (
    DKRecipeDisk,
    ORIG_HEAD,
    get_directory_sha,
    compare_sha,
)
from ..DKCommonUnitTestSettings import DKCommonUnitTestSettings
"""
WHERE DOES THE TEST DATA COME FROM?
recipe.p comes from TestCloudAPI.py::test_get_recipe
with the two pickle lines un-commented.
./Recipes/dk/templates/simple is a copy of the recipe files
that recipe.p was generated from
"""


class TestDKRecipeDisk(DKCommonUnitTestSettings):

    @classmethod
    def setUpClass(cls):
        cls.test_path = os.path.dirname(os.path.abspath(__file__))
        cls.pickle_recipe_path = os.path.join(cls.test_path, 'pickles', 'recipe.p')
        cls.files_path = os.path.join(cls.test_path, 'files')

    def setUp(self):
        self.temp_dir = None

    def tearDown(self):
        if self.temp_dir:
            shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_save_new_recipe_to_disk(self):

        r = pickle.load(open(self.pickle_recipe_path, "rb"))
        temp_dir = tempfile.mkdtemp(prefix='unit-tests', dir=TestDKRecipeDisk._TEMPFILE_LOCATION)
        kitchen_name = 'test_kitchen'
        DKKitchenDisk.write_kitchen(kitchen_name, temp_dir)
        kitchen_dir = os.path.join(temp_dir, kitchen_name)

        d = DKRecipeDisk(
            self.get_mock_ignore(), r['ORIG_HEAD'], r['recipes']['simple'], kitchen_dir
        )
        rc = d.save_recipe_to_disk()
        self.assertTrue(rc is not None)
        # FIXME Refactor this comparison without pickle
        # self.assertTrue(
        #     is_same(os.path.join(kitchen_dir, 'simple'),
        #             os.path.join(os.getcwd(), 'Recipes/dk/templates/simple')),
        #     'Pickled recipe differs from copy of recipe in Recipes')
        self.assertTrue(
            os.path.isfile(os.path.join(kitchen_dir, DK_DIR, 'recipes', 'simple', 'RECIPE_META'))
        )

        # check recipe sha is written to ORIG_HEAD
        orig_head_path = os.path.join(kitchen_dir, DK_DIR, 'recipes', 'simple', 'ORIG_HEAD')
        self.assertTrue(os.path.isfile(orig_head_path))
        self.assertEqual(r['ORIG_HEAD'], DKFileHelper.read_file(orig_head_path))

        shutil.rmtree(temp_dir, ignore_errors=True)

    def test_save_existing_recipe_to_disk(self):
        recipe_disk = self._setup_recipe_on_disk()

        new_sha = "new sha for recipe"
        recipe_disk._recipe_sha = new_sha
        recipe_disk.save_recipe_to_disk(update_meta=False)

        # check new sha is written to ORIG_HEAD
        self.assertEqual(
            new_sha, DKFileHelper.read_file(os.path.join(recipe_disk._recipe_meta_dir, ORIG_HEAD))
        )

    def test_write_recipe_state(self):
        recipe_disk = self._setup_recipe_on_disk()
        recipe_dir = os.path.join(recipe_disk._recipe_path, recipe_disk._recipe_name)

        # set remote shas to override with
        remote_shas = dict()
        simple_desc_sha = u'11111'
        remote_shas[u'simple'] = [{u'filename': u'description.json', u'sha': simple_desc_sha}]
        simple_node1_desc_sha = u'22222'
        remote_shas[normalize(u'simple/node1', WIN)] = [{
            u'filename': u'description.json',
            u'sha': simple_node1_desc_sha
        }]
        recipe_disk.write_recipe_state(recipe_dir, remote_shas)

        # check saved shas have remote shas incorporated
        kitchen_meta_dir = DKKitchenDisk.find_kitchen_meta_dir(recipe_dir)
        recipes_meta_dir = DKKitchenDisk.get_recipes_meta_dir(kitchen_meta_dir)
        recipe_name = 'simple'
        recipe_meta_dir = os.path.join(recipes_meta_dir, recipe_name)
        saved_shas = DKRecipeDisk.load_saved_shas(recipe_meta_dir)
        self.assertEqual(simple_desc_sha, saved_shas[normalize('simple/description.json', WIN)])
        self.assertEqual(
            simple_node1_desc_sha, saved_shas[normalize('simple/node1/description.json', WIN)]
        )

    def test_find_recipe(self):
        kitchen_name = 'bongo'
        temp_dir, kitchen_dir, kitchen_subdir, bad_dir = self._make_kitchen_testing_dir(
            kitchen_name
        )

        rv = DKRecipeDisk._find_recipe('snoozle')
        self.assertIsNone(rv)

        rv = DKRecipeDisk._find_recipe(kitchen_dir)
        self.assertIsNone(rv)

        rv = DKRecipeDisk._find_recipe(os.path.join(kitchen_dir, '.dk'))
        self.assertIsNone(rv)

        rv = DKRecipeDisk._find_recipe(temp_dir)
        self.assertIsNone(rv)

        recipe_root_path = os.path.join(kitchen_dir, 'recipe1')
        rv = DKRecipeDisk._find_recipe(recipe_root_path)
        self.assertEqual(rv, 'recipe1')

        node_path = os.path.join(recipe_root_path, 'node1')
        rv = DKRecipeDisk._find_recipe(node_path)
        self.assertEqual(rv, 'recipe1')

        datasources_path = os.path.join(node_path, 'data_sources')
        rv = DKRecipeDisk._find_recipe(datasources_path)
        self.assertEqual(rv, 'recipe1')

        rv = DKRecipeDisk._find_recipe(bad_dir)
        self.assertIsNone(rv)

        rv = DKRecipeDisk.is_recipe_root_dir(bad_dir)
        self.assertFalse(rv)

        rv = DKRecipeDisk.is_recipe_root_dir(node_path)
        self.assertFalse(rv)

        rv = DKRecipeDisk.is_recipe_root_dir(recipe_root_path)
        self.assertTrue(rv)

        rv = DKRecipeDisk.find_recipe_root_dir(bad_dir)
        self.assertIsNone(rv)
        rv = DKRecipeDisk.find_recipe_root_dir(node_path)
        self.assertEqual(rv, recipe_root_path)
        rv = DKRecipeDisk.find_recipe_root_dir(recipe_root_path)
        self.assertEqual(rv, recipe_root_path)

        recipe_meta_file_path = os.path.join(
            kitchen_dir, '.dk', 'recipes', 'recipe1', 'RECIPE_META'
        )
        os.remove(recipe_meta_file_path)
        rv = DKRecipeDisk._find_recipe(os.path.join(kitchen_dir, 'recipe1'))
        self.assertIsNone(rv)

        shutil.rmtree(temp_dir)

    def test_file_delete(self):
        recipe_info = pickle.load(open(os.path.join(self.files_path, "sample_recipe_001.p"), "rb"))
        kitchen_name = 'test_kitchen'
        temp_dir = tempfile.mkdtemp(prefix='unit-tests', dir=TestDKRecipeDisk._TEMPFILE_LOCATION)
        DKKitchenDisk.write_kitchen(kitchen_name, temp_dir)
        kitchen_dir = os.path.join(temp_dir, kitchen_name)

        recipe_name = 'simple'
        recipe = recipe_info['recipes'][recipe_name]
        d = DKRecipeDisk(self.get_mock_ignore(), recipe_info['ORIG_HEAD'], recipe, kitchen_dir)
        rc = d.save_recipe_to_disk()
        self.assertTrue(rc is not None)

        # Check simple/resources/very_cool.sql is present
        file_sha_contents_before = self._get_file_sha(recipe_name, kitchen_dir)

        file_kitchen_path = normalize('simple/resources/very_cool.sql', WIN)
        splitted_file_sha_contents_before = file_sha_contents_before.split('\n')
        self.assertTrue(len(splitted_file_sha_contents_before) == 22)
        self.assertTrue('%s:' % file_kitchen_path in file_sha_contents_before)

        recipe_dir = os.path.join(kitchen_dir, recipe_name)
        file_recipe_path = normalize('resources/very_cool.sql', WIN)
        DKRecipeDisk.write_recipe_state_file_delete(recipe_dir, file_recipe_path)

        # Check simple/resources/very_cool.sql is not present any more
        file_sha_contents_after = self._get_file_sha(recipe_name, kitchen_dir)

        splitted_file_sha_contents_after = file_sha_contents_after.split('\n')
        self.assertTrue(len(splitted_file_sha_contents_after) == 21)
        self.assertFalse('%s:' % file_kitchen_path in file_sha_contents_after)

    def test_recipe_delete(self):
        recipe_info = pickle.load(
            open(normalize(os.path.join(self.files_path, "sample_recipe_001.p"), WIN), "rb")
        )
        kitchen_name = 'test_kitchen'
        temp_dir = tempfile.mkdtemp(prefix='unit-tests', dir=TestDKRecipeDisk._TEMPFILE_LOCATION)
        DKKitchenDisk.write_kitchen(kitchen_name, temp_dir)
        kitchen_dir = os.path.join(temp_dir, kitchen_name)

        recipe_name = 'simple'
        recipe = recipe_info['recipes'][recipe_name]
        d = DKRecipeDisk(self.get_mock_ignore(), recipe_info['ORIG_HEAD'], recipe, kitchen_dir)
        rc = d.save_recipe_to_disk()
        self.assertTrue(rc is not None)

        # Check sha before changes
        file_sha_contents_before = self._get_file_sha(recipe_name, kitchen_dir)
        splitted_file_sha_contents_before = file_sha_contents_before.split('\n')
        self.assertTrue(len(splitted_file_sha_contents_before) == 22)

        # Perform the action we are testing
        DKRecipeDisk.write_recipe_state_recipe_delete(kitchen_dir, recipe_name)

        # Check recipe is not there any more
        file_sha_contents_after = self._get_file_sha(kitchen_dir, recipe_name)

        self.assertEquals('', file_sha_contents_after)

    def test_compare_sha(self):
        recipe_info = pickle.load(open(self.pickle_recipe_path, "rb"))
        temp_dir = tempfile.mkdtemp(prefix='unit-tests', dir=TestDKRecipeDisk._TEMPFILE_LOCATION)
        kitchen_name = 'test_kitchen'
        DKKitchenDisk.write_kitchen(kitchen_name, temp_dir)
        kitchen_dir = os.path.join(temp_dir, kitchen_name)

        recipe_name = 'simple'
        recipe = recipe_info['recipes'][recipe_name]
        d = DKRecipeDisk(self.get_mock_ignore(), recipe_info['ORIG_HEAD'], recipe, kitchen_dir)
        rc = d.save_recipe_to_disk()
        self.assertTrue(rc is not None)

        # LOCAL CHANGES - Muck with both side to create differences
        local_sha_dir = os.path.join(kitchen_dir, recipe_name)

        # Modify existing file
        with open(os.path.join(local_sha_dir, normalize('node1/precondition.json', WIN)), 'w') as f:
            f.write('some new content')
        with open(os.path.join(local_sha_dir, normalize('node1/description.json', WIN)), 'w') as f:
            f.write('BooGa BooGa')
        # Add a new file
        with open(os.path.join(local_sha_dir, normalize('node1/newfile.json', WIN)), 'w') as f:
            f.write('This is my new file. Hooray!')
        # Delete a file
        os.remove(os.path.join(local_sha_dir, normalize('node1/post_condition.json', WIN)))
        # Remove a directory
        shutil.rmtree(os.path.join(local_sha_dir, normalize('node1/data_sinks', WIN)))

        # "REMOTE" Changes
        # Change a sha
        recipe['simple/node2'][0]['sha'] = 'Who messed with my sha!'
        # Remove a remote file
        recipe['simple/node2'].pop()
        # Remove a directory
        del recipe['simple/node2/data_sinks']
        # Modify a remote file
        node1 = 'simple/node1'
        node1_filename = 'description.json'
        node1_sha = 'a new sha in remote'
        recipe[node1][0] = {'filename': node1_filename, 'sha': node1_sha}

        local_sha = get_directory_sha(self.get_mock_ignore(), local_sha_dir)
        recipe_dict = dict()
        recipe_dict['recipes'] = dict()
        recipe_dict['recipes']['simple'] = recipe
        normalize_recipe_dict(recipe_dict, WIN)
        rv = compare_sha(
            self.get_mock_ignore(), recipe_dict['recipes']['simple'], local_sha, local_sha_dir,
            recipe_name
        )

        same_count = 0
        for folder_name, folder_contents in six.iteritems(rv['same']):
            same_count += len(folder_contents)
        self.assertTrue(same_count >= 12)
        self.assertEqual(len(rv['different']), 2)

        only_local_count = 0
        for folder_name, folder_contents in six.iteritems(rv['only_local']):
            only_local_count += len(folder_contents)

        self.assertEqual(only_local_count, 3)
        self.assertEqual(len(rv['only_remote']), 2)

        # check local modified
        local_modified = rv.get('local_modified')
        self.assertEqual(1, len(local_modified))
        self.assertEqual(normalize(node1, WIN), list(local_modified.keys())[0])
        values = local_modified[normalize(node1, WIN)]
        self.assertEqual(1, len(values))
        self.assertEqual('precondition.json', values[0]['filename'])

        # check remote modified
        remote_modified = rv.get('remote_modified')
        self.assertEqual(1, len(remote_modified))
        self.assertEqual(normalize(u'simple/node2', WIN), list(remote_modified.keys())[0])
        values = remote_modified[normalize(u'simple/node2', WIN)]
        self.assertEqual(1, len(values))
        self.assertEqual(u'description.json', values[0]['filename'])

        # check modified both local and remote
        local_and_remote_modified = rv.get('local_and_remote_modified')
        self.assertEqual(1, len(local_and_remote_modified))
        self.assertEqual(normalize(node1, WIN), list(local_and_remote_modified.keys())[0])
        values = local_and_remote_modified[normalize(node1, WIN)]
        self.assertEqual(1, len(values))
        self.assertEqual(node1_filename, values[0]['filename'])
        self.assertEqual(node1_sha, values[0]['sha'])

        shutil.rmtree(temp_dir)

    def test_flatten_tree(self):
        print('hello')

    def test_build_sha1_directory(self):
        fp = os.path.join(self.files_path, 'recipe01')
        r = get_directory_sha(self.get_mock_ignore(), fp)
        self.assertIn('recipe01', r)
        self.assertIn(normalize('recipe01/sub01', WIN), r)
        self.assertIn(normalize('recipe01/sub01/sub02', WIN), r)
        sub02 = r[normalize('recipe01/sub01/sub02', WIN)]
        sub01 = r[normalize('recipe01/sub01', WIN)]
        root = r[normalize('recipe01', WIN)]
        self.assertEqual(1, len(sub02))
        self.assertEqual(1, len(sub01))
        self.assertEqual(1, len(root))
        self.assertEqual(sub02[0]['filename'], 'file_01_01_02_02.txt')
        self.assertEqual(sub02[0]['sha'], '615487a0933769879c9114e38c45c6a55ed84f1d')
        self.assertEqual(sub01[0]['filename'], 'file_01_01_01.txt')
        self.assertEqual(sub01[0]['sha'], '3da4c3e0af822e6e38dcf9ac3772c10a283a388d')
        self.assertEqual(root[0]['filename'], 'file_01_01.txt')
        self.assertEqual(root[0]['sha'], 'c9536cbfeddf3b47bce62052c516550d742e6840')

    # <kitchen_name>
    #   .dk
    #       KITCHEN_META
    #   bad
    #       .dk
    #   kitchen_subdir
    #   recipe1
    #       node1
    def _make_kitchen_testing_dir(self, kitchen_name):
        temp_dir = tempfile.mkdtemp(prefix='unit-tests', dir=TestDKRecipeDisk._TEMPFILE_LOCATION)
        kitchen_dir = os.path.join(temp_dir, kitchen_name)
        os.mkdir(kitchen_dir)
        dot_dir = os.path.join(kitchen_dir, '.dk')
        os.mkdir(dot_dir)

        bad_dir = os.path.join(temp_dir, 'bad')
        os.mkdir(bad_dir)
        bad_dot_dir = os.path.join(bad_dir, '.dk')
        os.mkdir(bad_dot_dir)

        with open(os.path.join(dot_dir, 'KITCHEN_META'), 'w') as kitchen_file:
            kitchen_file.write(kitchen_name)

        kitchen_subdir = os.path.join(kitchen_dir, 'kitchen_subdir')
        os.mkdir(kitchen_subdir)

        # Recipes
        recipes_subdir = os.path.join(dot_dir, 'recipes')
        os.mkdir(recipes_subdir)

        recipe_subdir = os.path.join(recipes_subdir, 'recipe1')
        os.mkdir(recipe_subdir)

        with open(os.path.join(recipe_subdir, 'RECIPE_META'), 'w') as recipe_meta_file:
            recipe_meta_file.write('recipe1')

        recipe1_subdir = os.path.join(kitchen_dir, 'recipe1')
        os.mkdir(recipe1_subdir)

        node1_subdir = os.path.join(recipe1_subdir, 'node1')
        os.mkdir(node1_subdir)

        ds_subdir = os.path.join(node1_subdir, 'data_sources')
        os.mkdir(ds_subdir)

        return temp_dir, kitchen_dir, kitchen_subdir, bad_dir

    def test_find_kitchen(self):

        kitchen_name = 'bobo'
        temp_dir, kitchen_dir, kitchen_subdir, bad_dir = self._make_kitchen_testing_dir(
            kitchen_name
        )

        self.assertIsNone(DKKitchenDisk.find_kitchen_name(temp_dir))
        self.assertEqual(DKKitchenDisk.find_kitchen_name(kitchen_dir), kitchen_name)
        self.assertEqual(DKKitchenDisk.find_kitchen_name(kitchen_subdir), kitchen_name)
        self.assertIsNone(DKKitchenDisk.find_kitchen_name(bad_dir))

        shutil.rmtree(temp_dir)

    def test_find_kitchen_meta_dir(self):

        kitchen_name = 'bobo'
        temp_dir, kitchen_dir, kitchen_subdir, bad_dir = self._make_kitchen_testing_dir(
            kitchen_name
        )

        kitchen_meta_dir = os.path.join(temp_dir, kitchen_name, DK_DIR)
        self.assertIsNone(DKKitchenDisk.find_kitchen_meta_dir(temp_dir))
        self.assertEqual(DKKitchenDisk.find_kitchen_meta_dir(kitchen_dir), kitchen_meta_dir)
        self.assertEqual(DKKitchenDisk.find_kitchen_meta_dir(kitchen_subdir), kitchen_meta_dir)
        self.assertIsNone(DKKitchenDisk.find_kitchen_meta_dir(bad_dir))

    def test_find_kitchen_root_dir(self):
        kitchen_name = 'bobo'
        temp_dir, kitchen_dir, kitchen_subdir, bad_dir = self._make_kitchen_testing_dir(
            kitchen_name
        )
        self.assertIsNone(DKKitchenDisk.find_kitchen_root_dir(temp_dir))
        self.assertEqual(DKKitchenDisk.find_kitchen_root_dir(kitchen_dir), kitchen_dir)
        self.assertEqual(DKKitchenDisk.find_kitchen_root_dir(kitchen_subdir), kitchen_dir)
        self.assertIsNone(DKKitchenDisk.find_kitchen_root_dir(bad_dir))

    def test_is_kitchen_root_dir(self):
        kitchen_name = 'bobo'
        temp_dir, kitchen_dir, kitchen_subdir, bad_dir = self._make_kitchen_testing_dir(
            kitchen_name
        )
        self.assertFalse(DKKitchenDisk.is_kitchen_root_dir(temp_dir))
        self.assertTrue(DKKitchenDisk.is_kitchen_root_dir(kitchen_dir))
        self.assertFalse(DKKitchenDisk.is_kitchen_root_dir(kitchen_subdir))
        self.assertFalse(DKKitchenDisk.is_kitchen_root_dir(bad_dir))

    def _setup_recipe_on_disk(self):
        r = pickle.load(open(self.pickle_recipe_path, "rb"))
        self.temp_dir = tempfile.mkdtemp(
            prefix='unit-tests', dir=TestDKRecipeDisk._TEMPFILE_LOCATION
        )
        kitchen_name = 'test_kitchen'
        DKKitchenDisk.write_kitchen(kitchen_name, self.temp_dir)
        kitchen_dir = os.path.join(self.temp_dir, kitchen_name)

        d = DKRecipeDisk(
            self.get_mock_ignore(), r['ORIG_HEAD'], r['recipes']['simple'], kitchen_dir
        )
        d.save_recipe_to_disk()
        return d

    # -------------------------------- Helper Methods ------------------------------------------------------------------
    def _get_file_sha(self, recipe_name, kitchen_path):
        full_path = os.path.join(kitchen_path, '.dk', 'recipes', recipe_name, 'FILE_SHA')
        contents = DKFileHelper.read_file(full_path)
        return contents
