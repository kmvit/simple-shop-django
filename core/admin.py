from django.contrib import admin
from .models import Item, OrderItem, Order, BillingAddress,Payment

class OrderAdmin(admin.ModelAdmin):
	readonly_fields = ('get_total',)

	def get_total(self, obj):
		return f'{obj.get_total()} {"руб."}'

admin.site.register(Item)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(BillingAddress)