from django.urls import path, include
from . import views
from transaction.views import *

urlpatterns = [
    path('accounts/', views.AccountsView.as_view(), name='accounts'),
    path('accounts/payment', views.PaymentView.as_view(), name='payment'),
    path('accounts/create', views.CreateView.as_view(), name='create'),
    path('accounts/', include('transaction.urls')),
    path('accounts/edit/<int:id>/', views.AccountEditView.as_view(), name='account_edit'),
    path('accounts/transaction/<int:transaction_id>/', DeleteTransaction.as_view(), name='delete_transaction'),
    path('accounts/transaction/edit/<int:transaction_id>/', EditTransaction.as_view(), name='edit_transaction'),

]