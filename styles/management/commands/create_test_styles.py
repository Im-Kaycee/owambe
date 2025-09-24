import os
import random
from django.core.management.base import BaseCommand
from styles.models import Style
from django.conf import settings

class Command(BaseCommand):
    help = 'Create 100 test styles with 6 available images'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=100,
            help='Number of styles to create (default: 100)',
        )

    def handle(self, *args, **options):
        count = options['count']
        
        # Import your custom User model
        from accounts.models import User
        
        # Get or create a test user (you can change this username)
        try:
            user = User.objects.get(username='kaycee')
        except User.DoesNotExist:
            user = User.objects.create_user(
                username='testuser',
                email='test@example.com',
                password='testpass123'
            )
            self.stdout.write(self.style.SUCCESS(f'Created test user: {user.username}'))
        
        # Sample data for variety
        categories = ['men', 'women', 'kids']
        fabric_types = ['Cotton', 'Silk', 'Linen', 'Wool', 'Chiffon', 'Denim', 'Velvet', 'Jacquard']
        occasions = ['Wedding', 'Party', 'Church', 'Office', 'Casual', 'Traditional', 'Festival', 'Graduation']
        colours = ['Red', 'Blue', 'Green', 'Yellow', 'Black', 'White', 'Purple', 'Pink', 'Orange', 'Brown']
        
        # Your 6 image filenames (adjust these to match your actual image files)
        image_files = [
            '2fb69f73354d30a48aa45cc2c6207cef.jpg',
            'SnapInsta.to_532172966_17856461199485150_5153975727907762128_n.jpg',
            '43699239b59f2b5e83bbda97b3627126.jpg',
            '6e213e8b1bb96dc580e1336a8c956590.jpg',
            '04bb10ccba71d2ee0a71cee39232ad37.jpg',
            '88353dc79f8c1bd419e871cbab895a99.jpg',
        ]
        
        # Check if images exist in media directory
        media_path = settings.MEDIA_ROOT / 'styles'
        available_images = []
        
        for img_file in image_files:
            img_path = media_path / img_file
            if img_path.exists():
                available_images.append(f'styles/{img_file}')
            else:
                self.stdout.write(self.style.WARNING(f'Image not found: {img_path}'))
        
        if not available_images:
            self.stdout.write(self.style.ERROR('No images found! Please add images to media/styles/ directory first.'))
            return
        
        self.stdout.write(f'Creating {count} test styles...')
        
        styles_created = 0
        for i in range(count):
            try:
                # Create unique title
                title = f"Test Style {i+1} - {random.choice(['Elegant', 'Modern', 'Traditional', 'Classic'])}"
                
                # Select random image from available ones
                image_path = random.choice(available_images)
                
                style = Style(
                    uploader=user,
                    title=title,
                    image=image_path,
                    category=random.choice(categories),
                    fabric_type=random.choice(fabric_types),
                    occasion=random.choice(occasions),
                    colour=random.choice(colours),
                    tailor_name=random.choice(['Master Tailor Ltd', 'Fashion House', 'Bespoke Designs', 'Creative Stitches', None]),
                    tailor_whatsapp=random.choice(['+1234567890', '+0987654321', None]),
                )
                
                style.save()
                styles_created += 1
                
                if (i + 1) % 10 == 0:
                    self.stdout.write(f'Created {i + 1} styles...')
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating style {i+1}: {str(e)}'))
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {styles_created} test styles!'))