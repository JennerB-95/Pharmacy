from datetime import datetime, date

from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.forms import model_to_dict
from crum import get_current_user
from django.db.models import Sum
from django.db.models.functions import Coalesce

from config.settings import MEDIA_URL, STATIC_URL
from core.erp.choices import gender_choices, type_choices
from core.models import BaseModel


class Category(BaseModel):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        super(Category, self).save()


    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['id']


class Laboratory(BaseModel):
    description = models.CharField(max_length=100, verbose_name='Nombre', unique=True)
    address = models.CharField(max_length=250, null=True, blank=True, verbose_name='Dirección')

    def __str__(self):
        return self.description

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        super(Laboratory, self).save()


    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Laboratorio'
        verbose_name_plural = 'Laboratorios'
        ordering = ['id']


class Distribuidor(BaseModel):
    laboratory = models.ForeignKey(Laboratory, on_delete=models.CASCADE, verbose_name='Laboratorio')
    name = models.CharField(max_length=100, verbose_name='Nombre')
    phone = models.CharField(max_length=8, null=True, blank=True, verbose_name='Telefono')
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name='Correo')
    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        super(Distribuidor, self).save()


    def toJSON(self):
        item = model_to_dict(self)
        item['laboratory'] = self.laboratory.toJSON()
        return item

    class Meta:
        verbose_name = 'Distribuidor'
        verbose_name_plural = 'Distribuidores'
        ordering = ['id']


class Unit(BaseModel):
    name = models.CharField(max_length=100, verbose_name='Nombre', unique=True)

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        super(Unit, self).save()


    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Unidad de Medida'
        verbose_name_plural = 'Unidades de Medida'
        ordering = ['id']


class Product(BaseModel):
    barcode = models.CharField(max_length=50, unique=True, verbose_name='Codigo de Barra')
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    pvp = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Precio Venta')
    pvp_cmp = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Precio Compra')
    health_register = models.CharField(max_length=50, verbose_name='Registro Sanitario')
    lot = models.CharField(max_length=20, null=True, blank=True, verbose_name='Lote') 
    due_date = models.DateField(verbose_name='Fecha de Vencimiento')
    component = models.CharField(max_length=200, null=True, blank=True, verbose_name='Componente')
    type_med = models.CharField(max_length=10, choices=type_choices, default='comercial', verbose_name='Tipo')
    indication = models.CharField(max_length=300, verbose_name='Indicación')
    
    stock = models.IntegerField(default=0, verbose_name='Existencia')
    latest_buy = models.DateField(null=True, blank=True, verbose_name='Ultima Compra')

    cat = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Categoría')
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, verbose_name='Unidad de Medida')
    lab = models.ForeignKey(Laboratory, on_delete=models.CASCADE, verbose_name='Laboratorio')
    image = models.ImageField(upload_to='product/', null=True, blank=True, verbose_name='Imagen')

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        super(Product, self).save()

    def toJSON(self):
        item = model_to_dict(self)
        item['due_date'] = self.due_date.strftime('%Y-%m-%d')
        item['type_med'] = {'id': self.type_med, 'name': self.get_type_med_display()}
        item['cat'] = self.cat.toJSON()
        item['unit'] = self.unit.toJSON()
        item['lab'] = self.lab.toJSON()
        item['image'] = self.get_image()
        item['status_med'] = format(self.status_med)
        item['pvp'] = format(self.pvp, '.2f')
        item['pvp_cmp'] = format(self.pvp_cmp, '.2f')
        return item

    def get_image(self):
        if self.image:
            return '{}{}'.format(MEDIA_URL, self.image)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    def get_stock(self):
        return int(self.detshopping_set.filter(saldo__gt=0).aggregate(total=Coalesce(Sum('saldo'), 0)).get('subtotal'))


    @property
    def status_med(self):	    
        hoy = date.today()	
        days = (self.due_date - hoy).days	   
        return days

    @property
    def stock_label(self):
        if (self.stock >= 0) and self.stock < 10: 
            return 'Danger'
        elif (self.stock > 10) and self.stock < 50:
            return 'Warning' 

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['id']
        unique_together = ('id', 'barcode')



