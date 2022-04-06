from django.urls import path, include

from . import views

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('', views.index, name='index'),
    path('cars/', views.cars, name="cars"),
    path('car/<int:car_id>', views.car, name='car'),
    path('order/', views.OrderListView.as_view(), name='orders'),
    path('search/', views.search, name='search'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('Profilis/', views.profilis, name='profilis'),
    path('user_order/', views.UserOrderListView.as_view(), name='user-orders'),
    path('order/<int:pk>', views.OrderDetailView.as_view(), name='order-detail'),
    path('order/new', views.OrderByUserCreateView.as_view(), name='user-order-new'),
    path('order/<int:pk>/orderline/new', views.OrderLineByUserCreateView.as_view(), name='user-orderline-new'),
    path('order/<int:pk>/update', views.OrderByUserUpdateView.as_view(), name='user-order-update'),
    path('order/<int:pk>/delete', views.OrderByUserDeleteView.as_view(), name='user-order-delete'),

]