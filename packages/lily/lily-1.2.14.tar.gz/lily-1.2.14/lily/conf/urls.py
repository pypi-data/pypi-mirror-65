
from django.conf.urls import url, include

urlpatterns = [

    url(
        r'^',
        include(('entrypoint.urls', 'entrypoint'), namespace='entrypoint')),

]
