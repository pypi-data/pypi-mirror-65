from .base_entity import BaseEntity
from sspo_db.application import factories as application_factories
from sspo_db.model import factories as model_factories
import logging
logging.basicConfig(level=logging.INFO)

class ProductBacklog(BaseEntity):

    def __init__(self, organization, configuration):
        super().__init__(organization, configuration)
        
        self.application = application_factories.ProductBacklogFactory()


    def create(self, element,product_backlog_definition):
        try:
            logging.info("Creating a product backlog")   
            
            product_backlog = model_factories.ProductBacklogFactory(name=element.name, 
                description=element.description, 
                product_backlog_definition = product_backlog_definition.id)
            
            self.application.create(product_backlog)
            
            return product_backlog
            
        except Exception as e: 
            logging.error("OS error: {0}".format(e))
            logging.error(e.__dict__)

            