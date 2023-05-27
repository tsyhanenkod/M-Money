from django.urls import path, include
from . import views

urlpatterns = [
    path('history/', views.HistoryView.as_view(), name='history'),
    path('history/<int:transaction_id>/', views.DeleteTransaction.as_view(), name='delete_transaction'),
]
