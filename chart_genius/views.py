from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.conf import settings
from .models import UploadedDataset
import pandas as pd
import google.generativeai as genai
import os
import json
import subprocess

# Configure Gemini AI
genai.configure(api_key=settings.GOOGLE_API_KEY)

def upload_analyze_page(request):
    return render(request, "chart.html")

def upload_dataset(request):
    """
    Handles file upload and stores dataset.
    """
    if request.method == "POST":
        print("Uploading dataset")
        file = request.FILES.get("file")
        print("Received file:", request.FILES)
        if not file:
            return JsonResponse({"error": "No file provided"}, status=400)

        dataset = UploadedDataset.objects.create(file=file)
        return JsonResponse({"dataset_id": dataset.id, "filename": dataset.file.name})
    return JsonResponse({"error": "Invalid request method!"}, status=405)

def analyze_dataset(request, dataset_id):
    """
    Handles user queries: generates AI Python code using the entire CSV file,
    removes the first and last lines of the generated code, executes it,
    deletes the temporary file, and returns the output in a JSON object
    with only one key "text".
    """
    dataset = get_object_or_404(UploadedDataset, id=dataset_id)
    csv_file_path = dataset.file.path

    try:
        df = pd.read_csv(csv_file_path)
    except Exception as e:
        return JsonResponse({"error": f"Error reading dataset: {str(e)}"}, status=500)

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            question = data.get("question", "").strip().lower()

            if not question:
                return JsonResponse({"error": "No question provided!"}, status=400)

            # AI Generates Python Code using the full dataset
            model = genai.GenerativeModel("models/gemini-1.5-flash")
            prompt = (
                f"Generate Python code for analyzing the entire dataset stored at: {csv_file_path}.\n"
                f"Dataset:\n{df.to_string()}\n"
                f"User Query: {question}\n"
                f"Only return the code, no explanation."
                f"for tables use matplt (recommended)"
            )
            response = model.generate_content(prompt)
            generated_code = response.text if response else "# AI could not generate code."
            print("Generated Code:\n", generated_code)

            # Process Code: Remove the first and last lines
            code_lines = generated_code.split("\n")
            if len(code_lines) > 2:
                cleaned_code = "\n".join(code_lines[1:-2])
            else:
                cleaned_code = generated_code  # fallback if there are not enough lines

            print("Cleaned Code:\n", cleaned_code)

            # Save Cleaned Code to a temporary Python file
            script_path = os.path.join(settings.MEDIA_ROOT, "generated_script.py")
            with open(script_path, "w") as script_file:
                script_file.write(cleaned_code)

            # Execute the Script
            try:
                output = subprocess.check_output(["python", script_path], universal_newlines=True)
            except subprocess.CalledProcessError as e:
                output = f"Error executing script: {str(e)}"

            # Delete the temporary script file
            os.remove(script_path)

            # Return a JSON object with only one key "text" containing the output
            return JsonResponse({"text": output})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format!"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Server Error: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request method!"}, status=405)
