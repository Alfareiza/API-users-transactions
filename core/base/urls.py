from rest_framework.routers import DefaultRouter

from core.base.views import TransactionsViewSet

router = DefaultRouter()
router.register(r'', TransactionsViewSet, basename='transactions')

transactions_urls = router.urls
