from sspo_db.application import factories as application_factories
from sspo_db.model import factories as model_factories
import re
from pprint import pprint
import logging
logging.basicConfig(level=logging.INFO)

class BaseEntity():

    def __init__(self, organization, configuration):
        
        self.organization = organization
        self.configuration = configuration

        # CONSTANTES    
        self.EPIC = "epic"
        self.PERFORMED_DEVELOPED_TASK = "scrum_performed_development_task"
        self.INTENDED_DEVELOPED_TASK = "scrum_intented_development_task"
        self.PROJECT_TFS = "project"
        self.TEAM_TFS = "team"
        self.TEAM_MEMBER_TFS = "individual"
        self.SPRINT_TFS =  "interaction"
        self.WORK_ITEM = "work_item"
        
        self.application_application_reference = application_factories.ApplicationReferenceFactory()

    def check_value (self, work_item, key):
        return work_item.fields[key] if key in work_item.fields else None

    def create_application_reference(self,external_id, external_url,external_type_entity, internal_uuid, entity_name ):
        #application reference
        application_reference = model_factories.ApplicationReferenceFactory(
                                                    name = None,
                                                    description = None,
                                                    configuration = self.configuration.id,
                                                    external_id = external_id,
                                                    external_url = external_url,
                                                    external_type_entity = external_type_entity,
                                                    internal_uuid = internal_uuid,
                                                    entity_name = entity_name
                                                )

        self.application_application_reference.create(application_reference)
    
    #verificar se o projeto existe 
    def retrive_team_member_seon (self, team_member, project_name):
        try:
            id = team_member['id']
            
            person = self.application_person.retrive_by_external_uuid(id)
            
            if person is None:
                
                email = None
                            
                regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
                            
                if re.search(regex,team_member['uniqueName']): 

                    email = team_member['uniqueName']

                    person = model_factories.PersonFactory(name=team_member['displayName'],
                                                                    email=email,
                                                                    organization = self.organization)
                            
                    self.application_person.create (person)
                            
                    logging.info("Team Member: create a person's reference")

                    self.create_application_reference(team_member.identity.id,team_member.identity.url,self.TEAM_MEMBER_TFS,person.uuid,person.__tablename__)
                    
            team_member = self.application_team_member.retrive_by_external_id_and_project_name(id,project_name)

            if team_member is None:
                team_member = self.application_developer.create_with_project_name(id, project_name)
            return team_member
        except Exception as e: 
            pprint ("OS error: {0}".format(e))
            pprint (e.__dict__)
            logging.error("OS error: {0}".format(e))
            logging.error(e.__dict__)  
    
    
    