import logging
from .base_entity import BaseEntity
from sspo_db.application import factories as application_factories
from sspo_db.model import factories as model_factories
logging.basicConfig(level=logging.INFO)
from datetime import datetime

class BaseScrumElement(BaseEntity):

    def __init__(self, organization, configuration):
        super().__init__(organization, configuration)
        
        self.scrum_element = None
        self.scrum_element_application = None
        self.element = None
        self.application_person = application_factories.PersonFactory()
        self.application_team_member = application_factories.TeamMemberFactory()
        self.application_sprint = application_factories.SprintFactory()
        self.application_sprint_backlog = application_factories.SprintBacklogFactory()
        
        self.application_developer = application_factories.DeveloperFactory()
        self.application_atomic_user_story = application_factories.AtomicUserStoryFactory()
        self.application_product_backlog = application_factories.ProductBacklogFactory()


    def update(self):
        try:
            self.set_name_description()
            logging.info('Scrum development Task: Update Name and Description: '+self.scrum_element.name)
            self.retrive_team_members()
            self.retrive_sprint()
            self.create_relations()  
            
        except Exception as e: 
            logging.error("OS error: {0}".format(e))
            logging.error(e.__dict__)


    def create(self):
        try:
            self.set_name_description()
            logging.info('Scrum development Task: Name and Description: '+self.scrum_element.name)
            self.retrive_team_members()
            self.retrive_sprint()
            self.create_relations()  
            logging.info("User Story: Create reference")
            self.create_application_reference(self.element.id, self.element.url, self.WORK_ITEM,self.scrum_element.uuid, self.scrum_element.__tablename__)
            
        except Exception as e: 
            logging.error("OS error: {0}".format(e))
            logging.error(e.__dict__)

    def set_name_description(self):
        self.scrum_element.name = self.element.fields['System.Title']
        self.scrum_element.description = str(self.check_value(self.element,'System.Description'))

    def retrive_project_name(self):
        
        project_name = self.check_value(self.element,"System.AreaLevel2") 
        if project_name is None:
            project_name = self.check_value(self.element,"System.AreaLevel1") 
        return project_name

    def retrive_team_members(self):
        try:
            created_by = self.check_value(self.element,'System.CreatedBy')
            activated_by = self.check_value(self.element,'Microsoft.VSTS.Common.ActivatedBy') 
            closed_by = self.check_value(self.element,'Microsoft.VSTS.Common.ClosedBy') 
            assigned_by = self.check_value(self.element,'System.AssignedTo')

            project_name = self.retrive_project_name()

            if created_by is not None and created_by is not 'None':
                team_member = self.retrive_team_member_seon(created_by,project_name)
                self.scrum_element.created_by = team_member.id
                            
            if activated_by is not None and activated_by is not 'None':
                team_member = self.retrive_team_member_seon(activated_by,project_name)
                self.scrum_element.activated_by = team_member.id
            
            if closed_by is not None and closed_by is not 'None':
                team_member = self.retrive_team_member_seon(closed_by,project_name)
                self.scrum_element.closed_by = team_member.id
            
            if assigned_by is not None and assigned_by is not 'None':
                logging.info("Assigned: "+assigned_by['id'])
                team_member = self.retrive_team_member_seon(assigned_by,project_name)
                if team_member is not None:
                    if  self.scrum_element.assigned_by is None:
                        self.scrum_element.assigned_by = [team_member]
                    else: 
                        self.scrum_element.assigned_by.append(team_member)
        
        except Exception as e: 
            logging.error("OS error: {0}".format(e))
            logging.error(e.__dict__)              
        
    def retrive_product_backlog(self, project_name):
        product_backlog = self.application_product_backlog.retrive_by_project_name(project_name)
        return product_backlog    

    def validate_date_format(self, date):

        try:
            return datetime.strptime(str(date), '%Y-%m-%dT%H:%M:%S.%fZ')
        except ValueError:
            return datetime.strptime(str(date), '%Y-%m-%dT%H:%M:%SZ')

    def retrive_dates(self):

        created_data = self.check_value(self.element,'System.CreatedDate')
        activated_date = self.check_value(self.element,'Microsoft.VSTS.Common.ActivatedDate')
        resolved_date = self.check_value(self.element,'Microsoft.VSTS.Common.ResolvedDate')
        closed_date = self.check_value(self.element,'Microsoft.VSTS.Common.ClosedDate')

        if created_data is not None and created_data is not 'None':
            self.scrum_element.created_date = self.validate_date_format(str(created_data)) 
                            
        if activated_date is not None and activated_date is not 'None':
            self.scrum_element.activated_date = self.validate_date_format(str(activated_date))
                    
        if resolved_date is not None and resolved_date is not 'None':
            self.scrum_element.resolved_date = self.validate_date_format(str(resolved_date)) 
                    
        if closed_date is not None and closed_date is not 'None':
            self.scrum_element.closed_date = self.validate_date_format(str(closed_date))
        
    def retrive_sprint(self):
        try:
            project_name = self.retrive_project_name()
            logging.info('Scrum development: Sprint')
            project_name = project_name.strip()

            sprint_name = self.check_value(self.element,"System.IterationLevel2") 
            
            logging.info('Scrum development: Sprint: '+str(sprint_name))

            if sprint_name is None:
                sprint_name = "limbo"
                logging.warning("LIMBO")
            else:
                sprint_name = sprint_name.strip()

            logging.info('Scrum development: Sprint Backlog')
            sprint_backlog = self.application_sprint_backlog.retrive_by_name_and_project_name(sprint_name,project_name)
            
            if sprint_backlog is not None:
                self.scrum_element.sprint_backlogs = [sprint_backlog]
            else:
                logging.error('Scrum development: Sprint Backlog: None')
            
            logging.info('Scrum development: retrive Sprint')
            sprints = self.application_sprint.retrive_by_name_and_project_name(sprint_name,project_name)
            if sprints is not None:
                self.scrum_element.sprints = [sprints]
            else:
                logging.error('Scrum development: retrive Sprint: NONE')
         
        except Exception as e: 
            logging.error("OS error: {0}".format(e))
            logging.error(e.__dict__)   

    def create_relations(self):
        try:
            relations = self.element.relations
            if relations is not None and relations is not 'None':
                for relation in relations:
                    relation_name = relation.attributes["name"] 
                    url = relation.url
                    
                    if relation_name == "Parent":
                        logging.info('Scrum development: Atomic User Story')
                        logging.info('Scrum development: Atomic User Story: '+ url)
                        
                        atomic_user_story = self.application_atomic_user_story.retrive_by_external_url(url)
                        
                        if atomic_user_story:
                            self.scrum_element.atomic_user_story = atomic_user_story.id
            
        except Exception as e: 
            logging.error("OS error: {0}".format(e))
            logging.error(e.__dict__)
   
    def validate_date_format(self, date):
        try:
            return datetime.strptime(str(date), '%Y-%m-%dT%H:%M:%S.%fZ')
        except ValueError:
            return datetime.strptime(str(date), '%Y-%m-%dT%H:%M:%SZ')
    