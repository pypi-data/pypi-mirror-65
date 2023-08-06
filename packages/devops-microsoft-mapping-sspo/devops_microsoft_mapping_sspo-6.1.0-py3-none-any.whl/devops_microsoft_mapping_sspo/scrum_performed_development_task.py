import logging
from .base_scrum_element import BaseScrumElement
from sspo_db.application import factories as application_factories
from sspo_db.model import factories as model_factories
logging.basicConfig(level=logging.INFO)
from datetime import datetime

class ScrumPerformedDevelopmentTask(BaseScrumElement):

    def __init__(self, organization, configuration):
        super().__init__(organization, configuration)

    def create (self, element, scrum_intented_development_task):
        try:
            self.element = element
            self.scrum_element = model_factories.ScrumPerformedDevelopmentTaskFactory()
            self.scrum_element_application = application_factories.ScrumPerformedDevelopmentTaskFactory()

            logging.info('Performed Task:Performed Task assigned with Intented')
            self.scrum_element.caused_by = scrum_intented_development_task.id
            
            logging.info('Performed Task: Calling scrum development task function')            
            super().create()
            
            logging.info('Performed Task:Persiting performed task')
            self.scrum_element_application.create(self.scrum_element)

            return self.scrum_element
        except Exception as e: 
            logging.error("OS error: {0}".format(e))
            logging.error(e.__dict__)   
    
    def update(self,element,scrum_intented_development_task):
        try:
            self.element = element
            self.scrum_element_application = application_factories.ScrumPerformedDevelopmentTaskFactory()
            self.scrum_element = self.scrum_element_application.retrive_by_external_uuid(element.id)

            logging.info('Performed Task:Performed Task assigned with Intented')
            self.scrum_element.caused_by = scrum_intented_development_task.id
            
            logging.info('Performed Task: Calling scrum development task function')            
            super().update()
            
            logging.info('Performed Task:Persiting performed task')
            self.scrum_element_application.update(self.scrum_element)

            return self.scrum_element

        except Exception as e: 
            logging.error("OS error: {0}".format(e))
            logging.error(e.__dict__)   
        

