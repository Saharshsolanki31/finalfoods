from django.contrib import admin

# Register your models here.
from user.models import user, cart, address, user_order_item, order_history, user_order_id

admin.site.register(user)
admin.site.register(address)
admin.site.register(cart)
admin.site.register(user_order_id)
admin.site.register(order_history)
admin.site.register(user_order_item)