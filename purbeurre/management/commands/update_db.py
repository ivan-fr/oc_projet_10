from django.core.management.base import BaseCommand
from django.db import connection
from django.db import reset_queries
from django.db import transaction

from purbeurre.managers.api import ApiManager
from purbeurre.models import Brand, Ingredient, Store, Category, Product


class Command(BaseCommand):
    help = 'Update the database with the openfoodfacts API'

    def handle(self, *args, **options):

        with transaction.atomic():

            products_db = Product.objects.all()
            product_count = products_db.count()

            self.stdout.write(self.style.SUCCESS(
                "il y a " + str(product_count) + " produits."
            ))

            for i, product_db in enumerate(products_db, start=1):
                product_from_api = ApiManager.get_product(product_db.bar_code,
                                                          with_clean=True)

                nutriments = product_from_api.get('nutriments', {})

                product_db.name = product_from_api.get('product_name', None)
                product_db.generic_name = product_from_api.get('generic_name',
                                                               None)
                product_db.nutrition_grades = product_from_api.get(
                    'nutrition_grades', None)
                product_db.fat = str(nutriments.get('fat_100g', None))
                product_db.saturated_fat = str(
                    nutriments.get('saturated-fat_100g', None))
                product_db.sugars = str(nutriments.get('sugars_100g', None))
                product_db.salt = str(nutriments.get('salt_100g', None))
                product_db.image_url = product_from_api.get('image_url', None)
                product_db.save()

                categories, categories_temoin = [], []
                categories_of_product = Category.objects.filter(
                    product=product_db)

                for category in product_from_api.get('categories', ()):
                    self.stdout.write(self.style.SUCCESS('lol'))
                    category_db, created = Category.objects.get_or_create(
                        name=category)
                    if category_db not in categories_of_product:
                        categories.append(category_db)
                    categories_temoin.append(category_db)

                product_db.categories.add(*categories)

                product_db.categories.remove(
                    *tuple(
                        set(categories_of_product).union(set(categories_temoin))
                        - set(categories_temoin)))

                iteration_ingredients = ()
                if product_from_api.get('ingredients_text_fr', ()):
                    iteration_ingredients = product_from_api \
                        .get('ingredients_text_fr')
                elif product_from_api.get('ingredients', ()):
                    iteration_ingredients = product_from_api.get('ingredients')

                ingredients, ingredients_temoin = [], []
                ingredients_of_product = Ingredient.objects.filter(
                    product=product_db)
                for ingredient in iteration_ingredients:
                    ingredient_db, created = Ingredient.objects.get_or_create(
                        name=ingredient)
                    if ingredient_db not in ingredients_of_product:
                        ingredients.append(ingredient_db)
                    ingredients_temoin.append(ingredient_db)
                product_db.ingredients.add(*ingredients)

                product_db.ingredients.remove(
                    *tuple(
                        set(ingredients_of_product).union(
                            set(ingredients_temoin))
                        - set(ingredients_temoin)))

                brands, brands_temoin = [], []
                brands_of_product = Brand.objects.filter(product=product_db)
                for brand in product_from_api.get('brands_tags', ()):
                    brand_db, created = Brand.objects.get_or_create(name=brand)
                    if brand_db not in brands_of_product:
                        brands.append(brand_db)
                    brands_temoin.append(brand_db)
                product_db.brands.add(*brands)

                product_db.brands.remove(
                    *tuple(set(brands_of_product).union(set(brands_temoin))
                           - set(brands_temoin)))

                stores, stores_temoin = [], []
                stores_of_product = Store.objects.filter(product=product_db)
                for store in product_from_api.get('stores_tags', ()):
                    store_db, created = Store.objects.get_or_create(name=store)
                    if store_db not in stores_of_product:
                        brands.append(store_db)
                    stores_temoin.append(store_db)
                product_db.stores.add(*stores)

                product_db.brands.remove(
                    *tuple(set(stores_of_product).union(set(stores_temoin))
                           - set(stores_temoin)))

                self.stdout.write(self.style.SUCCESS(
                    str(round(i / product_count * 100, 2)) + "% avec "
                    + str(len(connection.queries)) + " requêtes."
                ))

                reset_queries()
