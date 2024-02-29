from pprint import pprint

import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from home.utils import main
from home.templates.pages.table_base import html_string


# Create your views here.
# @login_required(login_url='/accounts/auth-signin/')
def index(request):
    context = {"result": ""}
    print(request.user.is_authenticated)
    # if not request.user.is_authenticated:
    #     return redirect('auth_signin')
    if request.method == 'POST' and request.FILES:
        # print(request.FILES)
        # company = request.POST.get("company")
        period = request.POST.get("period")
        file_1 = request.FILES['file_1']
        file_2 = request.FILES['file_2']
        print(file_1, file_2)
        dataset, blocks = main(file_1, file_2, period)
        print(dataset)
        # table = html_string.format(table=dataset)
        # # with open("home/templates/pages/dataset.html", "w", encoding="utf8") as f:
        # #     f.write(table)
        # context = {
        #     "sku": dataset["SKU"],
        #     "sales": dataset["Продажи"],
        #     "amount": dataset["Кол-во"]
        # }

        # result = []
        # for val in dataset.to_json().values():
        #     for inner_val in val.values():
        #         result.append(inner_val)

        # print(dataset.columns)
        context = {
            "data": dataset.values.tolist(),
            "orders": round(blocks["orders"]),
            "revenue": round(blocks["revenue"]),
            "roi": round(blocks["roi"]),
            "returns": round(blocks["returns"]),
            "profit": round(blocks["profit"]),
            "purchase": round(blocks["purchase"])

        }
        print(context)
        # return HttpResponse(table)
        # context = {"result": dataset}
    return render(request, 'pages/index.html', context=context)
