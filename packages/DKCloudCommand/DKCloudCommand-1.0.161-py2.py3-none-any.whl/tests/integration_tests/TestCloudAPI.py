import datetime
import json
import os
import pickle
import shutil
import six
import unittest

from time import time, sleep

from .BaseTestCloud import BaseTestCloud, WaitLoop
from DKCloudCommand.modules.DKCloudAPI import DKCloudAPI
from DKCloudCommand.modules.DKCloudCommandRunner import DKCloudCommandRunner


class TestCloudAPI(BaseTestCloud):

    pickle_dump = False

    def test_is_token_valid(self):
        self.assertIsNotNone(self._api._api_helper)
        self.assertIsNotNone(self._api._api_helper.token)

    def test_login(self):
        self.assertIsNotNone(self._api.login())

    def test_a_list_kitchen(self):
        # setup
        name = 'kitchens-plus'
        # test
        kitchens = self._list_kitchens()
        self.assertIsNotNone(kitchens)
        found = False
        for kitchen in kitchens:
            if isinstance(kitchen, dict) is True and 'name' in kitchen and name == kitchen['name']:
                found = True
        self.assertTrue(found)

    def test_create_kitchen(self):
        # setup
        parent_kitchen = 'CLI-Top'
        new_kitchen = 'temp-volatile-kitchen-API'
        new_kitchen = self._add_my_guid(new_kitchen)
        description = 'Some description'
        # test
        self._delete_and_clean_kitchen(new_kitchen)  # clean up junk
        rc = self._create_kitchen(parent_kitchen, new_kitchen, description)
        self.assertTrue(rc)
        kitchens = self._list_kitchens()
        created_kitchen = None
        for kitchen in kitchens:
            if isinstance(kitchen,
                          dict) is True and 'name' in kitchen and new_kitchen == kitchen['name']:
                created_kitchen = kitchen
                break

        self.assertIsNotNone(created_kitchen)
        self.assertEqual(description, created_kitchen['description'])

    def test_delete_kitchen(self):
        # setup
        parent_kitchen = 'CLI-Top'
        del_kitchen = 'temp-fleeting-kitchen-API'
        del_kitchen = self._add_my_guid(del_kitchen)
        self._delete_and_clean_kitchen(del_kitchen)  # clean up junk
        rc = self._create_kitchen(parent_kitchen, del_kitchen)
        self.assertTrue(rc)
        # test
        rc = self._delete_and_clean_kitchen(del_kitchen)
        self.assertTrue(rc)
        kitchens = self._list_kitchens()
        found = False
        for kitchen in kitchens:
            if isinstance(kitchen,
                          dict) is True and 'name' in kitchen and del_kitchen == kitchen['name']:
                found = True
        self.assertFalse(found)

    def test_update_kitchen(self):
        update_kitchen_name = self._branch
        original_description = 'example description'
        update_description = '%s %s' % (original_description, 'command line test')
        # setup
        update_kitchen = self._get_kitchen_dict(update_kitchen_name)
        self.assertIsNotNone(update_kitchen)
        update_kitchen['description'] = update_description
        # test
        self.assertTrue(self._api.update_kitchen(update_kitchen, 'command line test 2'))

        if self._use_mock is False:
            updated_kitchen = self._get_kitchen_dict(update_kitchen_name)
            self.assertTrue('description' in updated_kitchen)
            self.assertTrue(updated_kitchen['description'] == update_description)
            updated_kitchen['description'] = original_description
            self.assertTrue(self._api.update_kitchen(updated_kitchen, 'command line test 2'))

    def test_list_recipe(self):
        # setup
        kitchen = 'CLI-Top'
        recipe_name = 'simple'
        # test
        recipe_names = self._list_recipe(kitchen)
        self.assertIsNotNone(recipe_names)
        my_recipe = next(recipe for recipe in recipe_names if recipe == recipe_name)
        self.assertIsNotNone(my_recipe)  # should get back a list of strings

    def test_get_recipe(self):
        # setup
        kitchen = 'CLI-Top'
        recipe = 'simple'

        # How do we handle a non-existent recipe?
        bad_recipe = "momo"
        has_exception = False
        try:
            self._api.get_recipe(kitchen, bad_recipe)
        except Exception as e:
            has_exception = True
            self.assertTrue('Recipe "%s" not found in kitchen %s' % (bad_recipe, kitchen) in str(e))

        self.assertTrue(has_exception)

        # test
        rs = self._get_recipe(kitchen, recipe)
        self.assertIsNotNone(rs)
        # save recipe for use in DKRecipeDisk.py unit tests
        if TestCloudAPI.pickle_dump:
            pickle.dump(rs, open("recipe.p", "wb"))
        found = False
        for r in rs:
            if isinstance(r, six.text_type):
                found = True
        self.assertTrue(found)  # should get back a list of strings

    def test_recipe_status(self):
        # setup
        kitchen = 'CLI-Top'
        recipe = 'simple'

        cwd = os.getcwd()

        temp_dir, kitchen_dir = self._make_kitchen_dir(kitchen, change_dir=True)

        start_time = time()
        rv = DKCloudCommandRunner.get_recipe(self._api, kitchen, recipe)
        elapsed_recipe_status = time() - start_time
        print('get_recipe - elapsed: %d' % elapsed_recipe_status)

        new_path = os.path.join(kitchen_dir, recipe)
        os.chdir(new_path)

        new_file_path = os.path.join(new_path, 'new_file.txt')
        with open(new_file_path, 'w') as new_file:
            new_file.write('this is my new contents')
            new_file.flush()

        new_dir_path = os.path.join(new_path, 'newsubdir')
        os.makedirs(new_dir_path)

        new_sub_file_path = os.path.join(new_dir_path, 'new_sub_file.txt')
        with open(new_sub_file_path, 'w') as new_file:
            new_file.write('this is my new contents in my sub file')
            new_file.flush()

        newsubdir2 = os.path.join(new_path, 'newsubdir2')
        os.makedirs(newsubdir2)

        newsubsubdir = os.path.join(newsubdir2, 'newsubsubdir')
        os.makedirs(newsubsubdir)

        new_file_in_subsubdir = os.path.join(newsubsubdir, 'new-subsubdir-file.txt')
        with open(new_file_in_subsubdir, 'w') as new_file_in_subsubdir_file:
            new_file_in_subsubdir_file.write('{\n\t"animal":"cat",\n\t"color":"blue"\n}')
            new_file_in_subsubdir_file.flush()

        variables = os.path.join(new_path, 'variables.json')
        os.remove(variables)

        source_path = os.path.join(
            new_path, os.path.normpath('node2/data_sources/DKDataSource_NoOp.json')
        )
        with open(source_path, 'a') as source_file:
            source_file.write("I'm adding some text to this file")
            source_file.flush()

        node1 = os.path.join(new_path, 'node1')
        shutil.rmtree(node1)

        start_time = time()
        rc = self._api.recipe_status(kitchen, recipe)
        elapsed_recipe_status = time() - start_time
        print('recipe_status - elapsed: %d' % elapsed_recipe_status)
        self.assertTrue(rc.ok())
        rv = rc.get_payload()
        self.assertEqual(len(rv['different']), 1)
        self.assertEqual(len(rv['only_remote']), 4)
        self.assertEqual(len(rv['only_local']), 4)
        self.assertEqual(len(rv['same']), 6)
        self.assertEqual(len(rv['same'][os.path.normpath('simple/node2')]), 4)

        os.chdir(cwd)
        shutil.rmtree(temp_dir)

    def test_path_sorting(self):

        paths = [
            'description.json', 'graph.json', 'simple-file.txt', 'variables.json',
            'variations.json', 'node2/data_sinks', 'node1/data_sinks', 'node2', 'node1',
            'node1/data_sources', 'resources', 'node2/data_sources'
        ]
        paths = [
            'simple/newsubdir', 'simple/new_file.txt', 'simple/newsubdir2',
            'simple/newsubdir2/newsubsubdir'
        ]
        paths_sorted = sorted(paths)
        for idx, path in enumerate(paths_sorted):
            dir = os.path.dirname(os.path.commonprefix(paths))
        print(dir)

    def test_update_file(self):
        # setup
        parent_kitchen = 'CLI-Top'
        test_kitchen = 'CLI-test_update_file'
        test_kitchen = self._add_my_guid(test_kitchen)
        recipe_name = 'simple'
        file_name = 'description.json'
        api_file_key = file_name
        message = 'test update CLI-test_update_file'
        update_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        self._delete_and_clean_kitchen(test_kitchen)

        original_file = self._get_recipe_file(
            parent_kitchen, recipe_name, file_name, DKCloudAPI.JSON
        )
        self.assertTrue(self._create_kitchen(parent_kitchen, test_kitchen))
        new_kitchen_file = self._get_recipe_file(
            test_kitchen, recipe_name, file_name, DKCloudAPI.JSON
        )
        self.assertEqual(original_file, new_kitchen_file)
        new_kitchen_file_dict = self._get_the_dict(new_kitchen_file)

        # test
        new_kitchen_file_dict[test_kitchen] = update_str
        new_kitchen_file2 = self._get_the_json_str(new_kitchen_file_dict)
        rv = self._api.update_file(
            test_kitchen, recipe_name, message, api_file_key, new_kitchen_file2
        )
        self.assertTrue(rv.ok())
        new_kitchen_file3 = self._get_recipe_file(
            test_kitchen, recipe_name, file_name, DKCloudAPI.JSON
        )
        self.assertEqual(new_kitchen_file2.strip(), new_kitchen_file3.strip())

    def test_add_file(self):
        # setup
        parent_kitchen = 'CLI-Top'
        test_kitchen = 'test_create_file-API'
        test_kitchen = self._add_my_guid(test_kitchen)
        recipe_name = 'simple'
        file_name = 'added.sql'
        filedir = 'resources'
        recipe_file_key = os.path.join(recipe_name, filedir)
        file_contents = '--\n-- sql for you\n--\n\nselect 1024\n\n'
        file_path = os.path.join(filedir, file_name)
        message = 'test update test_create_file-API'
        self._delete_and_clean_kitchen(test_kitchen)
        self.assertTrue(self._create_kitchen(parent_kitchen, test_kitchen))
        # test
        rv = self._api.add_file(test_kitchen, recipe_name, message, file_path, file_contents)
        self.assertTrue(rv, "API add file failed")

        new_file = self._get_recipe_file_full(
            test_kitchen, recipe_name, recipe_file_key, file_name, DKCloudAPI.TEXT, check=False
        )
        self.assertTrue(new_file is not None)
        self.assertEqual(file_contents, new_file)

    def test_delete_file_top1(self):
        # setup
        parent_kitchen = 'CLI-Top'
        test_kitchen = 'test_delete_file_top1-API'
        test_kitchen = self._add_my_guid(test_kitchen)
        recipe_name = 'simple'
        file_name = 'description.json'
        recipe_file_key = file_name
        message = 'test update test_delete_file_top1-API'
        self._delete_and_clean_kitchen(test_kitchen)  # make sure it is gone
        self.assertTrue(self._create_kitchen(parent_kitchen, test_kitchen))
        # test
        sleep(10)
        rv = self._api.delete_file(test_kitchen, recipe_name, message, recipe_file_key, file_name)
        self.assertTrue(rv.ok())

        sleep(10)
        gone_kitchen_file = self._get_recipe_file(
            test_kitchen, recipe_name, file_name, DKCloudAPI.JSON, check=False
        )
        self.assertTrue(gone_kitchen_file is None)

    def test_delete_file_deeper(self):
        # setup
        parent_kitchen = 'CLI-Top'
        test_kitchen = 'test_delete_file_deeper-API'
        test_kitchen = self._add_my_guid(test_kitchen)
        recipe_name = 'simple'
        filedir = 'resources'
        file_name = 'very_cool.sql'
        api_file_key = os.path.join(filedir, file_name)
        recipe_file_key = os.path.join(recipe_name, filedir)
        message = 'test update test_delete_file_deeper-API'
        self._delete_and_clean_kitchen(test_kitchen)
        self.assertTrue(self._create_kitchen(parent_kitchen, test_kitchen))
        # test
        sleep(10)
        rv = self._api.delete_file(test_kitchen, recipe_name, message, api_file_key, file_name)
        self.assertTrue(rv.ok())

        gone_kitchen_file = self._get_recipe_file_full(
            test_kitchen, recipe_name, recipe_file_key, file_name, 'text', False
        )
        self.assertTrue(gone_kitchen_file is None)

    # --------------------------------------------------------------------------------------------------------------------
    #  Order commands
    # --------------------------------------------------------------------------------------------------------------------

    def test_create_order(self):
        # setup
        kitchen = 'CLI-Top'
        recipe = 'simple'
        variation = 'simple-variation-now'
        # test
        rs = self._create_order(kitchen, recipe, variation)
        self.assertIsNotNone(rs)
        self.assertTrue('status' in rs)
        self.assertEqual('success', rs['status'])
        self.assertTrue('order_id' in rs)

    def test_create_order_one_node(self):
        # setup
        kitchen = 'CLI-Top'
        recipe = 'simple'
        variation = 'simple-variation-now'
        node = 'node2'
        # test
        rs = self._create_order(kitchen, recipe, variation, node)
        self.assertIsNotNone(rs)
        self.assertTrue('status' in rs)
        self.assertEqual('success', rs['status'])
        self.assertTrue('order_id' in rs)

    def test_delete_all_order(self):
        # setup
        parent_kitchen = 'CLI-Top'
        new_kitchen = 'test_deleteall_orderAPI'
        new_kitchen = self._add_my_guid(new_kitchen)
        recipe = 'simple'
        variation = 'simple-variation-now'
        self._delete_and_clean_kitchen(new_kitchen)  # clean up junk
        rc = self._create_kitchen(parent_kitchen, new_kitchen)
        self.assertTrue(rc)
        rs = self._create_order(new_kitchen, recipe, variation)
        self.assertIsNotNone(rs)
        self.assertTrue('status' in rs)
        self.assertEqual('success', rs['status'])
        self.assertTrue('order_id' in rs)
        # test
        rc = self._order_delete_all(new_kitchen)

    def test_delete_one_order(self):
        # setup
        parent_kitchen = 'CLI-Top'
        new_kitchen = 'test_delete_one_order-API'
        new_kitchen = self._add_my_guid(new_kitchen)
        recipe = 'simple'
        variation = 'simple-variation-now'
        self._delete_and_clean_kitchen(new_kitchen)  # clean up junk
        rc = self._create_kitchen(parent_kitchen, new_kitchen)
        self.assertTrue(rc)
        order_response = self._create_order(new_kitchen, recipe, variation)
        self.assertIsNotNone(order_response)
        self.assertTrue('status' in order_response)
        self.assertEqual('success', order_response['status'])
        self.assertTrue('order_id' in order_response)
        # test
        order_id = order_response['order_id']
        rc = self._order_delete_one(new_kitchen, order_id)
        self.assertTrue(rc.ok())

    def test_order_stop(self):
        # setup
        parent_kitchen = 'CLI-Top-k8s'
        new_kitchen = 'test_order_stop-API'
        new_kitchen = self._add_my_guid(new_kitchen)
        recipe = 'test-everything-recipe'
        variation = self._get_run_variation_for_recipe('test-everything-recipe')
        self._delete_and_clean_kitchen(new_kitchen)  # clean up junk
        rc = self._create_kitchen(parent_kitchen, new_kitchen)
        self.assertTrue(rc)
        order_response = self._create_order(new_kitchen, recipe, variation)
        self.assertIsNotNone(order_response)
        order_id = order_response['order_id']
        # test
        sleep(2)
        rc = self._order_stop(new_kitchen, order_id)

    def test_orderrun_stop(self):
        parent_kitchen = 'CLI-Top'
        new_kitchen = 'test_orderrun_stop-API'
        new_kitchen = self._add_my_guid(new_kitchen)
        recipe_name = 'parallel-recipe-test'
        variation_name = self._get_run_variation_for_recipe(recipe_name)

        self._delete_and_clean_kitchen(new_kitchen)
        rc = self._create_kitchen(parent_kitchen, new_kitchen)
        self.assertTrue(rc.ok())

        # test
        order_response = self._create_order(new_kitchen, recipe_name, variation_name)
        self.assertIsNotNone(order_response)
        new_order_id = order_response['order_id']

        # order should be available immediately
        rc = self._api.list_order(new_kitchen)
        self.assertTrue(rc.ok())
        order_stuff = rc.get_payload()
        self.assertTrue('orders' in order_stuff)
        self.assertTrue('servings' in order_stuff)
        found_order = next(
            (order for order in order_stuff['orders'] if order['hid'] == new_order_id), None
        )
        self.assertIsNotNone(found_order)

        # wait a few seconds for the serving
        found_serving = None
        wait_loop = WaitLoop(sleep=1, timeout=20)

        while wait_loop:
            rc = self._api.list_order(new_kitchen)
            self.assertTrue(rc.ok())
            order_stuff = rc.get_payload()
            self.assertTrue('servings' in order_stuff)
            if new_order_id in order_stuff['servings'] and \
                    'servings' in order_stuff['servings'][new_order_id] and \
                    len(order_stuff['servings'][new_order_id]['servings']) > 0 and \
                    'orderrun_status' in order_stuff['servings'][new_order_id]['servings'][0]:
                found_serving = order_stuff['servings'][new_order_id]['servings'][0]
            if found_serving is not None:
                break

        self.assertIsNotNone(found_serving)
        orderrun_id = found_serving['hid']
        rc2 = self._orderrun_stop(new_kitchen, orderrun_id)
        self.assertTrue(rc2.ok())

    def test_get_compiled_order_run_from_recipe(self):
        # setup
        parent_kitchen = 'CLI-Top'
        new_kitchen = 'test_get_compiled_order_run_from_recipe-API'
        new_kitchen = self._add_my_guid(new_kitchen)
        recipe_name = 'parallel-recipe-test'
        variation_name = 'variation-test'
        self._delete_and_clean_kitchen(new_kitchen)
        self.assertTrue(self._create_kitchen(parent_kitchen, new_kitchen))
        # test
        resp = self._get_compiled_order_run(parent_kitchen, recipe_name, variation_name)
        self.assertTrue(isinstance(resp, dict))
        found = False
        for rn, recipe in six.iteritems(resp):
            if rn == recipe_name:
                found = True
        self.assertTrue(found)
        self.assertTrue(isinstance(resp, dict))
        self.assertTrue(len(resp) == 28)
        self.assertTrue(len(resp[recipe_name]) == 4)
        self.assertTrue(isinstance(resp[recipe_name], list))
        found_desc = False
        for item in resp[recipe_name]:
            if 'filename' in item and 'json' in item and item['filename'] == 'description.json':
                found_desc = True
                self.assertTrue(len(item['json']) >= 1)
        self.assertTrue(found_desc)

    def test_merge_kitchens_success(self):
        existing_kitchen_name = 'CLI-Top'
        base_test_kitchen_name = 'base-test-kitchen'
        base_test_kitchen_name = self._add_my_guid(base_test_kitchen_name)
        branched_test_kitchen_name = 'branched-from-base-test-kitchen'
        branched_test_kitchen_name = self._add_my_guid(branched_test_kitchen_name)

        # setup
        self._delete_and_clean_kitchen(branched_test_kitchen_name)
        self._delete_and_clean_kitchen(base_test_kitchen_name)
        # test
        # create base kitchen
        self.assertTrue(self._create_kitchen(existing_kitchen_name, base_test_kitchen_name))
        # create branch kitchen from base kitchen
        self.assertTrue(self._create_kitchen(base_test_kitchen_name, branched_test_kitchen_name))
        # do merge
        self._merge_kitchens(branched_test_kitchen_name, base_test_kitchen_name)
        self._merge_kitchens(base_test_kitchen_name, branched_test_kitchen_name)

    def test_merge_kitchens_improved(self):
        setup = True
        cleanup = True
        existing_kitchen_name = 'CLI-Top'
        recipe = 'simple'
        parent_kitchen = 'merge-parent'
        parent_kitchen = self._add_my_guid(parent_kitchen, delete_branch_on_teardown=cleanup)
        child_kitchen = 'merge-child'
        child_kitchen = self._add_my_guid(child_kitchen, delete_branch_on_teardown=cleanup)
        conflict_file = 'conflicted-file.txt'

        if setup:
            # # setup
            self._delete_and_clean_kitchen(parent_kitchen)
            self._delete_and_clean_kitchen(child_kitchen)
            self.assertTrue(self._create_kitchen(existing_kitchen_name, parent_kitchen))

            sleep(10)
            rv = self._api.add_file(
                parent_kitchen, recipe,
                'File will be changed on both branches to create a conflict.', conflict_file,
                'top\nbottom\n'
            )
            self.assertTrue(rv.ok())

            sleep(10)
            self.assertTrue(self._create_kitchen(parent_kitchen, child_kitchen))

            sleep(10)
            rv = self._api.update_file(
                child_kitchen, recipe, 'Changes on child to cause conflict', conflict_file,
                'top\nchild\nbottom\n'
            )
            self.assertTrue(rv.ok())

            sleep(10)
            rv = self._api.update_file(
                child_kitchen, recipe, 'Changes on parent to cause conflict', conflict_file,
                'top\nparent\nbottom\n'
            )
            self.assertTrue(rv.ok())

        # do merge
        self._merge_kitchens(child_kitchen, parent_kitchen)

    def test_list_order_errors(self):
        bad_kitchen = 'bsdfdfsdlomobo'
        rc = self._api.list_order(bad_kitchen, 5, 2)
        self.assertTrue(rc.ok())
        order_stuff = rc.get_payload()
        self.assertIsNotNone(len(order_stuff['orders']) == 0)

    def test_list_order_quick(self):
        test_kitchen = 'CLI-Top'
        # order should be available immediately
        rc = self._api.list_order(test_kitchen, 5, 2)
        self.assertTrue(rc.ok())
        order_stuff = rc.get_payload()
        self.assertTrue('orders' in order_stuff)
        self.assertTrue('servings' in order_stuff)

    def test_list_order(self):
        parent_kitchen = 'master'
        new_kitchen = self._add_my_guid('test_order_status')
        recipe_name = 'parallel-recipe-test'
        variation_name = self._get_run_variation_for_recipe(recipe_name)

        self._delete_and_clean_kitchen(new_kitchen)
        rc = self._create_kitchen(parent_kitchen, new_kitchen)
        self.assertTrue(rc.ok())

        # test
        order_response = self._create_order(new_kitchen, recipe_name, variation_name)
        new_order_id = order_response['order_id']
        self.assertIsNotNone(new_order_id)

        # order should be available immediately
        rc = self._api.list_order(new_kitchen)
        self.assertTrue(rc.ok())
        order_stuff = rc.get_payload()
        self.assertTrue('orders' in order_stuff)
        self.assertTrue('servings' in order_stuff)
        found_order = next(
            (order for order in order_stuff['orders'] if order['hid'] == new_order_id), None
        )
        self.assertIsNotNone(found_order)

        # wait a few seconds for the serving
        found_serving = None
        wait_loop = WaitLoop()

        while wait_loop:
            rc = self._api.list_order(new_kitchen)
            self.assertTrue(rc.ok())
            order_stuff = rc.get_payload()
            self.assertTrue('servings' in order_stuff)
            if new_order_id in order_stuff['servings'] and \
                    'servings' in order_stuff['servings'][new_order_id] and \
                    len(order_stuff['servings'][new_order_id]['servings']) > 0 and \
                    'orderrun_status' in order_stuff['servings'][new_order_id]['servings'][0] and \
                    'OrderRun Completed' in order_stuff['servings'][new_order_id]['servings'][0]['orderrun_status']:
                found_serving = True
            if found_serving is not None:
                break

        self.assertIsNotNone(found_serving)

    def test_orderrun_delete(self):
        parent_kitchen = 'master'
        new_kitchen = 'test_orderrun_delete'
        new_kitchen = self._add_my_guid(new_kitchen)
        recipe_name = 'parallel-recipe-test'
        variation_name = self._get_run_variation_for_recipe(recipe_name)

        self._delete_and_clean_kitchen(new_kitchen)
        # @todo add a delete all to the orders for this kitchen
        rc = self._create_kitchen(parent_kitchen, new_kitchen)
        self.assertTrue(rc.ok())

        # test
        order_response = self._create_order(new_kitchen, recipe_name, variation_name)
        self.assertIsNotNone(order_response)
        new_order_id = order_response['order_id']

        # wait a few seconds for the serving
        found_serving = None
        wait_loop = WaitLoop(sleep=2, timeout=60)

        while wait_loop:
            rc = self._api.list_order(new_kitchen)
            self.assertTrue(rc.ok())
            order_stuff = rc.get_payload()
            print('got %s' % order_stuff)
            self.assertTrue('servings' in order_stuff)
            if new_order_id in order_stuff['servings'] and \
                    'servings' in order_stuff['servings'][new_order_id] and \
                    len(order_stuff['servings'][new_order_id]['servings']) > 0 and \
                    'orderrun_status' in order_stuff['servings'][new_order_id]['servings'][0]:
                found_serving = order_stuff['servings'][new_order_id]['servings'][0]
            if found_serving is not None:
                break

        self.assertIsNotNone(found_serving)

        rv = self._api.delete_orderrun(new_kitchen, found_serving['hid'])
        self.assertTrue(rv.ok())
        try:
            self._api.delete_orderrun(new_kitchen, 'bad_id')
            self.assertTrue(False, 'Error, Should raise an exception')
        except Exception as e:
            self.assertTrue('ServingDelete' in str(e))
            self.assertTrue("Serving id 'bad_id' does not exist." in str(e))

        rc = self._api.list_order(new_kitchen)
        self.assertTrue(rc.ok())
        order_stuff = rc.get_payload()
        self.assertTrue('servings' in order_stuff)
        found_serving = next(
            (serving for serving in order_stuff['servings'] if serving['order_id'] == new_order_id),
            None
        )
        self.assertIsNone(found_serving)

    def test_kitchen_config(self):
        parent_kitchen = 'CLI-Top'
        child_kitchen = self._add_my_guid('modify_kitchen_settings_api')

        setup = True
        if setup:
            self._delete_and_clean_kitchen(child_kitchen)
            self._create_kitchen(parent_kitchen, child_kitchen)

        # add overrides
        add = [('newvar1', 'newval1'), ('newvar2', 'newval2'),
               ('newvar1', 'this should be in list')]
        rc = self._api.modify_kitchen_settings(child_kitchen, add=add)
        self.assertTrue(rc.ok())
        overrides_dict = rc.get_payload()
        self.assertEquals('newval2', overrides_dict['newvar2'])
        self.assertEquals('this should be in list', overrides_dict['newvar1'])

        # add one more override
        add = [('newvarX', 'newval1')]
        rc = self._api.modify_kitchen_settings(child_kitchen, add=add)
        self.assertTrue(rc.ok())
        overrides_dict = rc.get_payload()
        self.assertEquals('this should be in list', overrides_dict['newvar1'])
        self.assertEquals('newval2', overrides_dict['newvar2'])
        self.assertEquals('newval1', overrides_dict['newvarX'])

        # remove one override
        unset = ['newvar1']
        rc = self._api.modify_kitchen_settings(child_kitchen, unset=unset)
        self.assertTrue(rc.ok())
        overrides_dict = rc.get_payload()
        self.assertEquals('newval2', overrides_dict['newvar2'])
        self.assertEquals('newval1', overrides_dict['newvarX'])
        self.assertTrue('newvar1' not in overrides_dict)

        # remove the other 2 overrides
        unset = ['newvar1', 'newvar2']
        rc = self._api.modify_kitchen_settings(child_kitchen, unset=unset)
        self.assertTrue(rc.ok())
        overrides_dict = rc.get_payload()
        self.assertTrue('newvar1' not in overrides_dict)
        self.assertTrue('newvar2' not in overrides_dict)
        self.assertEquals('newval1', overrides_dict['newvarX'])

        # remove a non existing override
        unset = ['doesnotexist']
        rc = self._api.modify_kitchen_settings(child_kitchen, unset=unset)
        self.assertTrue(rc.ok())
        overrides_dict = rc.get_payload()
        self.assertEquals('newval1', overrides_dict['newvarX'])

    def test_kitchen_settings(self):
        kitchen_name = 'CLI-Top'
        rc = self._api.get_kitchen_settings(kitchen_name)
        self.assertTrue(rc.ok())
        kitchen_json = rc.get_payload()
        self.assertTrue('recipeoverrides' in kitchen_json)

    def test_agent_status(self):
        data = self._api.agent_status()
        self.assertTrue(isinstance(data, dict))
        self.assertTrue('agent_status' in data)
        self.assertTrue('available' in data['agent_status'])
        self.assertTrue('disk' in data['agent_status'])
        self.assertTrue('mem' in data['agent_status'])

    # helpers ---------------------------------
    # get the recipe from the server and return the file
    # WORKS JUST FOR THE top level files
    # TODO get rid of this routine because it only woks for the top level directory,
    # TODO switch to using _get_recipe_file_full()
    def _get_recipe_file(self, kitchen, recipe, file_name, the_type, check=True):
        the_file = None
        rs = self._get_recipe_files(kitchen, recipe)
        self.assertIsNotNone(rs)
        self.assertTrue(recipe in rs)
        self.assertIsNotNone(isinstance(rs[recipe], list))
        for item in rs[recipe]:  # JUST LOOKS IN TOP LEVEL DIRECTORY
            self.assertTrue(isinstance(item, dict))
            if DKCloudAPI.FILENAME in item and item[DKCloudAPI.FILENAME
                                                    ] == file_name and the_type in item:
                if isinstance(item[DKCloudAPI.JSON], dict):
                    the_file = json.dumps(item[DKCloudAPI.JSON])
                else:
                    the_file = item[DKCloudAPI.JSON]
        if check:
            self.assertIsNotNone(the_file)  # skip this e.g. looking for a deleted file
        return the_file

    def _get_recipe_file_full(
            self, kitchen, recipe, recipe_file_key, file_name, the_type, check=True
    ):
        """
        :param kitchen:
        :param recipe:
        :param recipe_file_key: has the recipe name and the path to the file, but not the file
        :param file_name: just the file name
        :param the_type:
        :param check: set to false when you don't expect the file to be there
        :return:
        """
        the_file = None
        rs = self._get_recipe_files(kitchen, recipe)
        self.assertIsNotNone(rs)
        self.assertTrue(recipe in rs)
        self.assertIsNotNone(isinstance(rs[recipe], list))
        if recipe_file_key not in rs:
            return the_file
        for item in rs[recipe_file_key]:
            self.assertTrue(isinstance(item, dict))
            if DKCloudAPI.FILENAME in item and item[DKCloudAPI.FILENAME
                                                    ] == file_name and the_type in item:
                if the_type == DKCloudAPI.JSON:
                    if isinstance(item[DKCloudAPI.JSON], dict):
                        the_file = json.dumps(item[DKCloudAPI.JSON])
                    else:
                        the_file = item[DKCloudAPI.JSON]
                elif the_type == DKCloudAPI.TEXT:
                    the_file = item[DKCloudAPI.TEXT]
        if check:
            self.assertIsNotNone(the_file)  # skip this e.g. looking for a deleted file
        return the_file

    def _get_kitchen_dict(self, kitchen_name):
        return self._api.get_kitchen_dict(kitchen_name)

    def _create_kitchen(self, existing_kitchen_name, new_kitchen_name, description=None):
        return self._api.create_kitchen(
            existing_kitchen_name, new_kitchen_name, description, 'junk'
        )

    def _merge_kitchens(self, from_kitchen, to_kitchen, resolved_conflicts=None):
        ret = self._api.kitchens_merge(from_kitchen, to_kitchen, resolved_conflicts)
        url = '/dk/index.html#/history/dk/'
        self.assertTrue(url in ret)

    def _check_no_merge_conflicts(self, resp):
        self.assertTrue(isinstance(resp, dict))
        self.assertTrue('merge-kitchen-result' in resp)
        self.assertTrue('status' in resp['merge-kitchen-result'])
        self.assertTrue(resp['merge-kitchen-result']['status'] == 'success')

    def _check_merge_conflicts(
            self, resp, recipe_name, recipe_path, conflict_file_name, from_kitchen_name,
            to_kitchen_name
    ):
        self.assertTrue(isinstance(resp, dict))
        self.assertTrue('merge-kitchen-result' in resp)

        conflicts = resp['merge-kitchen-result']['merge_info']['conflicts']

        self.assertTrue(recipe_name in conflicts)
        self.assertTrue('status' in resp['merge-kitchen-result'])
        self.assertTrue(resp['merge-kitchen-result']['status'] == 'conflicts')
        self.assertTrue(recipe_path in conflicts[recipe_name])
        self.assertTrue(isinstance(conflicts[recipe_name][recipe_path], list))
        for f in conflicts[recipe_name][recipe_path]:
            self.assertTrue(isinstance(f, dict))
            self.assertTrue('filename' in f)
            self.assertEqual(conflict_file_name, f['filename'])
        self.assertTrue('from-kitchen-name' in resp)
        self.assertEqual(resp['from-kitchen-name'], from_kitchen_name)
        self.assertTrue('to-kitchen-name' in resp)
        self.assertEqual(resp['to-kitchen-name'], to_kitchen_name)

    def _list_kitchens(self):
        rc = self._api.list_kitchen()
        self.assertTrue(rc.ok())
        kitchens = rc.get_payload()
        # test
        self.assertTrue(isinstance(kitchens, list))
        return kitchens

    def _list_recipe(self, kitchen):
        rs = self._api.list_recipe(kitchen)
        self.assertTrue(rs.ok)
        # test
        self.assertTrue(isinstance(rs.get_payload(), list))
        return rs.get_payload()

    def _get_recipe_files(self, kitchen, recipe):
        rs = self._api.get_recipe(kitchen, recipe)
        self.assertTrue(rs.ok())
        # test
        payload = rs.get_payload()
        self.assertTrue('recipes' in payload)
        self.assertTrue(isinstance(payload['recipes'], dict))
        return payload['recipes'][recipe]

    def _get_recipe(self, kitchen, recipe):
        rs = self._api.get_recipe(kitchen, recipe)
        self.assertTrue(rs.ok())
        # test
        payload = rs.get_payload()
        self.assertTrue('recipes' in payload)
        self.assertTrue('ORIG_HEAD' in payload)
        self.assertTrue(isinstance(payload['recipes'], dict))
        return payload

    def _create_order(self, kitchen, recipe, variation, node=None):
        rc = self._api.create_order(kitchen, recipe, variation, node)
        self.assertTrue(rc.ok())
        rs = rc.payload
        self.assertTrue(isinstance(rs, dict))
        return rs

    def _order_delete_all(self, kitchen):
        rc = self._api.order_delete_all(kitchen)
        self.assertTrue(rc.ok())
        return rc

    def _order_delete_one(self, kitchen, order_id):
        rc = self._api.order_delete_one(kitchen, order_id)
        self.assertTrue(rc.ok())
        return rc

    def _order_stop(self, kitchen, order_id):
        rc = self._api.order_stop(kitchen, order_id)
        self.assertTrue(rc.ok())
        return rc

    def _orderrun_stop(self, kitchen, orderrun_id):
        rc = self._api.orderrun_stop(kitchen, orderrun_id)
        self.assertTrue(rc.ok())
        return rc

    def _orderrun_detail(self, kitchen):
        rc = self._api.orderrun_detail(kitchen, dict())
        self.assertTrue(rc.ok())
        rs = rc.get_payload()['servings']
        self.assertTrue(isinstance(rs, list))
        return rs

    def _get_compiled_order_run(self, kitchen, recipe_name, veriation_name):
        rd = self._api.get_compiled_order_run(kitchen, recipe_name, veriation_name)
        self.assertTrue(rd.ok())
        p = rd.get_payload()
        return p


if __name__ == '__main__':
    unittest.main()
