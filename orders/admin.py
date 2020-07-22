from django.contrib import admin
from .models import Category, Ingredients, Suppliers, Status, Orders, OrderDetails, Stock, CashRecord, CashRecordDetail

# Register your models here.
admin.site.register(Category)
admin.site.register(Suppliers)
admin.site.register(Status)
admin.site.register(Stock)
admin.site.register(Ingredients)
admin.site.register(OrderDetails)


class OrderDetailsInline(admin.TabularInline):
    model = OrderDetails
    readonly_fields = ['measurement', 'item_total']
    exclude = ['itemTotal'] # To not to display db column

    def measurement(self, obj):
        return str(obj.ingredient_id.per)

    def item_total(self, obj):
        return str(obj.quantity * obj.unitPrice)
    item_total.short_description = ("TOTAL")


# Define the Order class
@admin.register(Orders)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'ordered_by', 'order_status', 'ordered_date')
    inlines = [OrderDetailsInline]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["ordered_by", "order_status"]
        else:
            return []

    def save_model(self, request, obj, form, change):
        if not obj.pk: #only sets ordered_by during the first save
            obj.ordered_by = str(request.user)
        super().save_model(request, obj, form, change)


class CashRecordDetailInline(admin.TabularInline):
    model = CashRecordDetail


@admin.register(CashRecord)
class CashRecordAdmin(admin.ModelAdmin):
    inlines = [CashRecordDetailInline]
