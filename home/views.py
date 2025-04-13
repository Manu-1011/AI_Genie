from django.shortcuts import render

def home(request):
    return render(request, 'home.html')
'''<!--<a href="{% url 'chart_genius:index' %}" class="feature-card">📊 Chart Genius</a>
             Future AI tools can be added here -->'''