from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from portfolio.models import Category, Technology, Project
from services.models import Service
from team.models import TeamMember
from testimonials.models import Testimonial
from blog.models import BlogPost, Tag, BlogCategory
from core.models import CompanyStat, FAQ, SiteSettings, NewsletterSubscriber
from clients.models import Client
from faker import Faker  # optional – install faker if you want realistic data

User = get_user_model()
fake = Faker()

class Command(BaseCommand):
    help = 'Seed the database with realistic demo data for Vanguard Labs'

    def handle(self, *args, **kwargs):
        self.stdout.write("🌱 Seeding data...")

        # Create admin user if none exists
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser('admin', 'admin@vanguardlabs.com', 'admin123')
            self.stdout.write("✅ Admin user created (admin/admin123)")

        # Site Settings
        settings, _ = SiteSettings.objects.get_or_create(
            site_name='Vanguard Labs',
            defaults={
                'tagline': 'Building Tomorrow\'s Digital Experiences.',
                'footer_text': 'We build premium digital solutions.',
                'copyright_text': '© Vanguard Labs. All rights reserved.',
                'contact_email': 'hello@vanguardlabs.com',
                'contact_phone': '+1 (555) 123-4567',
                'address': '123 Tech Street, Silicon Valley, CA',
                'meta_description': 'Vanguard Labs – premium digital agency building tomorrow\'s digital experiences.',
            }
        )
        self.stdout.write("✅ Site settings created")

        # Company Stats
        stats = [
            {'label': 'Projects Completed', 'value': 250, 'icon': 'fas fa-code'},
            {'label': 'Clients Served', 'value': 120, 'icon': 'fas fa-users'},
            {'label': 'Years of Experience', 'value': 8, 'icon': 'fas fa-calendar'},
            {'label': 'Technologies Mastered', 'value': 45, 'icon': 'fas fa-microchip'},
        ]
        for stat in stats:
            CompanyStat.objects.get_or_create(label=stat['label'], defaults=stat)
        self.stdout.write("✅ Company stats created")

        # FAQs
        faqs = [
            {'question': 'What services do you offer?',
             'answer': 'We offer web development, LMS, CBT systems, UI/UX, AI integration, brand identity, business automation, mobile apps, API development, and cloud deployment.'},
            {'question': 'How much does a project cost?',
             'answer': 'Each project is unique. We provide a custom quote based on your requirements after a discovery call.'},
            {'question': 'How long does a project take?',
             'answer': 'Timelines vary from 2 weeks for small projects to 6+ months for complex platforms.'},
        ]
        for i, faq in enumerate(faqs, start=1):
            FAQ.objects.get_or_create(question=faq['question'], defaults={'answer': faq['answer'], 'order': i})
        self.stdout.write("✅ FAQs created")

        # Categories
        categories = ['Web Development', 'Mobile App', 'UI/UX', 'AI / ML', 'LMS', 'CBT', 'Brand Identity']
        cat_objs = {}
        for cat in categories:
            obj, _ = Category.objects.get_or_create(name=cat, slug=cat.lower().replace(' ', '-'))
            cat_objs[cat] = obj
        self.stdout.write("✅ Categories created")

        # Technologies
        tech_names = ['Django', 'PostgreSQL', 'React', 'Vue', 'Tailwind', 'Docker', 'AWS', 'Python', 'JavaScript', 'Redis']
        tech_objs = {}
        for tech in tech_names:
            obj, _ = Technology.objects.get_or_create(name=tech, defaults={'icon': f'fab fa-{tech.lower()}'})
            tech_objs[tech] = obj
        self.stdout.write("✅ Technologies created")

        # Services
        services = [
            {'name': 'Web Development', 'icon': 'fa-globe'},
            {'name': 'LMS Development', 'icon': 'fa-graduation-cap'},
            {'name': 'CBT Systems', 'icon': 'fa-laptop'},
            {'name': 'UI/UX Design', 'icon': 'fa-pencil-ruler'},
            {'name': 'AI Integration', 'icon': 'fa-brain'},
            {'name': 'Brand Identity', 'icon': 'fa-paint-brush'},
        ]
        for svc in services:
            Service.objects.get_or_create(
                name=svc['name'],
                defaults={
                    'icon': svc['icon'],
                    'description': f'Premium {svc["name"]} tailored for your business.',
                    'is_active': True
                }
            )
        self.stdout.write("✅ Services created")

        # Team Members
        team_members = [
            {'name': 'Alice Johnson', 'role': 'CEO & Lead Developer', 'experience': 10},
            {'name': 'Bob Smith', 'role': 'Senior UI/UX Designer', 'experience': 7},
            {'name': 'Carol White', 'role': 'Full-Stack Developer', 'experience': 5},
            {'name': 'Dave Brown', 'role': 'DevOps Engineer', 'experience': 4},
        ]
        for member in team_members:
            TeamMember.objects.get_or_create(
                name=member['name'],
                defaults={
                    'role': member['role'],
                    'bio': f'Experienced {member["role"]} with a passion for innovation.',
                    'experience': member['experience'],
                    'photo': 'team/default.jpg',
                    'github': 'https://github.com/example',
                    'linkedin': 'https://linkedin.com/in/example',
                }
            )
        self.stdout.write("✅ Team members created")

        # Testimonials
        testimonials = [
            {'client_name': 'Company A', 'company': 'TechCorp', 'review': 'Vanguard Labs transformed our digital presence. Highly recommend!', 'rating': 5},
            {'client_name': 'Company B', 'company': 'StartupX', 'review': 'The team delivered beyond our expectations.', 'rating': 5},
        ]
        for t in testimonials:
            Testimonial.objects.get_or_create(
                client_name=t['client_name'],
                company=t['company'],
                defaults={'review': t['review'], 'rating': t['rating'], 'is_published': True}
            )
        self.stdout.write("✅ Testimonials created")

        # Blog Categories and Tags
        blog_cats = ['Technology', 'Design', 'Business', 'AI']
        for cat in blog_cats:
            BlogCategory.objects.get_or_create(name=cat, slug=cat.lower())
        tags = ['Django', 'React', 'UX', 'DevOps']
        tag_objs = {}
        for tag in tags:
            obj, _ = Tag.objects.get_or_create(name=tag, slug=tag.lower())
            tag_objs[tag] = obj
        self.stdout.write("✅ Blog categories and tags created")

        # Blog Posts
        for i in range(3):
            title = fake.sentence(nb_words=6)
            post, _ = BlogPost.objects.get_or_create(
                title=title,
                defaults={
                    'slug': slugify(title),
                    'content': fake.paragraphs(nb=5),
                    'cover_image': 'blog/default.jpg',
                    'is_published': True,
                    'author': TeamMember.objects.first(),
                }
            )
            post.categories.add(BlogCategory.objects.first())
            post.tags.add(tag_objs['Django'])
        self.stdout.write("✅ Blog posts created")

        # Clients
        clients = ['Acme Inc.', 'GlobalTech', 'StartupHub', 'EduOnline']
        for name in clients:
            Client.objects.get_or_create(
                name=name,
                defaults={
                    'status': 'active',
                    'industry': 'Technology',
                    'primary_contact_email': 'contact@example.com',
                }
            )
        self.stdout.write("✅ Clients created")

        # Projects
        project_data = [
            {'title': 'Vanguard Portfolio Site', 'client': 'Vanguard Labs', 'category': 'Web Development'},
            {'title': 'AI-driven Chatbot', 'client': 'TechCorp', 'category': 'AI / ML'},
            {'title': 'Mobile Banking App', 'client': 'GlobalTech', 'category': 'Mobile App'},
            {'title': 'Learning Management System', 'client': 'EduOnline', 'category': 'LMS'},
        ]
        for p in project_data:
            project, _ = Project.objects.get_or_create(
                title=p['title'],
                defaults={
                    'slug': slugify(p['title']),
                    'description': f'A comprehensive {p["category"]} project for {p["client"]}.',
                    'client': p['client'],
                    'category': cat_objs.get(p['category']),
                    'completion_date': timezone.now(),
                    'cover_image': 'projects/covers/default.jpg',
                    'featured': True,
                }
            )
            project.technologies.add(tech_objs['Django'])
            project.team_members.add(TeamMember.objects.first())
        self.stdout.write("✅ Projects created")

        # Newsletter subscriber (sample)
        NewsletterSubscriber.objects.get_or_create(email='demo@example.com')

        self.stdout.write(self.style.SUCCESS("✅ All data seeded successfully!"))
