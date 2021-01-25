import csv

from django.shortcuts import render
from .models import Ingredients, OrderDetails
from django.http import HttpResponse
from .forms import OrdersForm



# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "index.html")


def menu(request):
    return render(request, "menu.html")


def ingredient_list(request):
    name = 'aki'
    ing = Ingredients.objects.all()
    ##for i in ing:
    ##    print(i.category)
    return render(request, 'db.html', {'names': ing})


def exportCSV(request):
    response = HttpResponse(content_type='text/csv')
    writer =csv.writer(response)
    writer.writerow(['Order ID', 'Ingredient ID', 'Transaction Date', 'Quantity'])
    for orderD in OrderDetails.objects.all().values_list('order_id', 'ingredient_id', 'transaction_date', 'quantity'):
        writer.writerow(orderD)

    response['Content-Disposition'] = 'attachment; filename="OrderDetails.csv"'

    return response


def order_details(request):
    #orders = OrderDetails.objects.all()
    if request.method== 'POST':
        form = OrdersForm(request.POST)
        fromdate = request.POST.get("fromdate")
        todate = request.POST.get("todate")
        searchresult = OrderDetails.objects.filter(transaction_date__gte=fromdate, transaction_date__lte=todate)
        return render(request, 'db.html', {'orderDetails': searchresult})
    else:
        now = '2021-01-01'
        orders = OrderDetails.objects.all()
        OrderDetails
        return render(request, 'db.html', {'orderDetails': orders})
