from listings.views import initiate_payment, verify_payment

urlpatterns = [
    path("api/initiate-payment/", initiate_payment),
    path("api/verify-payment/", verify_payment),
]
