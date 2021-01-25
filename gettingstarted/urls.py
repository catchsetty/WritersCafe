from django.urls import path, include
from django.contrib import admin
from orders import views

admin.autodiscover()

import orders.views

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    path("orders/", include('orders.urls')),
    path("admin/", admin.site.urls),
    path("menu/", orders.views.menu, name="Menu"),
]
admin.site.site_header = 'Writer\'s Admin'
admin.site.site_title = 'Writer\'s Admin'
admin.site.index_title = 'Welcome to Writer\'s Cafe'

