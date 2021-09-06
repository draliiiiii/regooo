"""regois URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from clinic import views
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from dal import autocomplete

from clinic.models import Diagnosis

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'^select2/', include('django_select2.urls')),
    path("", views.PtList.as_view(),name="pt-list"),
    path("diagnoo-auoto/", views.DigAutocomplete.as_view(create_field="namee"),name="diagnoo-auoto"),
    path('upload/',views.upload,name="upload"),
    path('list/',views.record_list,name="list"),
    path('delete/<int:pk>/',views.delete,name="delete"),
    path('ocr/<int:pk>',views.ocr,name="ocr"),
    path('view/<int:pk>/' , views.view , name="view"),
    path('download/<int:pk>/' , views.download , name="download"),
    path('xray/' , views.xray , name="xray"),
    path('xray_list/',views.xray_list,name="xray_list"),
    path('xray_delete/<int:pk>/',views.xray_delete,name="xray_delete"),
    path("visit-ad/", views.VisCreate.as_view(),name="visit-ad"),
    path('visit/<int:patient_id>', views.PatientVisitCreate.as_view(),name="visit-auoto"),
    url(
    'test-autocomplete/$',
    autocomplete.Select2QuerySetView.as_view(
        model=Diagnosis,
        create_field='name',
    ),
    name='select2_one_to_one_autocomplete',
),
    path("bacup-ad/", views.Step2View.as_view(),name="back-ad"),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from django.contrib import admin

admin.autodiscover()
admin.site.enable_nav_sidebar = False
