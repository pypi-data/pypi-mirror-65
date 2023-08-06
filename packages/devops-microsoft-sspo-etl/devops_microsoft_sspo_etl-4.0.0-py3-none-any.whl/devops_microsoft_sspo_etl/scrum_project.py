
from tfs.tfs import TFS
from .base_entity import BaseEntity
from devops_microsoft_mapping_sspo import factories 
import logging
logging.basicConfig(level=logging.INFO)

class ScrumProject(BaseEntity):
    
    def do(self,data):
        try:
            logging.info("Project")
            self.config(data)
            projects = self.tfs.get_projects()
            
            if projects is None:
                logging.info ("Project None")
                return None
            
            for tfs_project in projects:
                
                teams = self.tfs.get_teams(tfs_project.id)
                logging.info ("Creating a Scrum Complex Project:"+tfs_project.id)
                scrum_project_application = None
                
                if (len(teams) > 1):
                    logging.info ("Creating a Scrum Complex Project")
                    scrum_project_application = factories.ScrumComplexProjectFactory(organization=self.organization, configuration=self.configuration)
                else:
                    logging.info ("Creating a Scrum Atomic Project")
                    scrum_project_application = factories.ScrumAtomicProjectFactory(organization=self.organization, configuration=self.configuration)
                    
                scrum_project_application.create(tfs_project,self.organization)    
                    
                logging.info ("Scrum Project's Application Reference Created")
        except Exception as e: 
            logging.error("OS error: {0}".format(e))
            logging.error(e.__dict__)  
        