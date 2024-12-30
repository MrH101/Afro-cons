'''from django.db import models

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=50,unique=True)
    slug = models.SlugField (max_length = 100,unique=True)
    deescription = models.TextField(max_length=255,blank=True)
    cat_image = models.ImageField(upload_to = 'media/categories',blank = True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.category_name
    '''
from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(max_length=255, blank=True)
    cat_image = models.ImageField(upload_to='categories/', blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ['category_name']  # Optional: Orders categories alphabetically by default

    def get_url(self):
            return reverse('products_by_category',args=[self.slug])
 
 
    def __str__(self):
        return self.category_name

    # Override save method to auto-generate slug if not provided
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)