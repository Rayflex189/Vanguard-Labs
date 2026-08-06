from django.core.management.base import BaseCommand
from portfolio.models import Category, Technology, Project
from team.models import TeamMember
from services.models import Service
# ... import all models you want to seed

class Command(BaseCommand):
    help = 'Seeds the database with demo data'

    def handle(self, *args, **kwargs):
        # Create categories
        cat, _ = Category.objects.get_or_create(name='Web Development', slug='web')
        tech, _ = Technology.objects.get_or_create(name='Django', icon='fab fa-django')
        # Create team members
        member, _ = TeamMember.objects.get_or_create(
            name='John Doe',
            defaults={'role': 'Lead Developer', 'bio': '...', 'experience': 5}
        )
        # Create services
        service, _ = Service.objects.get_or_create(
            name='Web Development',
            defaults={'icon': 'fa-code', 'description': '...', 'is_active': True}
        )
        # Create a project
        project, _ = Project.objects.get_or_create(
            title='Vanguard Site',
            defaults={
                'slug': 'vanguard-site',
                'description': '...',
                'client': 'Vanguard Labs',
                'category': cat,
                'completion_date': '2025-01-01',
                'cover_image': 'projects/covers/default.jpg',
                'featured': True,
            }
        )
        project.technologies.add(tech)
        project.team_members.add(member)
        self.stdout.write(self.style.SUCCESS('Demo data created successfully!'))
