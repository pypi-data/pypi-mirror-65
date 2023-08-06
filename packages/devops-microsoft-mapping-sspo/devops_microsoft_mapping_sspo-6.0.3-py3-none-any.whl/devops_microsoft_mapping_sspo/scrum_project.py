from .base_entity import BaseEntity
import logging
from sspo_db.application import factories as application_factories
logging.basicConfig(level=logging.INFO)

class ScrumProject(BaseEntity):

    def __init__(self, organization, configuration):

        super().__init__(organization, configuration)
        
        self.scrum_project = None
        self.scrum_project_application = None
        self.element = None
        self.organization = None

        self.application_scrum_process = application_factories.ScrumProcessFactory()
        self.application_product_backlog_definition = application_factories.ProductBacklogDefinitionFactory()
        self.application_product_backlog = application_factories.ProductBacklogFactory()
        
    def create(self):
        try:
            logging.info("Scrum Project: Information")
            
            self.scrum_project.name = self.element.name
            self.scrum_project.description = self.element.description
            self.scrum_project.organization = self.organization
            self.scrum_project_application.create(self.scrum_project)

            self.create_application_reference(
                    self.element.id, 
                    self.element.url,
                    self.PROJECT_TFS, 
                    self.scrum_project.uuid, 
                    self.scrum_project.type)
            
        except Exception as e: 
            logging.error("OS error: {0}".format(e))
            logging.error(e.__dict__) 

