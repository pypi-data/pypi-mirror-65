from .user_story import UserStory
from sspo_db.application import factories as application_factories
from sspo_db.model import factories as model_factories
import logging
logging.basicConfig(level=logging.INFO)
import re  

class AtomicUserStory(UserStory):

    def __init__(self, organization, configuration):
        super().__init__(organization, configuration)

    def create(self, element):
        try:
            logging.info("User Story: Create Atomic User Story")
            self.element = element
            self.scrum_element = model_factories.AtomicUserStoryFactory()
            self.scrum_element_application = application_factories.AtomicUserStoryFactory()
            
            super().create()
            logging.info("User Story: End")
            return self.scrum_element
            
        except Exception as e: 
            logging.error("OS error: {0}".format(e))
            logging.error(e.__dict__)
    
    def update(self, element):
        try:
            logging.info("User Story: Upate Atomic User Story")
            self.element = element
            self.scrum_element_application = application_factories.AtomicUserStoryFactory()
            self.scrum_element = self.scrum_element_application.retrive_by_external_uuid(element.id)
            super().update()

        except Exception as e: 
            logging.error("OS error: {0}".format(e))
            logging.error(e.__dict__)
    
    def delete(self, id):
        try:
            logging.info("User Story: Create Atomic User Story")
            self.scrum_element_application = application_factories.AtomicUserStoryFactory()
            #self.scrum_element = self.scrum_element_application.find(id, configuration_id)
            #super().delete()

        except Exception as e: 
            logging.error("OS error: {0}".format(e))
            logging.error(e.__dict__)
