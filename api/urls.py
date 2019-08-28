from django.urls import path, include
# from django.conf.urls import url

# from rest_framework.documentation import include_docs_urls

urlpatterns = [
    # url(r'^docs/', include_docs_urls(title='API Documentation', public=True)),

    path('notifier/', include("notifier.api.urls")),
]

