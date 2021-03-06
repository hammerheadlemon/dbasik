import factory

from datamap.models import Datamap
from datamap.models import DatamapLine
from register.models import Project
from register.models import ProjectStage
from register.models import ProjectType
from register.models import Tier


class TierFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tier

    name = "Test Tier from Factory"
    slug = "test-tier-from-factory"
    description = "Description for Tier object"


class DatamapFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Datamap
        django_get_or_create = ('name', 'tier')

    name = "Test Datamap from Factory"
    tier = factory.SubFactory(TierFactory)


class DatamapLineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DatamapLine

    datamap = factory.SubFactory(DatamapFactory)
    key = "Test key"
    sheet = "Test sheet"
    cell_ref = "A1"


class ProjectTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProjectType

    name = factory.Faker('name')


class ProjectStageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProjectStage

    name = "Test Stage"


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Project

    name = "Test Project"
    tier = factory.SubFactory(TierFactory)
    project_type = factory.SubFactory(ProjectTypeFactory)
    stage = factory.SubFactory(ProjectStageFactory)
