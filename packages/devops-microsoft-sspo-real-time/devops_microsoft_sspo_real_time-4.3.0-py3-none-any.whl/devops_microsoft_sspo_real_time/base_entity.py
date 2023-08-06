from sspo_db.application import factories as application_factories
from sspo_db.model import factories as model_factories
import re
from pprint import pprint
from tfs.tfs import TFS
import logging
logging.basicConfig(level=logging.INFO)

class BaseEntity():

    def __init__(self):
        
        self.organization = None
        
    def config (self, data):

        self.data = data

        self.organization_uuid = data['organization_uuid']
        self.configuration_uuid = self.data['configuration_uuid']
        
        self.tfs_key = data['secret']
        self.tfs_url = data['url']
        
        self.retrive_tfs()
        
        self.application_configuration = application_factories.ConfigurationFactory()
        self.application_organization = application_factories.OrganizationFactory()
        
        self.organization = self.application_organization.get_by_uuid(self.organization_uuid)
        self.configuration = self.application_configuration.get_by_uuid(self.configuration_uuid)
    
    def retrive_tfs(self):
        self.tfs =  TFS(self.tfs_key, self.tfs_url) 
    