
.. image:: images/dkm-logo.png
   :width: 600
   :alt: DjangoKubernetesManager


Django Kubernetes Manager is an ongoing project to wrap the complexity of Kubernetes management in the simplicity of Django Rest Framework.

License
--------
This project is license under the MIT license. Please see the license dir for
dependency licenses.

Docs
-------
API_


Full_


.. _API: https://github.com/IntrospectData/Django-Kubernetes-Manager/blob/master/docs/openapi.md

.. _Full: https://django-kubernetes-manager.readthedocs.io/en/latest/index.html


Installation
---------------
Install the app using pip::

  $ pip install django-kubernetes-manager

Getting Started
---------------
1. Add "django_kubernetes_manager" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'django_kubernetes_manager',
    ]

2. Include the django_kubernetes_manager URLconf in your project urls.py like this::

    path('dkm/', include('django_kubernetes_manager.urls')),

3. To create models in your database, run::
  
    python manage.py migrate

    * Requires Postgresql or other database with JSON support.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to configure a TargetCluster (you'll need the Admin app enabled).

5. Create, update, delete, deploy, or remove a Kubernetes object
   using the api :)
