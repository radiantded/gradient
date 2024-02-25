from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from home.utils import main
from home.templates.pages.table_base import html_string


# Create your views here.

def index(request):
    context = {"result": ""}
    if not request.user.is_authenticated:
        return redirect('auth_signin')
    if request.method == 'POST' and request.FILES:
        file = request.FILES['file']
        dataset = main(file)
        print(dataset)
        table = html_string.format(table=dataset)
        # with open("home/templates/pages/dataset.html", "w", encoding="utf8") as f:
        #     f.write(table)
        context = {"result": dataset}
        # return HttpResponse(table)
        # context = {"result": dataset}
    return render(request, 'pages/index.html', context=context)
