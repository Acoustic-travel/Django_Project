from django.shortcuts import render


import os
from django.shortcuts import redirect
from django.core.files.storage import FileSystemStorage
from .forms import CSVUploadForm

def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            fs = FileSystemStorage()
            filename = fs.save(csv_file.name, csv_file)
            uploaded_file_url = fs.url(filename)
            return redirect('analyze_data', filename=filename)
    else:
        form = CSVUploadForm()
    return render(request, 'upload.html', {'form': form})

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64

def analyze_data(request, filename):
    file_path = os.path.join('media', filename)
    df = pd.read_csv(file_path)
    
    # Basic analysis
    summary = df.describe().to_html()
    head = df.head().to_html()
    missing_values = df.isnull().sum().to_frame().to_html()
    
    # Generate plots
    plots = []
    for column in df.select_dtypes(include=['int64', 'float64']).columns:
        plt.figure(figsize=(10, 5))
        sns.histplot(df[column], kde=True)
        plt.title(f'Histogram of {column}')
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        graph = base64.b64encode(image_png)
        graph = graph.decode('utf-8')
        plots.append(graph)
        plt.close()
    
    context = {
        'summary': summary,
        'head': head,
        'missing_values': missing_values,
        'plots': plots,
    }
    return render(request, 'analysis.html', context)