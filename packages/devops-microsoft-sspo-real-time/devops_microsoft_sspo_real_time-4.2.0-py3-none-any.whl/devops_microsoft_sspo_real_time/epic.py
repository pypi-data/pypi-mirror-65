import logging
from .base_entity import BaseEntity
from devops_microsoft_mapping_sspo import factories 
logging.basicConfig(level=logging.INFO)
from datetime import datetime

class Epic(BaseEntity):

    def do(self,data):

        try:
            logging.info("Atomic User Story Task:Start")
            logging.info("Atomic User Story Task:Retrive Information about Atomic User Story")
            self.config(data)
            
            content = data["content"]
            id = content['id']
            event_type = content['eventType']
            
            work_item = self.tfs.get_work_item(str(id),None,None, "All")

            if event_type == "workitem.created":
                self.__create(work_item)
            elif event_type == "workitem.updated":
                self.__update(work_item)
            else: 
                self.__delete(work_item)

            logging.info("Scrum Development Task:End")
            
        except Exception as e: 
            logging.error("OS error: {0}".format(e))
            logging.error(e.__dict__)  

    def __create(self, work_item):
        logging.info("Scrum Development Task: Creating")

        epic_mapping = factories.EpicFactory(organization=self.organization,configuration=self.configuration)
        epic_mapping.create(work_item)
        
        logging.info("Scrum Development Task: Created")
    
    def __update(self, work_item):
        logging.info("Scrum Development Task: Update")
        epic_mapping = factories.EpicFactory(organization=self.organization,configuration=self.configuration)
        epic_mapping.update(work_item)
    
    def __delete(self, work_item):
        logging.info("Scrum Development Task: Delete")

   