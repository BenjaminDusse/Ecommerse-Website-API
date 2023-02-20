import random
from django.core.management.base import BaseCommand, CommandError
from django.contrib.admin.utils import flatten
from django_seed import Seed
from store.models import Collection
from store.models import Product, ProductImage

NAME = 'products'

class Command(BaseCommand):
    help = 'This command creates {NAME}'

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=2, type=int, help="How many {NAME} you want to create"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        collections = Collection.objects.all()
        seeder.add_entity(
            Product,
            number,
            {
                'title': lambda x: seeder.faker.catch_phrase(),
                'slug': lambda x: seeder.faker.slug(),
                'description': lambda x: seeder.faker.paragraph(nb_sentences=5),
                'unit_price': lambda x: random.randrange(50, 9999, 10),
                'inventory': lambda x: random.randrange(1, 50, 10),
                'collection': lambda x: random.choice(collections)
            },
        )

        created_photos = seeder.execute()
        created_clean = flatten(list(created_photos.values()))
        for i in range(1, random.randint(1, 9)):
            for pk in created_clean:
                product = Product.objects.get(pk=pk)
                ProductImage.objects.create(
                    caption=seeder.faker.sentence(),
                    product=product,
                    file=f"product_images/{random.randint(1, 21)}.jpg"
                )
        self.stdout.write(self.style.SUCCESS(f"{number} {NAME} created!"))
