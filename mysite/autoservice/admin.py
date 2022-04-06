from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from .models import Service, CarModel, Car, Order, OrderLine, Profilis, OrderComment

class OrderLineInline(admin.TabularInline):
    model = OrderLine
    extra = 0 # išjungia placeholder'ius

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderLineInline]
    list_display = ('car', 'due_date', 'is_overdue')

class CarAdmin(admin.ModelAdmin):
    list_display = ('owner', 'car_model', 'licence_plate', 'vin_code')
    list_filter = ('owner', 'car_model')
    search_fields = ('licence_plate', 'vin_code')


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('order', 'user', 'date_created')

admin.site.register(Profilis)
admin.site.register(Service, ServiceAdmin)
admin.site.register(CarModel)
admin.site.register(Car, CarAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderLine)
admin.site.register(OrderComment, CommentAdmin)