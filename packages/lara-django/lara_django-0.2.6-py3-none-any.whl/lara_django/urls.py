"""________________________________________________________________________

:PROJECT: lara-django

*lara-django base settings*

:details: lara URL Configuration.

    The `urlpatterns` list routes URLs to views. For more information please see:
        https://docs.djangoproject.com/en/2.0/topics/http/urls/
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


:authors: mark doerr (mark@uni-greifswald.de)

:date: (creation)          20180623
:date: (last modification) 20190630

.. note:: -
.. todo:: -
________________________________________________________________________

**Copyright**:
  This file is provided "AS IS" with NO WARRANTY OF ANY KIND,
  INCLUDING THE WARRANTIES OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

  For further Information see LICENSE file that comes with this distribution.
________________________________________________________________________
"""

__version__ = "0.1.7"

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

#from lara_base.views import HomeMenu, SignUp

#~ from sila_device_manager.views import hello, current_datetime

app_name = 'lara-django' # !! this sets the apps namespace to be used in the template

admin.site.site_header = "LARA Administration"
admin.site.site_title = "LARA Admin"
admin.site.index_title = "Welcome to LARA Administration"

urlpatterns = [
#    path('', HomeMenu.as_view(), name='index'),
    path('', include('lara_base.urls')),
    path('admin/', admin.site.urls),
#    path('signup/', SignUp.as_view(), name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('people/', include('lara_people.urls') ),
    path('substances/', include('lara_substances.urls')),
    path('labstore/', include('lara_substances_store.urls')),
    path('devices/', include('lara_devices.urls')),
    path('data/', include('lara_data.urls')),
    path('processes/', include('lara_processes.urls')),
    path('containers/', include('lara_containers.urls')),
    path('projects/', include('lara_projects.urls')),
    path('devices/', include('lara_devices.urls')),
    #~ path(r'time/', current_datetime),
]
