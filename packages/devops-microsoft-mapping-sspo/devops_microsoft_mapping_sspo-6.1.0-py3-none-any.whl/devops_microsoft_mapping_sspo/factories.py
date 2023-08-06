import factory
from devops_microsoft_mapping_sspo.scrum_intented_development_task import ScrumIntentedDevelopmentTask
from devops_microsoft_mapping_sspo.scrum_performed_development_task import ScrumPerformedDevelopmentTask
from devops_microsoft_mapping_sspo.scrum_atomic_project import ScrumAtomicProject
from devops_microsoft_mapping_sspo.scrum_complex_project import ScrumComplexProject
from devops_microsoft_mapping_sspo.sprint import Sprint
from devops_microsoft_mapping_sspo.team_member import Teammember
from devops_microsoft_mapping_sspo.atomic_user_story import AtomicUserStory
from devops_microsoft_mapping_sspo.epic import Epic
from devops_microsoft_mapping_sspo.scrum_process import ScrumProcess
from devops_microsoft_mapping_sspo.development_team import DevelopmentTeam
from devops_microsoft_mapping_sspo.product_backlog_definition import ProductBacklogDefinition
from devops_microsoft_mapping_sspo.product_backlog import ProductBacklog
from devops_microsoft_mapping_sspo.scrum_team import ScrumTeam

class ScrumAtomicProjectFactory(factory.Factory):
    class Meta:
        model = ScrumAtomicProject
        
    organization = None
    configuration = None

class ScrumComplexProjectFactory(factory.Factory):
    class Meta:
        model = ScrumComplexProject
    
    organization = None
    configuration = None

class ScrumIntentedDevelopmentTaskFactory(factory.Factory):
    class Meta:
        model = ScrumIntentedDevelopmentTask
    
    organization = None
    configuration = None

class ScrumPerformedDevelopmentTaskFactory(factory.Factory):
    class Meta:
        model = ScrumPerformedDevelopmentTask
    
    organization = None
    configuration = None

class SprintFactory(factory.Factory):
    class Meta:
        model = Sprint
    
    organization = None
    configuration = None

class TeamMemberFactory(factory.Factory):
    class Meta:
        model = Teammember
    
    organization = None
    configuration = None

class EpicFactory(factory.Factory):
    class Meta:
        model = Epic
    
    organization = None
    configuration = None

class AtomicUserStoryFactory(factory.Factory):
    class Meta:
        model = AtomicUserStory

    organization = None
    configuration = None

class ScrumProcessFactory(factory.Factory):
    class Meta:
        model = ScrumProcess

    organization = None
    configuration = None

class DevelopmentTeamFactory(factory.Factory):
    class Meta:
        model = DevelopmentTeam

    organization = None
    configuration = None

class ProductBacklogFactory(factory.Factory):
    class Meta:
        model = ProductBacklog

    organization = None
    configuration = None

class ProductBacklogDefinitionFactory(factory.Factory):
    class Meta:
        model = ProductBacklogDefinition
    
    organization = None
    configuration = None

class ScrumTeamFactory(factory.Factory):
    class Meta:
        model = ScrumTeam
    
    organization = None
    configuration = None