from .user_story_abastract import UserStoryAbstract
from devops_microsoft_mapping_sspo import factories 
import logging
logging.basicConfig(level=logging.INFO)
import re  

class UserStory(UserStoryAbstract):

    def do(self,data):
        try:
            
            self.config(data)
            logging.info("User Story")
            logging.info("User Story: Retrive information from TFS")
            work_itens = self.tfs.get_work_item_query_by_wiql_epic_user_story_product_backlog_item()

            for work_item in work_itens:

                element = self.tfs.get_work_item(work_item.id, None,None, "All")

                if element.fields['System.WorkItemType'] == "User Story" or element.fields['System.WorkItemType'] =="Product Backlog Item":
                    logging.info("User Story: Create User Story")
                    atomic_user_story_mapping = factories.AtomicUserStoryFactory(organization=self.organization, configuration=self.configuration)
                    atomic_user_story_mapping.create(element)
               
                elif element.fields['System.WorkItemType'] == "Epic":
                    logging.info("User Story: Epic")
                    
                    epic_mapping = factories.EpicFactory(organization=self.organization, configuration=self.configuration)
                    epic_mapping.create(element)
                    
        except Exception as e: 
            logging.error("OS error: {0}".format(e))
            logging.error(e.__dict__)              
    