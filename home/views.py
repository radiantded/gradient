from datetime import datetime

from django.http import FileResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from home.forms import OzonForm, YandexForm, WildberriesForm
from home.utils import ozon, round_values, yandex, wildberries


@login_required(login_url='/accounts/auth-signin/')
def index(request):
    ozon_form = OzonForm()
    context = {"ozon": ozon_form}
    if request.method == 'POST' and request.FILES:
        try:
            period = request.POST.get("period")
            file_1 = request.FILES['file_1']
            file_2 = request.FILES['file_2']
            ozon_form = OzonForm(request.FILES)
            abc, blocks, dataframe = ozon(file_1, file_2, period)
        except Exception as ex:
            print(ex)
            return render(request, 'pages/index.html', context=context)
        file_name = f"ozon-{int(datetime.timestamp(datetime.now()))}.xlsx"
        dataframe.to_excel(f"media/{file_name}")
        table = dataframe.values.tolist()[:5]
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
            "ozon": ozon_form,
            "file_name": file_name,
        }
    return render(request, 'pages/index.html', context=context)


@login_required(login_url='/accounts/auth-signin/')
def yandex_index(request):
    yandex_form = YandexForm()
    context = {"yandex": yandex_form}
    if request.method == 'POST' and request.FILES:
        try:
            united = request.FILES['united']
            mp_services = request.FILES['mp_services']
            netting = request.FILES['netting']
            sebes = request.FILES['sebes']
            yandex_form = YandexForm(request.POST, request.FILES)
            period = request.POST.get("period")
            abc, blocks, dataframe = yandex(united, mp_services, netting, sebes, period)
        except Exception as ex:
            print(ex)
            return render(request, 'pages/index.html', context=context)
        file_name = f"yandex-{int(datetime.timestamp(datetime.now()))}.xlsx"
        dataframe.to_excel(f"media/{file_name}")
        table = dataframe.values.tolist()[:6]
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
            "yandex": yandex_form,
            "file_name": file_name,
        }
    return render(request, 'pages/index.html', context=context)


login_required(login_url='/accounts/auth-signin/')
def wb_index(request):
    wb_form = WildberriesForm()
    context = {"wb": wb_form}
    if request.method == 'POST' and request.FILES:
        try:
            main = request.FILES['main']
            hran = request.POST['hran']
            reklama = request.POST['reklama']
            sebes = request.FILES['sebes']
            wb_form = WildberriesForm(request.POST, request.FILES)
            abc, blocks, dataframe = wildberries(main, hran, reklama, sebes)
        except Exception as ex:
            print(ex)
            return render(request, 'pages/index.html', context=context)
        file_name = f"wb-{int(datetime.timestamp(datetime.now()))}.xlsx"
        dataframe.to_excel(f"media/{file_name}")
        table = dataframe.values.tolist()[:5]
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
            "wb": wb_form,
            "file_name": file_name,
        }
    return render(request, 'pages/index.html', context=context)



@login_required(login_url='/accounts/auth-signin/')
def faq_ozon(request):
    return render(request, 'pages/faq_ozon.html')


@login_required(login_url='/accounts/auth-signin/')
def faq_yandex(request):
    return render(request, 'pages/faq_yandex.html')


@login_required(login_url='/accounts/auth-signin/')
def faq_wb(request):
    return render(request, 'pages/faq_wb.html')


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