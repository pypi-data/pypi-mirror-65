from .base_entity import BaseEntity
from sspo_db.application import factories as application_factories
from sspo_db.model import factories as model_factories
import logging
logging.basicConfig(level=logging.INFO)

class ScrumTeam(BaseEntity):
    
    def __init__(self, organization, configuration):
        super().__init__(organization, configuration)
        self.application = application_factories.ScrumTeamFactory()

    def create(self, element,scrum_project, organization):
        try:
            logging.info("Scrum Team: Creating")
            
            scrum_team = model_factories.ScrumTeamFactory(name = element.name, 
                                                                        description = element.description, 
                                                                        scrum_project= scrum_project.id,
                                                                        organization = organization)
            
            
            self.application.create(scrum_team)
            
            return scrum_team
            
        except Exception as e: 
            logging.error("OS error: {0}".format(e))
            logging.error(e.__dict__)   





            