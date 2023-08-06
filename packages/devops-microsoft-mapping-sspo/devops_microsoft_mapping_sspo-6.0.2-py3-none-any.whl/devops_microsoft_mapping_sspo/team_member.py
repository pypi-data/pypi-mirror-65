from .base_entity import BaseEntity
import logging
logging.basicConfig(level=logging.INFO)
from sspo_db.application import factories as application_factories
from sspo_db.model import factories as model_factories
import re  

class Teammember(BaseEntity):
    def __init__(self, organization, configuration):
        super().__init__(organization, configuration)
        
        self.application_person = application_factories.PersonFactory()
        self.application_scrum_team = application_factories.ScrumTeamFactory()
        self.application_scrum_master = application_factories.ScrumMasterFactory()
        self.application_development_team = application_factories.DevelopmentTeamFactory()
        self.application_developer = application_factories.DeveloperFactory()

    def create(self, team_member, team):
        try:
            person = self.application_person.retrive_by_external_uuid(team_member.identity.id)   
                            
            if person is None:
                person = self.create_person(team_member)
            
            scrum_team = self.application_scrum_team.retrive_by_external_uuid(team.id)  
            development_team = self.application_development_team.retrive_by_external_uuid(team.id)   
                        
            logging.info("Team Member: creating a team member")
            team_member_seon = None
            if team_member.is_team_admin:
                logging.info("Team Member: Scrum Master")
                team_member_seon = self.create_scrum_master(person,scrum_team)
            else:
                logging.info("Team Member: Developer")
                team_member_seon = self.create_developer(person, development_team)
            
            return team_member_seon
        
        except Exception as e: 
            logging.error("OS error: {0}".format(e))
            logging.error(e.__dict__)
        
    def create_person(self, team_member):
        try:
            logging.info("Team Member: create a person")
            email = None
            person = None                    
            regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
            #Verificando se o unique_name é um email                     
            if(re.search(regex,team_member.identity.unique_name)): 
                #verificar se o email existe
                person = self.application_person.get_by_email(team_member.identity.unique_name)
                if person is None:
                    person = self.__create_person(team_member)
            else:
                person = self.__create_person(team_member)
            
            return person 
                
        except Exception as e: 
            logging.error("OS error: {0}".format(e))
            logging.error(e.__dict__)
    
    def __create_person(self, team_member):
        
        try:

            email = None
            regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
            #Verificando se o unique_name é um email                     
            if(re.search(regex, team_member.identity.unique_name)): 
                email = team_member.identity.unique_name    
            
            person = model_factories.PersonFactory(name=team_member.identity.display_name,
                                                                        email=email,
                                                                        organization = self.organization)
                                
            self.application_person.create (person)
            logging.info("Team Member: create a person's reference")
            self.create_reference(person, team_member)
            return person
        
        except Exception as e: 
            logging.error("OS error: {0}".format(e))
            logging.error(e.__dict__)  

    def create_scrum_master(self, person, scrum_team):
        try:
            scrum_master = model_factories.ScrumMasterFactory(
                                name = person.name,
                                description = person.description,
                                person = person,
                                team = scrum_team,
                                team_role = ""
                            )
            self.application_scrum_master.create(scrum_master)
            return scrum_master
        except Exception as e: 
            logging.error("OS error: {0}".format(e))
            logging.error(e.__dict__)  
        
    def create_developer(self, person, development_team):
        try:
            developer = model_factories.DeveloperFactory(
                                name = person.name,
                                description = person.description,
                                person = person,
                                team = development_team,
                                team_role = ""
                            )
            self.application_developer.create(developer)
            return developer
        except Exception as e: 
            logging.error("OS error: {0}".format(e))
            logging.error(e.__dict__)  
    
    def create_reference(self, person, team_member):
        try:
            self.create_application_reference (team_member.identity.id,team_member.identity.url,self.TEAM_MEMBER_TFS,person.uuid,person.__tablename__)            

        except Exception as e: 
            logging.error("OS error: {0}".format(e))
            logging.error(e.__dict__)  