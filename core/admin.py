from django.contrib import admin
from .models import *
from django.utils.html import format_html
from django.utils.html import mark_safe



class OrderAdmin(admin.ModelAdmin):
	readonly_fields = ('get_total',)

	def get_total(self, obj):
		return f'{obj.get_total()} {"руб."}'


class ImageItemInline(admin.TabularInline):
	model = ImageItem
	extra = 0
	readonly_fields = ['thumbnail']



class ItemAdmin(admin.ModelAdmin):
	exclude = ('image',)
	inlines = (
		ImageItemInline,
	)
	raw_id_fields = ('category_item',)





admin.site.register(Item, ItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(BillingAddress)
admin.site.register(CategoryItem)
admin.site.register(CharacterItem)
admin.site.register(ImageItem)
admin.site.register(BrendItem)
