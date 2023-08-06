import logging
from .base_scrum_element import BaseScrumElement
from sspo_db.application import factories as application_factories
from sspo_db.model import factories as model_factories
logging.basicConfig(level=logging.INFO)
from datetime import datetime

class ScrumIntentedDevelopmentTask(BaseScrumElement):

    def __init__(self, organization, configuration):
        super().__init__(organization, configuration)

    def update(self, element):
        try:
            logging.info('Intented Task: Updating Intended Task')
            self.element = element
            self.scrum_element_application = application_factories.ScrumIntentedDevelopmentTaskFactory()
            self.scrum_element = self.scrum_element_application.retrive_by_external_uuid(element.id)
            super().update()

            self.__product_backlog()
            self.__story_points()
            self.__created_date()
            self.__activity()
            self.__define_priority()
            
            logging.info('Updating intented task')
            self.scrum_element_application.update(self.scrum_element)
            logging.info('Updating Task persited')
            
            return self.scrum_element

            return self.scrum_element
        except Exception as e: 
            logging.error("OS error: {0}".format(e))
            logging.error(e.__dict__)

    def create(self, element):
        try:
            logging.info('Intented Task: Creating Intended Task')
            
            self.element = element
            self.scrum_element = model_factories.ScrumIntentedDevelopmentTaskFactory()
            self.scrum_element_application = application_factories.ScrumIntentedDevelopmentTaskFactory()
            self.application_development_task_type = application_factories.DevelopmentTaskTypeFactory()
            self.application_priority = application_factories.PriorityFactory()
            
            logging.info('Intented Task: Calling scrum development task function')
            super().create()
            
            self.__product_backlog()
            self.__story_points()
            self.__created_date()
            self.__activity()
            self.__define_priority()
            
            logging.info('Persisting intented task')
            self.scrum_element_application.create(self.scrum_element)
            logging.info('Intented Task persited')
            
            return self.scrum_element
    
        except Exception as e: 
            logging.error("OS error: {0}".format(e))
            logging.error(e.__dict__)
    
    def __define_priority (self):
        try:
            priority = self.check_value(self.element,'Microsoft.VSTS.Common.Priority')
            if priority is not None and priority is not 'None':    
                Priority = model_factories.PriorityFactory()
                level = None
                if priority == 1:
                    level = Priority.normal
                elif priority == 2 or priority == 3:
                    level = Priority.medium
                else:
                    level = Priority.high
                
                logging.info('Intented Task: searching priority')
                priority = self.application_priority.retrive_by_name(level)
                self.scrum_element.priority = priority.id
                logging.info('Intented Task: Priority: '+str(priority.name))
            
        except Exception as e: 
            logging.error("OS error: {0}".format(e))
            logging.error(e.__dict__)   
            
    def __product_backlog(self):
        try:
            project_name = self.retrive_project_name()
            product_backlog = self.retrive_product_backlog(project_name)

            # Product Backlog 
            logging.info('Intented Task: Product Backlog')
            if product_backlog is not None:
                self.scrum_element.product_backlog = product_backlog.id
            else:
                logging.error('Intented Task: Product Backlog: None')
            
        except Exception as e: 
            logging.error("OS error: {0}".format(e))
            logging.error(e.__dict__)  
    
    def __story_points(self):
        try:
            story_points = self.check_value(self.element,'Microsoft.VSTS.Scheduling.StoryPoints')
            logging.info('Intented Task: Story Point: '+str(story_points))

            if story_points is not None: 
                self.scrum_element.story_points  = story_points

        except Exception as e: 
            logging.error("OS error: {0}".format(e))
            logging.error(e.__dict__)  

    def __created_date(self):
        try:
        
            logging.info('Intented Task: Dates')
            created_data = self.check_value(self.element,'System.CreatedDate')
            if created_data is not None and created_data is not 'None':
                self.scrum_element.created_date = self.validate_date_format(str(created_data)) 
        
        except Exception as e: 
            logging.error("OS error: {0}".format(e))
            logging.error(e.__dict__)   
    
    def __activity(self):
        try:
            activity  = self.check_value(self.element,'Microsoft.VSTS.Common.Activity')
            logging.info('Intented Task: Activity: '+str(activity))

            if activity is not None and activity is not 'None':
                logging.info('Intented Task: Type Activity')
                type_activity = self.application_development_task_type.retrive_by_name(activity.lower())
                self.scrum_element.type_activity = type_activity.id
        
        except Exception as e: 
            logging.error("OS error: {0}".format(e))
            logging.error(e.__dict__)  
