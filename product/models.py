from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.safestring import mark_safe
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel




class Category(object):
    pass


class Category(MPTTModel):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )

    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    keywords = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    image = models.ImageField(blank=True, upload_to='images/')
    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField(null=False, unique=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title

    class MPTTMeta :
        order_insertion_by =['title']

    def get_absolute_url(self):
        return reverse('article_detail',kwargs = {'slug':self.slug})

    def __str__(self):
            full_path =[self.title]
            k= self.parent
            while k is not None :
              full_path.append(k.title)
              k = k.parent
            return '/'.join(full_path[::-1])


class Product(models.Model):
        STATUS = (
            ('True', 'True'),
            ('False', 'False'),
        )
        aciselect = (
            ('True', 'az'),
            ('False', 'cok'),
        )
        category = models.ForeignKey(Category, on_delete=models.CASCADE)
        title = models.CharField(max_length=50)
        resturant = models.CharField(max_length=255)
        description = models.TextField(max_length=255)
        image = models.ImageField(blank=True, upload_to='images/')
        status = models.CharField(max_length=10, choices=STATUS)
        slug = models.SlugField(null=False, unique=True)
        create_at = models.DateTimeField(auto_now_add=True)
        update_at = models.DateTimeField(auto_now=True)
        detail = RichTextUploadingField()

        price = models.FloatField()
        amount = models.IntegerField()
        aci = models.CharField(max_length=10, choices=aciselect)

        def __str__(self):
            return self.title

        def get_absolute_url(self):
            return reverse('article_detail', kwargs={'slug': self.slug})

        def image_tag(self):
            if self.image.url is not None:
                return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
            else:
                return ""



class Images(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    title = models.CharField(max_length=50,blank=True)
    image = models.ImageField(blank=True, upload_to='images/')



    def __str__(self):
        return self.title


class comment(models.Model):
    STATUS = (
        ('New', 'New'),
        ('True', 'True'),
        ('False', 'False'),
    )
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    subject = models.CharField(max_length=50,blank=True)
    comment = models.CharField(max_length=250,blank=True)
    rate = models.IntegerField(default=1)
    ip = models.CharField(max_length=20,blank=True)
    status = models.CharField(max_length=10, choices=STATUS,default='New')
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

class commentForm(ModelForm):
        class Meta:
            model = comment
            fields = ['subject', 'comment', 'rate']







