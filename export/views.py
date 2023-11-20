from django.core.paginator import Paginator
from django.shortcuts import render
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse, JsonResponse
from export.models import UserInfo
import openpyxl
import razorpay
from django.conf import settings

# Create your views here.
def create(request):
    l = [{"name":'Raju'+str(x), "email":'raju'+str(x)+'@gmail.com', "age":10+x} for x in range(1,50)]
    for item in l:
        user = UserInfo()
        user.name = item['name']
        user.email = item['email']
        user.age = item['age']
        user.save()
    return render(request, 'export/home.html')


def index(request):
    users = UserInfo.objects.all()
    # context = {
    #     'users': users
    # }
    paginator = Paginator(users, 10)  # Show 10 products per page
    page = request.GET.get('page')
    users = paginator.get_page(page)
    return render(request, 'export/home.html', {'users': users})

def export_to_pdf(request):
    template_path = 'export/home.html'  # Replace with the path to your HTML template
    # Add context data for your HTML template
    context = {
        'users': UserInfo.objects.all()
    } 

    template = get_template(template_path)
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="table_export.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Error while rendering PDF', status=400)

    return response

def export_to_excel(request):
    workbook = openpyxl.Workbook()
    worksheet = workbook.active

    # Add your data to the Excel worksheet
    # For example, assuming you have a list of data rows
    data = [["Name", "Email", "Age"]] + [[item.name, item.email, item.age] for item in UserInfo.objects.all()]
    

    for row in data:
        worksheet.append(row)

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="table_export.xlsx"'

    workbook.save(response)

    return response

def create_razorpay_order(request):
    client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
    data = {
        'amount': 10000,  # The amount is in paisa (e.g., 10000 paisa = 100 INR)
        'currency': 'INR',
        'receipt': 'order_rcptid_11',
    }

    order = client.order.create(data)
    return JsonResponse(order)

def razorpay_callback(request):
    response = request.POST
    client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
    try:
        client.utility.verify_payment_signature(response)
        # Payment successful, update your database or perform other actions
        return JsonResponse({'status': 'success'})
    except Exception as e:
        # Payment failed or signature verification failed
        return JsonResponse({'status': 'failure', 'error_message': str(e)})

def payment_view(request):
    return render(request, 'export/payment_form.html')

def payment_callback(request):
    # Handle payment verification here
    response_data = request.body
    # Perform payment verification and update your database as needed
    # Return a JSON response to acknowledge the payment
    return JsonResponse({'status': 'success'})
