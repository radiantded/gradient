from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from home.utils import main
from home.templates.pages.table_base import html_string

# Create your views here.

def index(request):
    context = {"result": ""}
    if request.method == 'POST' and request.FILES:
        file = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        dataset = main(filename)
        table = html_string.format(table=dataset)
        with open("home/templates/pages/dataset.html", "w", encoding="utf8") as f:
            f.write(table)
            return render(request, "pages/dataset.html")
        # context = {"result": dataset}
    return render(request, 'pages/index.html', context=context)
