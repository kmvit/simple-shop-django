from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.html import mark_safe

LABEL = (
	('primary','Новинка'),
	('danger','Горячее'),
)

class Item(models.Model):
	"""Товары"""
	title = models.CharField(max_length=100)
	slug = models.SlugField(default='product')
	price = models.FloatField(verbose_name='Цена')
	discount_price = models.FloatField(blank=True, null=True, verbose_name='Скидка')
	description = models.TextField('Описание')
	label_item = models.CharField(max_length=10, choices=LABEL, verbose_name='Лэйбл')
	category_item = models.ForeignKey('CategoryItem', verbose_name='Категория товара',
	                                  on_delete=models.SET_NULL,
	                                  blank=True,
	                                  null=True)
	brend_item = models.ForeignKey('BrendItem',
	                                  verbose_name='Бренд товара',
	                                  on_delete=models.SET_NULL,
	                                  blank=True, null=True)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('core:product', kwargs={
			'slug':self.slug
		})

	def get_add_to_cart_url(self):
		return reverse('core:add-to-cart', kwargs={
			'slug': self.slug
		})

	def get_remove_from_cart_url(self):
		return reverse('core:remove-from-cart', kwargs={
			'slug': self.slug
		})
	def get_characters(self):
		return f'{"".join([p.title for p in self.character_item.all()])}' \
		       f' - {"".join([p.description for p in self.character_item.all()])}'


	def get_first_image(self):
		"""Показ первой картинки"""
		image = self.itemimage_set.all().first()
		return image



class ImageItem(models.Model):
	image = models.ImageField(upload_to='item', verbose_name="Изображение")
	item = models.ForeignKey(Item, verbose_name='Товара',
	                         on_delete=models.SET_NULL,
	                         blank=True, null=True, related_name='images')
	class Meta:
		verbose_name = 'Изображение товара'
		verbose_name_plural = 'Изображения товара'

	def __str__(self):
		return self.image.name

	def get_first_image(self, obj):
		return obj.image.first()


	def thumbnail(self):
		return mark_safe('<img src="%s" height="150" width="150"/>' % (self.image.url))

	thumbnail.short_description = 'Изображение'




class CategoryItem(models.Model):
	"""Категория товара"""
	title = models.CharField(max_length=100, verbose_name='Категория товара')
	slug = models.SlugField(unique=True, verbose_name='url')

	class Meta:
		verbose_name = 'Категории товара'
		verbose_name_plural = 'Категория товара'

	def __str__(self):
		return self.title

class CharacterItem(models.Model):
	"""Характеристики товара"""
	title = models.CharField(max_length=100, verbose_name='Название')
	description = models.CharField(max_length=100, verbose_name='Значение')

	class Meta:
		verbose_name = 'Характеристики товара'
		verbose_name_plural = 'Характеристика товара'

	def __str__(self):
		return self.title

class BrendItem(models.Model):
	"""Бренд товара"""
	title = models.CharField(max_length=100, verbose_name='Название')

	class Meta:
		verbose_name = 'Бренд товара'
		verbose_name_plural = 'Бренды'

	def __str__(self):
		return self.title

class OrderItem(models.Model):
	"""Элементы корзины пользователя"""
	user = models.ForeignKey(settings.AUTH_USER_MODEL,
	                         on_delete=models.CASCADE, verbose_name='Пользователь')

	item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name='Продукт')
	quantity = models.IntegerField(default=1, verbose_name='Количество')
	ordered = models.BooleanField(default=False, verbose_name='Заказал')

	def __str__(self):
		return f'{self.item.title} - {self.quantity} шт '

	def get_total_item_price(self):
		return self.quantity * self.item.price

	def get_total_discount_item_price(self):
		return self.quantity * self.item.discount_price

	def get_amount_saved(self):
		return int(self.get_total_item_price() - self.get_total_discount_item_price())

	def get_final_price(self):
		if self.item.discount_price:
			return self.get_total_discount_item_price()
		else:
			return self.get_total_item_price()



class Order(models.Model):
	"""Корзина пользователя"""
	user = models.ForeignKey(settings.AUTH_USER_MODEL,
	                         on_delete=models.CASCADE , verbose_name='Пользователь')
	items = models.ManyToManyField(OrderItem, verbose_name='Товары')
	start_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата начала')
	ordered_date = models.DateTimeField('Дата покупки')
	ordered = models.BooleanField(default=False, verbose_name='Заказал')
	billing_address = models.ForeignKey('BillingAddress', on_delete=models.SET_NULL, blank=True, null=True)
	payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)

	def __str__(self):
		return f'{self.user.username} - {self.start_date}'


	def get_total(self):
		total = 0
		for order_item in self.items.all():
			total += order_item.get_final_price()
		return total


class BillingAddress(models.Model):
	"""Данные о заказах пользователей"""
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	city = models.CharField(max_length=100)
	street_address = models.CharField(max_length=100)
	zip = models.CharField(max_length=100)
	name = models.CharField(max_length=100)
	phone = models.CharField(max_length=100)

	def __str__(self):
		return self.user.username


class Payment(models.Model):
	stripe_charge_id = models.CharField(max_length=50)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
	amount = models.FloatField()
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.user.username
