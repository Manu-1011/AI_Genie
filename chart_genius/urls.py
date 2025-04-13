from django.urls import path
from .views import upload_analyze_page, upload_dataset, analyze_dataset
app_name = 'chart_genius'
urlpatterns = [
    path('', upload_analyze_page, name='upload_analyze'),
    path('upload/', upload_dataset, name='upload_dataset'),
    path('analyze/<int:dataset_id>/', analyze_dataset, name='analyze_dataset'),
]
