from qr_code import urls as qr_code_urls

from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include

from book import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^$', views.index),
    url(r'^liste_terrariums/$', views.liste_terrariums),
    url(r'^ajouter_terrarium/$', views.ajouter_terrarium),
    url(r'^terrarium/(?P<identifiant>[0-9]*)/$', views.terrarium),
    url(r'^editer_terrarium/(?P<identifiant>[0-9]*)/$', views.editer_terrarium),
    url(r'^ajouter_maintenance/(?P<identifiant>[0-9]*)/$', views.ajouter_maintenance),
    url(r'^editer_maintenance/(?P<identifiant>[0-9]*)/$', views.editer_maintenance),
    url(r'^liste_specimens/$', views.liste_specimens),
    url(r'^ajouter_specimen/$', views.ajouter_specimen),
    url(r'^editer_specimen/(?P<identifiant>[0-9]*)/$', views.editer_specimen),
    url(r'^specimen/(?P<identifiant>[0-9]*)/$', views.specimen),
    url(r'^ajouter_repas/(?P<identifiant>[0-9]*)/$', views.ajouter_repas),
    url(r'^editer_repas/(?P<identifiant>[0-9]*)/$', views.editer_repas),
    url(r'^ajouter_mue/(?P<identifiant>[0-9]*)/$', views.ajouter_mue),
    url(r'^editer_mue/(?P<identifiant>[0-9]*)/$', views.editer_mue),
    url(r'^ajouter_mesure/(?P<identifiant>[0-9]*)/$', views.ajouter_mesure),
    url(r'^editer_mesure/(?P<identifiant>[0-9]*)/$', views.editer_mesure),
    url(r'^ajouter_emplacement/(?P<identifiant>[0-9]*)/$', views.ajouter_emplacement),
    url(r'^editer_emplacement/(?P<identifiant>[0-9]*)/$', views.editer_emplacement),
    url(r'^stock/$', views.stock),
    url(r'^ajouter_achat/$', views.ajouter_achat),
    url(r'^editer_achat/(?P<identifiant>[0-9]*)/$', views.editer_achat),
    url(r'^ajouter_photo/(?P<identifiant>[0-9]*)/$', views.upload_photo),
    url(r'^creer_carte/(?P<identifiant>[0-9]*)/$', views.creer_carte),
    url(r'^qr_code/', include(qr_code_urls, namespace='qr_code')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
