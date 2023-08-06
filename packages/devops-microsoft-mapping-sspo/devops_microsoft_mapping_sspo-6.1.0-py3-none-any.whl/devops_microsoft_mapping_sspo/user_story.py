from .base_entity import BaseEntity
from sspo_db.application import factories as application_factories
from sspo_db.model import factories as model_factories
from datetime import datetime
from .base_scrum_element import BaseScrumElement
import logging
logging.basicConfig(level=logging.INFO)
import re  
class UserStory(BaseScrumElement):
    
    def __init__(self, organization, configuration):
        super().__init__(organization, configuration)

    def create(self):
        try:
            logging.info("User Story")

            logging.info("User Story: add name and description")
            self.set_name_description()
            
            logging.info("User Story: add dates")
            #recuperando as datas    
            self.retrive_dates()

            story_points = self.check_value(self.element,'Microsoft.VSTS.Scheduling.StoryPoints')
            logging.info('User Story: Story Point: '+str(story_points))

            if story_points is not None: 
                self.scrum_element.story_points  = story_points

            logging.info("User Story: project name")
            #Adicionando o EPIC o backlog
            project_name = self.retrive_project_name()
            
            logging.info("User Story: retrive Product Backlog: "+project_name)
            product_backlog = self.retrive_product_backlog(project_name)

            # Product Backlog 
            logging.info("User Story: add Product Backlog :"+str(product_backlog.id))
            
            self.scrum_element.product_backlog = product_backlog.id

            logging.info("User Story: Retrive Team Members")
            self.retrive_team_members()

            logging.info("User Story: create Seon Element")
            self.scrum_element_application.create(self.scrum_element)
            
            logging.info("User Story: Create reference")
            self.create_application_reference(self.element.id, self.element.url, self.WORK_ITEM,self.scrum_element.uuid, self.scrum_element.__tablename__)
                                        
        except Exception as e: 
            logging.error("OS error: {0}".format(e))
            logging.error(e.__dict__)
    
    def update(self):
        try:
            logging.info("User Story: Update")

            logging.info("User Story: Update: add name and description")
            self.set_name_description()
            
            logging.info("User Story: Update: add dates")
            #recuperando as datas    
            self.retrive_dates()

            story_points = self.check_value(self.element,'Microsoft.VSTS.Scheduling.StoryPoints')
            logging.info('User Story: Update: Story Point: '+str(story_points))

            if story_points is not None: 
                self.scrum_element.story_points  = story_points

            logging.info("User Story: Update: project name")
            #Adicionando o EPIC o backlog
            project_name = self.retrive_project_name()
            
            logging.info("User Story: Update: retrive Product Backlog: "+project_name)
            product_backlog = self.retrive_product_backlog(project_name)

            # Product Backlog 
            logging.info("User Story: Update: add Product Backlog :"+str(product_backlog.id))
            
            self.scrum_element.product_backlog = product_backlog.id

            logging.info("User Story: Update: Retrive Team Members")
            self.retrive_team_members()

            logging.info("User Story: create Seon Element")
            self.scrum_element_application.update(self.scrum_element)
            
        except Exception as e: 
            logging.error("OS error: {0}".format(e))
            logging.error(e.__dict__)
    