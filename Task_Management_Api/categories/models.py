from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    """
    Category model representing a category in the task management system.

    Attributes:
        name (str): The unique name of the category, with a maximum length of 50 characters.
        author (User): A foreign key to the User who created a custom category
        is_default (bool): Boolean field indicating if the category is default or custom

    Methods:
        __str__(): Returns the string representation of the category, which is its name.
    """
    name = models.CharField(max_length=50)
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name