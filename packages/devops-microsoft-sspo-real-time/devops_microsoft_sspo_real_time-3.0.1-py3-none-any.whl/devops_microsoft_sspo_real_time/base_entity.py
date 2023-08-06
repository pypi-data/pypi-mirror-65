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
        
        # CONSTANTES    
        self.EPIC = "epic"
        self.PERFORMED_DEVELOPED_TASK = "scrum_performed_development_task"
        self.INTENDED_DEVELOPED_TASK = "scrum_intented_development_task"
        self.PROJECT_TFS = "project"
        self.TEAM_TFS = "team"
        self.TEAM_MEMBER_TFS = "individual"
        self.SPRINT_TFS =  "interaction"
        self.WORK_ITEM = "work_item"

        self.data = data

        self.organization_id = self.data['organization_id']
        self.tfs_key = self.data['tfs_key']
        self.tfs_url = self.data['tfs_url']
        self.application = self.data['application']
        self.retrive_tfs()
        
        self.application_service = application_factories.ApplicationFactory()
        self.application_organization = application_factories.OrganizationFactory()
        
        self.organization = self.application_organization.get_by_uuid(self.organization_id)
        self.application = self.application_service.get_by_uuid(self.application)
    
    def retrive_tfs(self):
        self.tfs =  TFS(self.tfs_key, self.tfs_url) 
        
    def create_application_reference(self,external_id, external_url,external_type_entity, internal_uuid, entity_name ):
        #application reference
        application_reference = model_factories.ApplicationReferenceFactory(
                                                    name = None,
                                                    description = None,
                                                    application = self.application.id,
                                                    external_id = external_id,
                                                    external_url = external_url,
                                                    external_type_entity = external_type_entity,
                                                    internal_uuid = internal_uuid,
                                                    entity_name = entity_name
                                                )

        self.application_application_reference.create(application_reference)