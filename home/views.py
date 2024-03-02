import os.path
from datetime import datetime
from pprint import pprint

import pandas as pd
from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# from rest_framework.response import FileResponse

from core.settings import BASE_DIR, MEDIA_ROOT
from home.forms import UploadFileForm
from home.utils import main, round_values
from django.core.files.storage import FileSystemStorage



@login_required(login_url='/accounts/auth-signin/')
def index(request):
    form = UploadFileForm()
    context = {"form": form}
    if request.method == 'POST' and request.FILES:
        try:
            period = request.POST.get("period")
            file_1 = request.FILES['file_1']
            file_2 = request.FILES['file_2']
            form = UploadFileForm(request.FILES)
            abc, blocks, dataframe = main(file_1, file_2, period)
        except:
            return render(request, 'pages/index.html')
        # try:
        file_name = f"data-{int(datetime.timestamp(datetime.now()))}.xlsx"
        dataframe.to_excel(f"media/{file_name}")
        # except:
        #     pass
        table = dataframe.values.tolist()[:3]
        table = round_values(table, to_int=False)
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
            "form": form,
            "file_name": file_name,
        }
    # pprint(context)
    return render(request, 'pages/index.html', context=context)


def download(request, file_name):
    try:
        file = open(f"media/{file_name}", "rb")
        response = FileResponse(
            file,
            as_attachment=True
        )
        response['Content-Disposition'] = f'attachment; filename={file_name}'
        return response
    except:
        return render(request, 'pages/index.html')