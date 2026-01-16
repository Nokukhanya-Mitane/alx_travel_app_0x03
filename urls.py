from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from listings.views import initiate_payment, verify_payment

schema_view = get_schema_view(
   openapi.Info(
      title="ALX Travel API",
      default_version='v1',
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns += [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
    path("api/initiate-payment/", initiate_payment),
    path("api/verify-payment/", verify_payment),
]
