import csv
import json
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import FormMixin
from openpyxl.workbook import Workbook
from django.views import View
from blog.models import Product
from ..forms import CustomerModelForm, ProductListModelForm
from ..models import Customer
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView, DetailView


# Create your views here.

# class ProductCreate(ListView):
#     # paginator_by = 5
#     form_class = ProductListModelForm
#     model = Product
#     template_name = ''
#     success_url = ''

def index(request):
    products = Product.objects.all()
    paginator = Paginator(products, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'blog/index.html', context)

# class ProductList(View):
#     def get(self, request):
#         products = Product.objects.all()
#         paginator = Paginator(products, 2)
#         page_number = request.GET.get('page')
#         page_obj = paginator.get_page(page_number)
#         return render(request, 'blog/product/index.html', {'page_obj': page_obj})

class ProductListTemplateView(TemplateView):
    template_name = 'blog/product/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.all()
        paginator = Paginator(products, 2)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context["page_obj"] = page_obj
        return context


# def product_detail(request, slug):
#     product = Product.objects.get(slug=slug)
#     attributes = product.get_attributes()
#
#     context = {
#         'product': product,
#         'attributes': attributes
#     }
#     return render(request, template_name='blog/product-detail.html', context=context)

# class ProductDetailView(View):
#     def get(self, request, slug):
#         product = Product.objects.get(slug=slug)
#         attributes = product.get_attributes()
#         context = {
#             'product': product,
#             'attributes': attributes
#         }
#         return render(request, 'blog/product/product-detail.html', context)

class ProductDetailTemplateView(TemplateView):
    template_name = 'blog/product/product-detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        product = Product.objects.get(slug=kwargs['slug'])
        attributes = product.get_attributes()
        context['product'] = product
        context['attributes'] = attributes

        return context


# class ProductAddView(View):
#     def get(self, request):
#         form = ProductListModelForm()
#         return render(request, 'blog/product/add-product.html', {'form': form})
#
#     def post(self, request):
#         form = ProductListModelForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('index')
#
#         return render(request, 'blog/product/add-product.html', {'form': form})
class ProductAddTemplateView(TemplateView):
    template_name = 'blog/product/add-product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProductListModelForm()
        return context

    def post(self, request, *args, **kwargs):
        form = ProductListModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')


class ProductUpdateView(View):
    def get(self, request, slug):
        product = Product.objects.get(slug=slug)
        form = ProductListModelForm(instance=product)
        return render(request, 'blog/product/update-product.html', {'form': form})

    def post(self, request, slug):
        product = Product.objects.get(slug=slug)
        form = ProductListModelForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('index')

        return render(request, 'blog/product/update-product.html', {'form': form})




# def customers(request):
#     customers = Customer.objects.all()
#     paginator = Paginator(customers, 5)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)
#     search_query = request.GET.get('search')
#     if search_query:
#         page_obj = Customer.objects.filter(Q(name__icontains=search_query) | (Q(email__icontains=search_query)))
#     else:
#         customers = Customer.objects.all()
#     context = {
#
#         'page_obj': page_obj,
#     }
#     return render(request, 'blog/customer/customers.html', context)


# View
# class CustomersList(View):
#     template_name = 'blog/customer/customers.html'
#     paginate_by = 5
#
#     def get(self, request, *args, **kwargs):
#         customers = Customer.objects.all()
#         paginator = Paginator(customers, self.paginate_by)
#         page_number = request.GET.get("page")
#         page_obj = paginator.get_page(page_number)
#         search_query = request.GET.get('search')
#         if search_query:
#             customers = Customer.objects.filter(Q(name__icontains=search_query) | Q(email__icontains=search_query))
#             paginator = Paginator(customers, self.paginate_by)
#             page_obj = paginator.get_page(page_number)
#
#         context = {
#             'page_obj': page_obj,
#         }
#         return render(request, self.template_name, context)

# TemplateView
# class CustomersListTemplateView(TemplateView):
#     template_name = 'blog/customer/customers.html'
#     paginate_by = 5
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         request = self.request
#         customers = Customer.objects.all()
#         paginator = Paginator(customers, self.paginate_by)
#         page_number = request.GET.get("page")
#         page_obj = paginator.get_page(page_number)
#         search_query = request.GET.get('search')
#         if search_query:
#             customers = Customer.objects.filter(Q(name__icontains=search_query) | Q(email__icontains=search_query))
#             paginator = Paginator(customers, self.paginate_by)
#             page_obj = paginator.get_page(page_number)
#
#         context['page_obj'] = page_obj
#         return context


# ListView

class CustomersListView(ListView):
    model = Customer
    template_name = 'blog/customer/customers.html'
    context_object_name = 'page_obj'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(Q(name__icontains=search_query) | Q(email__icontains=search_query))
        return queryset


# def add_customer(request):
#     customers = Customer.objects.all()
#     if request.method == 'POST':
#         form = CustomerModelForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('customers')
#     else:
#         form = CustomerModelForm(request.GET)
#
#     context = {
#         'customers': customers,
#         'form': form
#     }
#     return render(request, 'blog/customer/add-customer.html', context)

# View
# class CustomerAddList(View):
#     template_name = 'blog/customer/add-customer.html'
#
#     def get(self, request, *args, **kwargs):
#         customers = Customer.objects.all()
#         form = CustomerModelForm()
#         context = {
#             'customers': customers,
#             'form': form
#         }
#         return render(request, self.template_name, context)
#
#     def post(self, request, *args, **kwargs):
#         customers = Customer.objects.all()
#         form = CustomerModelForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('customers')
#         context = {
#             'customers': customers,
#             'form': form
#         }
#         return render(request, self.template_name, context)

