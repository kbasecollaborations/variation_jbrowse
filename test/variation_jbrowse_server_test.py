# -*- coding: utf-8 -*-
import os
import time
import unittest
from configparser import ConfigParser

from variation_jbrowse.variation_jbrowseImpl import variation_jbrowse
from variation_jbrowse.variation_jbrowseServer import MethodContext
from variation_jbrowse.authclient import KBaseAuth as _KBaseAuth

from installed_clients.AssemblyUtilClient import AssemblyUtil
from installed_clients.WorkspaceClient import Workspace


class variation_jbrowseTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = os.environ.get('KB_AUTH_TOKEN', None)
        config_file = os.environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('variation_jbrowse'):
            cls.cfg[nameval[0]] = nameval[1]
        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'variation_jbrowse',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.serviceImpl = variation_jbrowse(cls.cfg)
        cls.callback_url = os.environ['SDK_CALLBACK_URL']
#        ret = cls.wsClient.create_workspace({'workspace': cls.wsName})  # noqa
#        cls.prepareTestData()


    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    def test_run_variation_jbrowse_ok(self):
        # call your implementation
        ret = self.serviceImpl.run_variation_jbrowse(self.ctx,
                                                {'workspace_name':'pranjan77:narrative_1601290579560',
                                                  'variation_ref': '48223/7/15'
                                                 })


