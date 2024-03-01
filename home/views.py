import os.path
from pprint import pprint

import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from core.settings import BASE_DIR, MEDIA_ROOT
from home.forms import UploadFileForm
from home.utils import main, round_values
from django.core.files.storage import FileSystemStorage



# @login_required(login_url='/accounts/auth-signin/')
def index(request):
    if request.method == 'GET':
        form = UploadFileForm()
        context = {"form": form}
    # if not request.user.is_authenticated:
    #     return redirect('auth_signin')
    elif request.method == 'POST' and request.FILES:
        try:
            period = request.POST.get("period")
            file_1 = request.FILES['file_1']
            file_2 = request.FILES['file_2']
            form = UploadFileForm(request.FILES)
            abc, blocks, dataframe = main(file_1, file_2, period)
        except:
            return render(request, 'pages/index.html')
        try:
            dataframe.to_excel("media/dataframe.xlsx")
        except:
            pass
        table = dataframe.values.tolist()[:3]
        table = round_values(table)
        abc = round_values(abc.values.tolist())

        context = {
            "data": abc,
            "table": table,
            "orders": round(blocks["orders"]),
            "revenue": round(blocks["revenue"]),
            "roi": round(blocks["roi"]),
            "returns": round(blocks["returns"]),
            "profit": round(blocks["profit"]),
            "purchase": round(blocks["purchase"]),
            "form": form
        }

    return render(request, 'pages/index.html', context=context)


def download(request):
    try:
        with open("media/dataframe.xlsx", "rb") as file:
            response = HttpResponse(file.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'attachment; filename=dataframe.xlsx'
            return HttpResponse(response)
    except:
        return render(request, 'pages/index.html')