# TemplateView
# class CustomerAddTemplateView(TemplateView):
#     template_name = 'blog/customer/add-customer.html'
#
#     def get(self, request, *args, **kwargs):
#         customers = Customer.objects.all()
#         form = CustomerModelForm()
#         context = {
#             'customers': customers,
#             'form': form
#         }
#         return self.render_to_response(context)
#
#     def post(self, request, *args, **kwargs):
#         customers = Customer.objects.all()
#         form = CustomerModelForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('customers')
#         context = {
#             'customers': customers,
#             'form': form
#         }
#         return self.render_to_response(context)


# ListView
class CustomersAddListView(FormMixin, ListView):
    model = Customer
    template_name = 'blog/customer/add-customer.html'
    context_object_name = 'customers'
    form_class = CustomerModelForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            return redirect('customers')
        return self.render_to_response(self.get_context_data(form=form))




# def customers_detail(request, pk):
#     customers = Customer.objects.get(id=pk)
#     context = {
#         'customers': customers
#     }
#     return render(request, 'blog/customer/customer-details.html', context)

# View
# class CustomerDetailView(View):
#     template_name = 'blog/customer/customer-details.html'
#
#     def get(self, request, pk, *args, **kwargs):
#         customer = get_object_or_404(Customer, id=pk)
#         context = {
#             'customer': customer
#         }
#         return render(request, self.template_name, context)

# TemplateView
# class CustomerDetailTemplateView(TemplateView):
#     template_name = 'blog/customer/customer-details.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         pk = self.kwargs.get('pk')
#         customer = get_object_or_404(Customer, id=pk)
#         context['customer'] = customer
#         return context
# DetailView
class CustomerDetailView(DetailView):
    model = Customer
    template_name = 'blog/customer/customer-details.html'
    context_object_name = 'customer'

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Customer, id=pk)




# def delete_customer(request, pk):
#     customer = Customer.objects.filter(id=pk).first()
#     if customer:
#         customer.delete()
#         return redirect('customers')

# DeleteView
class CustomerDeleteView(DeleteView):
    model = Customer
    success_url = reverse_lazy('customers')

    def get(self, request, *args, **kwargs):
        return self.delete(self.request, *args, **kwargs)

# def update_customer(request, pk):
#     customer = Customer.objects.get(id=pk)
#     form = CustomerModelForm(instance=customer)
#     if request.method == 'POST':
#         form = CustomerModelForm(request.POST, request.FILES, instance=customer)
#         if form.is_valid():
#             form.save()
#             return redirect('customers_detail', pk)
#
#     context = {
#         'form': form,
#         'customer': customer
#     }
#     return render(request, 'blog/customer/update-customer.html', context)

# updateView

class CustomerUpdateView(UpdateView):
    model = Customer
    form_class = CustomerModelForm
    template_name = 'blog/customer/update-customer.html'

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return Customer.objects.get(id=pk)

    def get_success_url(self):
        pk = self.kwargs.get('pk')
        return reverse_lazy('customers_detail', kwargs={'pk': pk})



# def export_data(request):
#     format = request.GET.get('format', 'csv')
#     if format == 'csv':
#         response = HttpResponse(content_type='text/csv')
#         response['Content-Disposition'] = 'attachment; filename="customers.csv" '
#         writer = csv.writer(response)
#         writer.writerow(['id', 'name', 'email', 'phone', 'billing_address'])
#         for customer in Customer.objects.all():
#             writer.writerow([customer.id, customer.name, customer.email, customer.phone, customer.billing_address])
#     elif format == 'json':
#         response = HttpResponse(content_type='application/json')
#         data = list((Customer.objects.values('id', 'name', 'email', 'phone', 'billing_address')))
#         response.content = json.dumps(data, indent=4)
#         response['Content-Disposition'] = 'attachment; filename="customers.json"'
#     elif format == 'xlsx':
#         response = HttpResponse(content_type='application/ms-excel')
#         response['Content-Disposition'] = 'attachment; filename="customers.xlsx"'
#         wb = Workbook()
#         ws = wb.active
#         ws.title = "My View Customer"
#
#         headers = ["Id", "Name", "Email", "Phone", "Billing_Address"]
#         ws.append(headers)
#         for customer in Customer.objects.all():
#             ws.append([customer.id, customer.name, customer.email, customer.phone, customer.billing_address])
#         wb.save(response)
#
#     else:
#         response = HttpResponse(status=404)
#         response.content = 'Bad requests'
#
#     return response

class ExportDataView(View):
    def get(self, request):
        format = request.GET.get('format', 'csv')

        if format == 'csv':
            response = self.export_csv()
        elif format == 'json':
            response = self.export_json()
        elif format == 'xlsx':
            response = self.export_xlsx()
        else:
            response = HttpResponse(status=404)
            response.content = 'Bad requests'

        return response

    def export_csv(self):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="customers.csv"'
        writer = csv.writer(response)
        writer.writerow(['id', 'name', 'email', 'phone', 'billing_address'])
        customers = Customer.objects.all()
        for customer in customers:
            writer.writerow([customer.id, customer.name, customer.email, customer.phone, customer.billing_address])
        return response

    def export_json(self):
        response = HttpResponse(content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="customers.json"'
        data = list(Customer.objects.values('id', 'name', 'email', 'phone', 'billing_address'))
        response.content = json.dumps(data, indent=4)
        return response

    def export_xlsx(self):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="customers.xlsx"'
        wb = Workbook()
        ws = wb.active
        ws.title = "Events"

        headers = ["id", "name", "email", "phone", "billing_address"]
        ws.append(headers)

        customers = Customer.objects.all()
        for customer in customers:
            ws.append([customer.id, customer.name, customer.email, customer.phone, customer.billing_address])

        wb.save(response)
        return response
