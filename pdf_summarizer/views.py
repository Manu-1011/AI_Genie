import pdfplumber
import google.generativeai as genai
from django.conf import settings
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status, views
from .models import PDFDocument

# Set up Google AI
genai.configure(api_key=settings.GOOGLE_API_KEY)  # Make sure to store your API key securely in settings

from django.shortcuts import render

def index(request):
    return render(request, 'index.html')
class PDFSummarizerView(views.APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        file = request.FILES.get('file')

        if not file:
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        # Save uploaded file
        pdf_doc = PDFDocument.objects.create(file=file)

        # Extract text from the PDF
        text = ""
        with pdfplumber.open(pdf_doc.file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"

        if not text.strip():
            return Response({'error': 'No readable text found in PDF'}, status=status.HTTP_400_BAD_REQUEST)

        # Store extracted text in cache (Session-based)
        session_key = f"pdf_text_{request.session.session_key}"
        cache.set(session_key, text, timeout=3600)  # Store for 1 hour

        # Generate summary
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        response = model.generate_content(f"Summarize the following text:\n\n{text}")
        summary = response.text if response else "Could not generate summary."

        return Response({'summary': summary, 'session_key': request.session.session_key}, status=status.HTTP_200_OK)

class PDFQuestionAnswerView(views.APIView):
    def post(self, request):
        session_key = f"pdf_text_{request.session.session_key}"
        text = cache.get(session_key)

        if not text:
            return Response({'error': 'No PDF uploaded. Please upload a file first.'}, status=status.HTTP_400_BAD_REQUEST)

        question = request.data.get('question')
        if not question:
            return Response({'error': 'Please enter a question.'}, status=status.HTTP_400_BAD_REQUEST)

        # Generate answer using AI
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        response = model.generate_content(f"Based on the following text, answer this question:\n\nText: {text}\n\nQuestion: {question}")
        answer = response.text if response else "Could not generate an answer."

        return Response({'answer': answer}, status=status.HTTP_200_OK)