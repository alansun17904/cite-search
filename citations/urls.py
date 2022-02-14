from django.urls import path, re_path
from citations.views import IndexView, GraphView

app_name = 'citations'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    re_path(r'results/(?P<query>.*)', GraphView.as_view(), name='result')
]
