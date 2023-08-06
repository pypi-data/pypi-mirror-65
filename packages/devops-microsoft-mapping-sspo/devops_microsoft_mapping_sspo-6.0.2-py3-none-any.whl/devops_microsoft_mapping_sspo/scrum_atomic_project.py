from .scrum_project import ScrumProject
from sspo_db.application import factories as application_factories
from sspo_db.model import factories as model_factories
import logging
logging.basicConfig(level=logging.INFO)

class ScrumAtomicProject(ScrumProject):

    def __init__(self, organization, configuration):
        super().__init__(organization, configuration)

    def create(self, element, organization, scrum_complex_project=None):
        try:
            logging.info("Scrum Atomic Project: Start")
            
            self.element = element
            self.organization = organization
            self.scrum_project = model_factories.ScrumAtomicProjectFactory()
            self.scrum_project_application = application_factories.ScrumAtomicProjectFactory()
            
            super().create()

            if scrum_complex_project is not None:
                self.scrum_project.root = False
                self.scrum_project.scrum_complex_project_id = scrum_complex_project.id
                self.update(self.scrum_project)

            self.__create_process(self.scrum_project, organization)

            logging.info("Scrum Atomic Project: End")

            return self.scrum_project

        except Exception as e: 
            logging.error("OS error: {0}".format(e))
            logging.error(e.__dict__)

    def __create_process(self,scrum_project, organization):
        try:

            logging.info("Creating a scrum process") 

            scrum_process = model_factories.ScrumProcessFactory(name=scrum_project.name, 
                        description=scrum_project.description, 
                        scrum_project = scrum_project)

            self.application_scrum_process.create(scrum_process)
                        
            logging.info("Creating a product backlog definition")    
            product_backlog_definition = model_factories.ProductBacklogDefinitionFactory(name=scrum_project.name, 
                description=scrum_project.description, 
                scrum_process = scrum_process)
            self.application_product_backlog_definition.create(product_backlog_definition)
                        
            logging.info("Creating a product backlog")   
            
            product_backlog = model_factories.ProductBacklogFactory(name=scrum_project.name, 
                description=scrum_project.description, 
                product_backlog_definition = product_backlog_definition.id)
            
            self.application_product_backlog.create(product_backlog)
                        
            logging.info("Creating a scrum team")  

            scrum_team = model_factories.ScrumTeamFactory(name = scrum_project.name, 
                                                                        description = scrum_project.description, 
                                                                        scrum_project= scrum_project.id,
                                                                        organization = organization)
            
            application_scrum_team = application_factories.ScrumTeamFactory()
            application_scrum_team.create(scrum_team)
                        
            logging.info("Creating a development team")  
            development_team = model_factories.DevelopmentTeamFactory(name = scrum_project.name, 
                                                                        description = scrum_project.description, 
                                                                        scrum_team_id = scrum_team.id)
                        
            application_development_team = application_factories.DevelopmentTeamFactory()
            application_development_team.create(development_team)

            logging.info("Creating a Application Reference")  
            '''
            self.create_application_reference(
                    team.id, 
                    team.url,
                    self.TEAM_TFS, 
                    scrum_team.uuid, 
                    scrum_team.type)

            self.create_application_reference(
                    team.id, 
                    team.url,
                    self.TEAM_TFS, 
                    development_team.uuid, 
                    development_team.type)
            '''
        except Exception as e: 
            logging.error("OS error: {0}".format(e))
            logging.error(e.__dict__)
    
    def update (self, atomic_project):
        try:
            self.scrum_project_application = application_factories.ScrumAtomicProjectFactory()
            self.scrum_project_application.update(atomic_project)
            
        except Exception as e: 
            logging.error("OS error: {0}".format(e))
            logging.error(e.__dict__)