
from initial import views
from django.urls import path


urlpatterns = [
    path("", views.home,name='home'),
    path("works/", views.works,name='works'),
    path("feature/", views.feature,name='feature'),
    path("pricing/", views.pricing,name='pricing'),
    path("analyzer/",views.analyzer,name='analyzer'),
]


# serve uploaded media files (resume PDFs) — works in both dev and production
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)