class Client(BaseModel):
    names = models.CharField(max_length=150, verbose_name='Nombres')
    surnames = models.CharField(max_length=150, verbose_name='Apellidos')
    nit = models.CharField(max_length=10, unique=True, verbose_name='Nit', null=True, blank=True)
    phone = models.CharField(max_length=8, null=True, blank=True, verbose_name='Telefono')
    gender = models.CharField(max_length=10, choices=gender_choices, default='male', verbose_name='Sexo')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return '{} {} / {}'.format(self.names, self.surnames, self.nit)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        super(Client, self).save()


    def toJSON(self):
        item = model_to_dict(self)
        item['gender'] = {'id': self.gender, 'name': self.get_gender_display()}
        item['full_name'] = self.get_full_name()
        return item

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['id']


class Shopping(BaseModel):
    date_joined = models.DateField(default=datetime.now)
    laboratory = models.ForeignKey(Laboratory, on_delete=models.CASCADE)
    no_bill = models.CharField(max_length=10)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.laboratory.description

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        super(Shopping, self).save()

    # def calculate_invoice(self):
    #     subtotal = 0.0
    #     for d in self.detshopping_set.all():
    #         subtotal += float(d.price) * int(d.cant)
    #     self.subtotal = subtotal
    #     self.total = float(self.subtotal)
    #     self.save()

    def toJSON(self):
        item = model_to_dict(self)
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['laboratory'] = self.laboratory.toJSON()
        item['subtotal'] = format(self.subtotal, '.2f')
        item['total'] = format(self.total, '.2f')
        item['det'] = [i.toJSON() for i in self.detshopping_set.all()]
        return item

    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'
        ordering = ['id']

class DetShopping(BaseModel):
    shopping = models.ForeignKey(Shopping, on_delete=models.CASCADE)
    prod = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant = models.IntegerField(default=0)
    saldo = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.prod.name

    @property
    def cost_unit(self):
        return self.subtotal/self.cant

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        super(DetShopping, self).save()


    def toJSON(self):
        item = model_to_dict(self, exclude=['shopping'])
        item['prod'] = self.prod.toJSON()
        item['price'] = format(self.price, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de Compra'
        verbose_name_plural = 'Detalle de Compras'
        ordering = ['id']

@receiver(post_save, sender=DetShopping)
def detail_shopping_save(sender, instance,**kwargs):
    id_producto = instance.prod.id
    fecha_compra=instance.shopping.date_joined

    prod=Product.objects.filter(pk=id_producto).first()
    if prod:
        cantidad = int(prod.stock) + int(instance.cant)
        prod.stock = cantidad
        prod.latest_buy=fecha_compra
        prod.save()

@receiver(post_delete, sender=DetShopping)
def detail_shopping_delete(sender, instance, **kwargs):
    id_producto = instance.prod.id
    
    prod=Product.objects.filter(pk=id_producto).first()
    if prod:
        cantidad = int(prod.stock) - int(instance.cant)
        prod.stock = cantidad
        prod.save()



class Sale(BaseModel):
    cli = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_joined = models.DateField(default=datetime.now)
    earning = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    
    def __str__(self):
        return self.cli.names

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        super(Sale, self).save()


    def toJSON(self):
        item = model_to_dict(self)
        item['cli'] = self.cli.toJSON()
        item['subtotal'] = format(self.subtotal, '.2f')
        item['total'] = format(self.total, '.2f')
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['det'] = [i.toJSON() for i in self.detsale_set.all()]
        return item

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['id']

    @property
    def earnings(self):
        from .models import DetSale;
        fact_detail = DetSale.objects.filter(sale=self)
        total = 0
        for i in fact_detail:
            total = i.prc_earnings
            # print(total)
        return total


class DetSale(BaseModel):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    prod = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    earnings = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.prod.name

    @property
    def prc_earnings(self):
        res = self.prod.pvp_cmp * self.prod.cantidad
        print(self.prod.pvp_cmp)
        print(self.prod.cantidad)
        return self.prod.costo_venta - res

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_updated = user
        super(DetSale, self).save()


    def toJSON(self):
        item = model_to_dict(self, exclude=['sale'])
        item['prod'] = self.prod.toJSON()
        item['price'] = format(self.price, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalle de Ventas'
        ordering = ['id']


@receiver(post_save, sender=DetSale)
def detalle_fac_guardar(sender,instance,**kwargs):
    product_id = instance.prod.id

    prod=Product.objects.filter(pk=product_id).first()
    if prod:
        quantity = int(prod.stock) - int(instance.cant)
        prod.stock = quantity
        prod.save()

@receiver(post_delete, sender=DetSale)
def detalle_fac_delete(sender,instance,**kwargs):
    product_id = instance.prod.id

    prod=Product.objects.filter(pk=product_id).first()
    if prod:
        quantity = int(prod.stock) + int(instance.cant)
        prod.stock = quantity
        prod.save()