from django.urls import path
from .views import PDFSummarizerView, index, PDFQuestionAnswerView
app_name = 'pdf_summarizer'
urlpatterns = [
    path('', index, name='index'),
    path('api/summarize/', PDFSummarizerView.as_view(), name='pdf_summarizer'),
    path('api/ask-question/', PDFQuestionAnswerView.as_view(), name='ask_question'),
]
