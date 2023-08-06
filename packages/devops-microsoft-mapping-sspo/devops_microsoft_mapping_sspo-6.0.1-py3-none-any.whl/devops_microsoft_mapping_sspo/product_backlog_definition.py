from .base_entity import BaseEntity
from sspo_db.application import factories as application_factories
from sspo_db.model import factories as model_factories
import logging
logging.basicConfig(level=logging.INFO)

class ProductBacklogDefinition(BaseEntity):
    
    def __init__(self, organization, configuration):
        super().__init__(organization, configuration)
        self.application = application_factories.ProductBacklogDefinitionFactory()

    def create(self, element,scrum_process):
        try:
            logging.info("Product Backlog Process: Creating")
            
            product_backlog_definition = model_factories.ProductBacklogDefinitionFactory(name=element.name, 
                description=element.description, 
                scrum_process = scrum_process)
            
            self.application.create(product_backlog_definition)
            
            return product_backlog_definition
            
        except Exception as e: 
            logging.error("OS error: {0}".format(e))
            logging.error(e.__dict__)   
    
