from .base_entity import BaseEntity
import logging
logging.basicConfig(level=logging.INFO)
from devops_microsoft_mapping_sspo import factories 
from sspo_db.application import factories as application_factories
from pprint import pprint

class ScrumProjectTeam(BaseEntity):
    
    def do(self, data):
        try:
            self.config(data)
            
            self.application_complex_scrum_project = application_factories.ScrumComplexProjectFactory()
            logging.info("Project Team")
            
            projects = self.tfs.get_projects()

            for project in projects:
                
                logging.info("Getting Project Teams from: "+project.name)
                teams = self.tfs.get_teams(project.id)
                scrum_complex_project = self.application_complex_scrum_project.retrive_by_external_uuid(project.id)
                
                for team in teams:
                    #Verificando se o projeto é atomico
                    if scrum_complex_project is not None:
                        logging.info("Creating a scrum atomic project, scrum process and scrum team")   
                        #cria o projeto atomico e associa a um complexo
                        scrum_atomic_project_mapping = factories.ScrumAtomicProjectFactory(organization=self.organization, configuration=self.configuration)
                        scrum_atomic_project_mapping.create(team,self.organization,scrum_complex_project)
        
        except Exception as e: 
            logging.error("OS error: {0}".format(e))
            logging.error(e.__dict__)  
