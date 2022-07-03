
from django.urls import path
from .views import *
from graphene_django.views import GraphQLView
from .schema import schema

urlpatterns = [
    path('' , login_attempt , name="login"),
    path('register', register, name= "register"),
    path('otp' , otp , name="otp"),
    path('login-otp', login_otp , name="login_otp"), 
    path('cart' , cart , name="cart"),
    path("graphql", GraphQLView.as_view(graphiql=True, schema=schema)),
    path('details_product/<int:pk>',details_product,name='details_product'),

]
