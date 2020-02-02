from . import views
from django.conf.urls import url

urlpatterns = [

    # register a new user and return user id
    url(r'^register$', views.register_user),

    # add a new data entry to db, return the calculated health score
    # need to specify userid and day count
    url(r'^add$',views.add_entry),

    # retrieve similar cases
    url(r'^similar/(?P<userid>[\w]+)/(?P<limit>[\w]+)$', views.get_similar)


]