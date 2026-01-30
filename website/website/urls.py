# myproject/urls.py
from django.contrib import admin
from django.urls import path

from home.views import index, bisadijual, simpan, hapus

urlpatterns = [
    path('', index, name='index'),  # Root URL
    path('produk', index, name='index'),  # Root URL
    path('bisadijual', bisadijual, name='bisadijual'),  # Root URL
    path('simpan', simpan, name='simpan'),  # Root URL
    path('hapus', hapus, name='hapus'),  # Root URL

    path('admin/', admin.site.urls),
]
