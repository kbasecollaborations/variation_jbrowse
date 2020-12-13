# -*- coding: utf-8 -*-
#BEGIN_HEADER
# The header block is where all import statments should live
import logging
import os
from pprint import pformat
import uuid
import requests
import json

#from Bio import SeqIO

#from installed_clients.AssemblyUtilClient import AssemblyUtil
from installed_clients.KBaseReportClient import KBaseReport
from variation_jbrowse.Utils.htmlreportutils import htmlreportutils
#END_HEADER


class variation_jbrowse:
    '''
    Module Name:
    variation_jbrowse

    Module Description:
    A KBase module: variation_jbrowse
This sample module contains one small method that filters contigs.
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = ""
    GIT_COMMIT_HASH = ""

    #BEGIN_CLASS_HEADER
    # Class variables and functions can be defined in this block
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        
        # Any configuration parameters that are important should be parsed and
        # saved in the constructor.
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.shared_folder = config['scratch']
        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)
        self.hr = htmlreportutils()
        self.sw_url = config['srv-wiz-url']


    def get_jbrowse_url(self):
        '''
        get the most recent jbrowserserver url from the service wizard.
        sw_url: service wizard url
        '''
        # TODO Fix the following dev thing to beta or release or future
        json_obj = {
            "method": "ServiceWizard.get_service_status",
            "id": "",
            "params": [{"module_name": "JbrowseServer", "version": "dev"}]
        }
        sw_resp = requests.post(url=self.sw_url, data=json.dumps(json_obj))

        #print (sw_resp)
        vfs_resp = sw_resp.json()
        #print (vfs_resp)
        #jbrowse_url = vfs_resp['result'][0]['url'].replace(":443", "")
        jbrowse_url=vfs_resp['result'][0]['url']
        #jbrowse_url=""
        return jbrowse_url

        #END_CONSTRUCTOR

    def run_variation_jbrowse(self, ctx, params):
        """
        This example function accepts any number of parameters and returns results in a KBaseReport
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "ReportResults" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN run_variation_jbrowse

        # Print statements to stdout/stderr are captured and available as the App log
        logging.info('Starting run_variation_jbrowse function. Params=' + pformat(params))
        directory = str(uuid.uuid4())
        path = os.path.join("/kb/module/work/tmp", directory)
        os.mkdir(path)
        html_path = os.path.join(path, "index.html")


        #jbrowse_url="https://kbase.us:443/dynserv/a9c861fc01f6857a768f4316e585f4315c815ecf.JbrowseServer/jbrowse/"
        jbrowse_url= self.get_jbrowse_url()
        jbrowse_url +="/jbrowse/"
        jbrowse_url += str(params['variation_ref'])
        jbrowse_url += "/index.html"

        jbrowse_iframe="<iframe width=95%% height=95% src='"
        jbrowse_iframe += jbrowse_url
        jbrowse_iframe += "'</>"
        with open(html_path, "w") as f:
            f.write("<html><body>")
            f.write(jbrowse_iframe)
            f.write("</body></html>")
        output = self.hr.create_html_report(path, params['workspace_name'])
        #output={}
        print(output)
        #END run_variation_jbrowse

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method run_variation_jbrowse return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
