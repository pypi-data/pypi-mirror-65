
from tfs.tfs import TFS
from .base_entity import BaseEntity
from pprint import pprint

from sspo_db.application import factories as application_factories
import logging
logging.basicConfig(level=logging.INFO)

class ScrumProject(BaseEntity):
    
    def do(self,data):
        try:

            logging.info("Scrum Project: Start")
            self.config(data)
            
            content = data["content"]
            project_id = content['resourceContainers']['project']['id']
            
            #verificar se o projeto existe em SEON
            scrum_atomic_project_application = application_factories.ScrumAtomicProjectFactory()
            scrum_complex_project_application = application_factories.ScrumComplexProjectFactory()
            
            logging.info("Scrum Project: Searching Project ID: "+str(project_id))
            scrum_atomic_project  = scrum_atomic_project_application.retrive_by_external_uuid(project_id)
            scrum_complex_project = scrum_complex_project_application.retrive_by_external_uuid(project_id)

            if scrum_atomic_project is None and scrum_complex_project is None:
                self.__create(project_id)
            else:
                if scrum_atomic_project:
                    logging.info("Scrum Project: Scrum Atomic Project found:"+scrum_atomic_project.name)    
                else:
                    logging.info("Scrum Project: Scrum Complex Project found:"+scrum_complex_project.name)    
            
            logging.info("Scrum Project: End")
            
        except Exception as e: 
            logging.error("OS error: {0}".format(e))
            logging.error(e.__dict__)  
        
    def __create(self, project_id):
        logging.info("Scrum Project: Não Existe")
        logging.info("Scrum Project: é necessário tudo?")