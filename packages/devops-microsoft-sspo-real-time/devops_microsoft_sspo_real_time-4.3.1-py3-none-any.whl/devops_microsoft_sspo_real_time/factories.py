import factory
from devops_microsoft_sspo_real_time.scrum_development_task import ScrumDevelopmentTask
from devops_microsoft_sspo_real_time.scrum_project import ScrumProject
from devops_microsoft_sspo_real_time.atomic_user_story import AtomicUserStory
from devops_microsoft_sspo_real_time.epic import Epic
import factory

class EpicFactory(factory.Factory):
    class Meta:
        model = Epic

class AtomicUserStoryFactory(factory.Factory):
    class Meta:
        model = AtomicUserStory

class ScrumDevelopmentTaskFactory(factory.Factory):
    class Meta:
        model = ScrumDevelopmentTask

class ScrumProjectFactory(factory.Factory):
    class Meta:
        model = ScrumProject
