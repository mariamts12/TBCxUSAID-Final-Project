from django.db import models


class CategoryManager(models.Manager):

    def get_top_categories(self):
        return self.filter(parent=None)

    def get_all_subcategories(self, category_id: int) -> set:
        category = self.prefetch_related("subcategories").get(id=category_id)

        result = set()
        result.add(category_id)

        self.__add_subcategories(result, category)

        return result

    def __add_subcategories(self, result, category_instance):
        subcategories = category_instance.subcategories.all()
        for subcategory in subcategories:
            result.add(subcategory.id)
            self.__add_subcategories(result, subcategory)
