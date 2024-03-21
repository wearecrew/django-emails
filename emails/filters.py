from django.contrib import admin


class DeliveredFilter(admin.SimpleListFilter):
    title = "Delivered"

    parameter_name = "delivered"

    def lookups(self, request, model_admin):
        return [
            ("yes", "Yes"),
            ("no", "No"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "yes":
            return queryset.filter(delivered__gte=1)
        if self.value() == "no":
            return queryset.filter(delivered=0)
