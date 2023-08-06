from .base_entity import BaseEntity
from sspo_db.application import factories as application_factories
from sspo_db.model import factories as model_factories
import logging
logging.basicConfig(level=logging.INFO)

class ScrumProcess(BaseEntity):
    
    def __init__(self, organization, configuration):
        super().__init__(organization, configuration)
        self.application_scrum_process = application_factories.ScrumProcessFactory()

    def create(self, element,scrum_process):
        try:
            logging.info("Scrum Process: Creating scrum process")
            
            scrum_process = model_factories.ScrumProcessFactory(name=element.name, 
                        description=element.description, 
                        scrum_project = scrum_process)

            self.application_scrum_process.create(scrum_process)
            return scrum_process
            
        except Exception as e: 
            logging.error("OS error: {0}".format(e))
            logging.error(e.__dict__)   
    
