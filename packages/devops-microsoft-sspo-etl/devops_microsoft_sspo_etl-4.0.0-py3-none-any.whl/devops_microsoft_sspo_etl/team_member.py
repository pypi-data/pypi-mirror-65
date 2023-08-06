from .base_entity import BaseEntity
from devops_microsoft_mapping_sspo import factories 
import re  

import logging
logging.basicConfig(level=logging.INFO)

class TeamMember(BaseEntity):

    def do(self,data):

        try:
            logging.info("Team Member")

            self.config(data)
            
            projects = self.tfs.get_projects()
            team_member_mapping = factories.TeamMemberFactory( organization=self.organization, configuration=self.configuration)
            
            for project in projects:
                logging.info("Team Member: retrive teams from " +project.name)
                teams = self.tfs.get_teams(project.id)
                for team_tfs in teams:
                    
                    team_members = self.tfs.get_team_members(project.id,team_tfs.id)
                    logging.info("Team Member: retrive team member from " +team_tfs.name)
                    
                    for team_member in team_members:
                        team_member_mapping.create(team_member, team_tfs)
                       
        except Exception as e: 
            logging.error("OS error: {0}".format(e))
            logging.error(e.__dict__)              