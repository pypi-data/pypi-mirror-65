
from tfs.tfs import TFS
from .base_entity import BaseEntity
from pprint import pprint

from sspo_db.application import factories as application_factories
from devops_microsoft_mapping_sspo import factories as mapping_factories
from sspo_db.model import factories as model_factories
import logging
logging.basicConfig(level=logging.INFO)

class ScrumProject(BaseEntity):
    
    def do(self,data):
        try:

            logging.info("Scrum Project: Start")
            self.config(data)
            
            content = data["content"]
            project_id = content['all']['resourceContainers']['project']['id']

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
        try:
            logging.info("Scrum Project: Não Existe")
            scrum_atomic_project_mapping = mapping_factories.ScrumAtomicProjectFactory(organization=self.organization,configuration=self.configuration)
            
            projects = self.tfs.get_projects()
            
            for project in projects: 
                if project.id == project_id:
                    element = project
                    break
            
            logging.info("Scrum Project: Criando o projeto e os processos iniciais")
            scrum_atomic_project = scrum_atomic_project_mapping.create(element, self.organization, None)
            
            logging.info("Scrum Project: Criando os Sprints")
            self.__create_sprint(scrum_atomic_project, element)
            
            logging.info("Scrum Project: Criando o Team Members")
            self.__create_team_member(scrum_atomic_project, element)
            
        except Exception as e: 
            logging.error("OS error: {0}".format(e))
            logging.error(e.__dict__)  
            
    def __create_sprint(self,scrum_atomic_project, msdevops_project):
        try:
            scrum_process = scrum_atomic_project.scrum_process

            sprint = model_factories.SprintFactory(name = "Limbo", description = "Limbo", scrum_process = scrum_process )
            application_sprint =  application_factories.SprintFactory()        
            application_sprint.create(sprint)
            
            application_sprint_backlog = application_factories.SprintBacklogFactory()
            
            sprint_backlog = model_factories.SprintBacklogFactory()
            sprint_backlog.sprint = sprint.id
            sprint_backlog.name = sprint.name
            sprint_backlog.description = sprint.description
            
            application_sprint_backlog.create(sprint_backlog)

            sprint_mapping = mapping_factories.SprintFactory(organization=self.organization, configuration=self.configuration)
            
            teams = self.tfs.get_teams(msdevops_project.id)

            for team in teams:
                interactions = self.tfs.get_interactions(msdevops_project,team)
                
                for interaction in interactions:
                    logging.info("Interaction: Creating interaction")
                        
                    sprint_mapping.create(interaction,scrum_process)

        except Exception as e: 
            logging.error("OS error: {0}".format(e))
            logging.error(e.__dict__)  
    
    def __create_team_member(self,scrum_atomic_project, msdevops_project):
        try:
            
            teams = self.tfs.get_teams(msdevops_project.id)
            
            team_member_mapping = mapping_factories.TeamMemberFactory( organization=self.organization, configuration=self.configuration)
            
            for team in teams:
                team_members = self.tfs.get_team_members(msdevops_project.id,team.id)
                logging.info("Team Member: retrive team member from " +team.name)
                    
                for team_member in team_members:
                    team_member_mapping.create(team_member, team)
                
            
        except Exception as e: 
            logging.error("OS error: {0}".format(e))
            logging.error(e.__dict__)  