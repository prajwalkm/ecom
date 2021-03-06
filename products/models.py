from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from random import randint
# Create your models here.


class ProductQuerySet(models.query.QuerySet):
	def active(self):
		return self.filter(active=True)


class ProductManager(models.Manager):
	def get_queryset(self):
		return ProductQuerySet(self.model,using=self._db)

	def all(self,*args,**kwargs):
		return self.get_queryset().active()

	def get_related(self,instance):
		products_one=self.get_queryset().filter(categories__in=instance.categories.all())
		products_two=self.get_queryset().filter(default=instance.default)
		qs=(products_one|products_two).exclude(id=instance.id).filter(active=True).distinct()
		return qs

gender_choices=(
	('mens','Mens'),
	('ladies','Ladies'))

class products(models.Model):
	title=models.CharField(max_length=120)
	fancy_title=models.CharField(max_length=120,default="Trendy Watch")
	description=models.TextField(blank=True,null=True)
	color=models.CharField(max_length=120,blank=True,null=True)
	gender=models.CharField(max_length=120,choices=gender_choices,default="Mens")
	price=models.DecimalField(decimal_places=2,max_digits=20)
	active=models.BooleanField(default=True)
	objects=ProductManager()
	categories=models.ManyToManyField('category',blank=True)
	default=models.ForeignKey('category',related_name="default_category",null=True,blank=True)

    

	#def __unicode__(self):
	#	return self.title

	def __str__(self):
		return self.title

	class Meta:
		ordering=['-id']

	def get_absolute_url(self):
		return reverse("ProductsDetail",kwargs={"pk":self.pk})

	def get_image_url(self):
		img=self.productimage_set.first()
		if img:
			return img.image.url
		return img #none

class variation(models.Model):
	products=models.ForeignKey(products)
	title=models.CharField(max_length=120)
	price=models.DecimalField(decimal_places=2,max_digits=20)
	sale_price=models.DecimalField(decimal_places=2,max_digits=20,null=True,blank=True)
	active=models.BooleanField(default=True)
	inventory=models.IntegerField(null=True,blank=True)

	#def __unicode__(self):
	#	return self.title
	def __str__(self):
		return self.title

	def get_price(self):
		if self.sale_price is not None:
			return self.sale_price
		else:
			return self.price

	def get_html_price(self):
		if self.sale_price is not None:
			html_text="<span class='sale-price'>%s</span> <span class='og_price'>%s</span>"%(self.sale_price,self.price)
		else:
			html_text="<span class='price'>%s</span>"%(self.price)
		return mark_safe(html_text)


	def get_absolute_url(self):
		return self.products.get_absolute_url()

	def add_to_cart(self):
		return "%s?item=%s&qty=1" %(reverse("carts"), self.id)


	def remove_from_cart(self):
		return "%s?item=%s&qty=1&delete=True" %(reverse("carts"), self.id)

	def get_title(self):
		return "%s - %s" %(self.products.title,self.title)


def product_post_saved_receiver(sender,instance,created,*args,**kwargs):
	products=instance
	variations=products.variation_set.all()
	if variations.count()==0:
		new_var=variation()
		new_var.products=products
		new_var.title="default"
		new_var.price=products.price
		new_var.save()



post_save.connect(product_post_saved_receiver,sender=products)

def image_upload_to(instance,filename):
	title=instance.products.title
	file_extension = filename.split(".")[1]
	slug=slugify(title)
	new_filename="%s-%s.%s"%(slug,instance.id,file_extension)
	return 'products/%s/%s'%(slug,new_filename)

class ProductImage(models.Model):
	products=models.ForeignKey(products)
	image= models.ImageField(upload_to=image_upload_to)

	def __str__(self):
		return self.products.title


 



class category(models.Model):
	title=models.CharField(max_length=120,unique=True)
	slug=models.SlugField(unique=True)
	description=models.TextField(null=True,blank=True)
	active=models.BooleanField(default=True)
	timestamp=models.DateTimeField(auto_now_add=True,auto_now=False)

	def __str__(self):
		return self.title

	
	def get_absolute_url(self):
		return reverse("category_detail",kwargs={"slug":self.slug})


	

def image_upload_to_featured(instance,filename):
	title='featured'
	file_extension = filename.split(".")[1]
	slug=slugify(title)
	new_filename="%s-%s.%s"%(slug,randint(1,1000),file_extension)
	return 'products/%s/featured/%s'%(slug,new_filename)




class ProductFeatured(models.Model):
	image=models.ImageField(upload_to=image_upload_to_featured)
	title=models.CharField(max_length=120,null=True,blank=True)
	description=models.TextField(blank=True,null=True)
	text=models.CharField(max_length=220,null=True,blank=True)

	text_right=models.BooleanField(default=False)
	active=models.BooleanField(default=True)


	def __str__(self):
		return self.title













