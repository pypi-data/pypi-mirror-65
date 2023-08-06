from .scrum_project import ScrumProject
from sspo_db.application import factories as application_factories
from sspo_db.model import factories as model_factories
import logging
logging.basicConfig(level=logging.INFO)

class ScrumComplexProject(ScrumProject):

    def __init__(self, organization, configuration):
        super().__init__(organization, configuration)

    def create(self, element, organization):
        try:
            logging.info("Scrum Complex Project: Start")
            self.element = element
            self.organization = organization
            self.scrum_project = model_factories.ScrumComplexProjectFactory()
            self.scrum_project_application = application_factories.ScrumComplexProjectFactory()
            
            super().create()
            logging.info("Scrum Complex Project: End")
            return self.scrum_project
        except Exception as e: 
            logging.error("OS error: {0}".format(e))
            logging.error(e.__dict__)