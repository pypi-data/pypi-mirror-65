from .base_entity import BaseEntity
import logging

from devops_microsoft_mapping_sspo import factories 
from sspo_db.application import factories as application_factories
from sspo_db.model import factories as model_factories

logging.basicConfig(level=logging.INFO)
class Sprint(BaseEntity):
    
    def do(self,data):
        try:

            self.config(data)
            logging.info("Interaction")

            self.application_sprint =  application_factories.SprintFactory()
            application_scrum_atomic = application_factories.ScrumAtomicProjectFactory()
            application_sprint_backlog = application_factories.SprintBacklogFactory()

            sprint_mapping = factories.SprintFactory(organization=self.organization, configuration=self.configuration)

            # Buscando os projetos do TFS
            projects = self.tfs.get_projects()
            
            for project in projects:
                
                atomic = True
                teams = self.tfs.get_teams(project.id)
                
                if len(teams) > 1:
                    atomic = False
                
                for team in teams: 

                    interactions = self.tfs.get_interactions(project,team)
                    project_id = team.id 
                    
                    if atomic: 
                        project_id = project.id

                    atomic_project = application_scrum_atomic.retrive_by_external_uuid(project_id)
                    scrum_process = atomic_project.scrum_process

                    sprint = model_factories.SprintFactory(name = "Limbo", description = "Limbo", scrum_process = scrum_process )
                    
                    self.application_sprint.create(sprint)
                    
                    sprint_backlog = model_factories.SprintBacklogFactory()
                    sprint_backlog.sprint = sprint.id
                    sprint_backlog.name = sprint.name
                    sprint_backlog.description = sprint.description
                    application_sprint_backlog.create(sprint_backlog)
                        
                    for interaction in interactions:
                    
                        logging.info("Interaction: Creating interaction")
                        
                        sprint_mapping.create(interaction,scrum_process)

        except Exception as e: 
            logging.error("OS error: {0}".format(e))
            logging.error(e.__dict__)  



                    