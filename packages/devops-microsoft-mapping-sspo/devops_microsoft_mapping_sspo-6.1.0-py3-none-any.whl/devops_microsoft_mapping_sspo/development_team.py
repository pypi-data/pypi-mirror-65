from .base_entity import BaseEntity
from sspo_db.application import factories as application_factories
from sspo_db.model import factories as model_factories
import logging
class DevelopmentTeam(BaseEntity):

    def __init__(self, organization, configuration):
        super().__init__(organization, configuration)
        
        self.application = application_factories.DevelopmentTeamFactory()

    def create(self, element,scrum_team):
        try:
            logging.info("Scrum Development Team: Creating")
            
            development_team = model_factories.DevelopmentTeamFactory(name = element.name, 
                                                                        description = element.description, 
                                                                        scrum_team_id = scrum_team.id)
            
            
            self.application.create(development_team)
            
            return development_team
            
        except Exception as e: 
            logging.error("OS error: {0}".format(e))
            logging.error(e.__dict__)   
