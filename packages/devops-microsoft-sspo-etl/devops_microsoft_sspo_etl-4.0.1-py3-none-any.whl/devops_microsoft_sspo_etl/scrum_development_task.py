from .user_story_abastract import UserStoryAbstract

from devops_microsoft_mapping_sspo import factories 
from pprint import pprint
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)

class ScrumDevelopmentTask(UserStoryAbstract):

    def do(self,data):
        try:
            logging.info("Task")
            self.config(data)
            
            # Buscando os projetos do TFS
            work_itens = self.tfs.get_work_item_query_by_wiql_task()

            logging.info("Buscando Task")
            for work_item in work_itens:
                element = self.tfs.get_work_item(work_item.id, None,None, "All")
                
                if element.fields['System.WorkItemType'] == "Task":   
                    state = str(self.check_value(element,'System.State'))
                    
                    if state == "New" or state =="To Do":
                        logging.info("Buscando Task: Criando intented")
                        scrum_intented_mapping = factories.ScrumIntentedDevelopmentTaskFactory(organization=self.organization, configuration=self.configuration)
                        scrum_intented_mapping.create(element)
                    else:
                        logging.info("Buscando Task: Criando Performed")
                        scrum_intented_mapping = factories.ScrumIntentedDevelopmentTaskFactory(organization=self.organization, configuration=self.configuration)
                        scrum_intented_development_task = scrum_intented_mapping.create(element)

                        scrum_performed_mapping = factories.ScrumPerformedDevelopmentTaskFactory(organization=self.organization,configuration=self.configuration)
                        scrum_performed_mapping.create(element,scrum_intented_development_task)

        except Exception as e: 
            logging.error("OS error: {0}".format(e))
            logging.error(e.__dict__)    
    