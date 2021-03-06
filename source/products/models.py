from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.utils.safestring import mark_safe
from django.utils.text import slugify


class ProductQuerySet(models.query.QuerySet):

    def active(self):
        return self.filter(active=True)


class ProductManager(models.Manager):

    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    # Altera o padrão de busca da query "all"
    def all(self, *args, **kwargs):
        return self.get_queryset().active()

    def get_related(self, instance):
        products_one = self.get_queryset().filter(
                categories__in=instance.categories.all()
                )
        products_two = self.get_queryset().filter(
                default=instance.default
                )
        # TODO: Precisa excluir os produtos que não estão ativos
        # Retornar o 'default' no queryset faz com que produtos de categorias
        # diferentes sejam retornados também
        q = (products_one | products_two).exclude(id=instance.id).distinct()
        return q


class Product(models.Model):

    title = models.CharField(max_length=240)
    description = models.TextField(blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    active = models.BooleanField(default=True)
    categories = models.ManyToManyField('Category', blank=True)
    default = models.ForeignKey(
            'Category',
            related_name='default_category',
            null=True,
            blank=True
            )

    # instanciando o objeto ProductManager, automaticamente a ListView só irá
    # retornar os objetos definidos no método 'all', sem precisar fazer
    # qualquer chamada na 'views.py'
    objects = ProductManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'pk': self.pk})

    def get_image_url(self):
        img = self.productimage_set.first()
        if img:
            return img.image.url
        return img # img será None


class Variation(models.Model):
    product = models.ForeignKey(Product)
    title = models.CharField(max_length=120)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    sale_price = models.DecimalField(
            decimal_places=2,
            max_digits=20,
            null=True,
            blank=True
            )
    active = models.BooleanField(default=True)
    inventory = models.IntegerField(null=True, blank=True) # refer none == unlimited amount

    def __str__(self):
        return self.title

    def get_price(self):
        if self.sale_price is not None:
            return self.sale_price
        else:
            return self.price

    def get_html_price(self):
        if self.sale_price is not None:
            html_price = "{} </small><small class=\
                    'orig-price'>{}</small>".format(self.sale_price, self.price)
            price = mark_safe(html_price)

        else:
            price = self.price

        return price or None

    def get_absolute_url(self):
        return self.product.get_absolute_url()

    def get_title(self):
        return "{} - {}".format(self.product.title, self.title)

    def add_to_cart(self):
        return "{}?item={}&qty=1".format(reverse('cart'), self.id)

    def delete_from_cart(self):
        return "{}?item={}&qty=1&delete=True".format(reverse('cart'), self.id)


def product_post_saved_receiver(sender, instance, created, *args, **kwargs):
    """
    Se o objeto MP3 Player for criado/alterado (salvo de alguma forma),
    os argumentos enviados serão:
    sender == <class 'products.models.Product'> # a classe
    instance == MP3 Player # a instancia da classe
    created == False # acho que indica se a instância acabou de ser criada
    """

    product = instance

    # Reverse Relation
    variations = product.variation_set.all() # É quase igual a instanciar
                                             # Variation.objects.filter(product=product)
    if variations.count() == 0:
        new_var = Variation()
        new_var.product = product
        new_var.title = "Default"
        new_var.price = product.price
        new_var.save()


post_save.connect(product_post_saved_receiver, sender=Product)


def image_upload_to(instance, filename):
    title = instance.product.title
    slug = slugify(title)
    *filename_garbage, file_extension = filename.split(".")
    new_filename = "{}-{}.{}".format(slug, instance.id, file_extension)

    if 'ProductFeatured' in repr(instance):
        return "products/{}/featured/{}".format(slug, new_filename)

    return "products/{}/{}".format(slug, new_filename)


class ProductImage(models.Model):

    product = models.ForeignKey(Product)
    image = models.ImageField(upload_to=image_upload_to)

    def __str__(self):
        return self.product.title


class Category(models.Model):
    title = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("categories:category_detail", kwargs={'slug': self.slug })


class ProductFeatured(models.Model):
    product = models.ForeignKey(Product)
    image = models.ImageField(upload_to=image_upload_to)
    title = models.CharField(max_length=120, blank=True)
    text = models.CharField(max_length=220, blank=True)
    text_right = models.BooleanField(default=False)
    show_price = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    make_image_background = models.BooleanField(default=False)

    def __str__(self):
        return self.product.title
