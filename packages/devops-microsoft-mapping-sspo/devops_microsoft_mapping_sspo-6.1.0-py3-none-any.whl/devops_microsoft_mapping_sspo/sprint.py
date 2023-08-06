from .base_entity import BaseEntity
from sspo_db.application import factories as application_factories
from sspo_db.model import factories as model_factories
import logging
logging.basicConfig(level=logging.INFO)

class Sprint(BaseEntity):

    def __init__(self, organization, configuration):
        super().__init__(organization, configuration)

        self.application_sprint = application_factories.SprintFactory()
        self.application_sprint_backlog = application_factories.SprintBacklogFactory()

    def create(self, element,scrum_process):
        try:
            logging.info("Interaction: Creating interaction")
                        
            name = element.name
            interaction_id = element.id
            finish = element.attributes.finish_date 
            start = element.attributes.start_date 
                        
            sprint = model_factories.SprintFactory(name = name, 
                description =name, 
                scrum_process = scrum_process,
                startDate = start,
                endDate = finish
            )
                    
            self.application_sprint.create(sprint)

            self.create_application_reference(
                element.id,
                element.url,
                self.SPRINT_TFS,
                sprint.uuid,
                sprint.__tablename__)

            logging.info("Interaction: Sprint Backlog")
                        
            sprint_backlog = model_factories.SprintBacklogFactory(
                    name = sprint.name,
                    description = sprint.description,
                    sprint = sprint.id
            )
                        
            self.application_sprint_backlog.create(sprint_backlog)
            
            return sprint
            
        except Exception as e: 
            logging.error("OS error: {0}".format(e))
            logging.error(e.__dict__)