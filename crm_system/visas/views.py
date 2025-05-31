from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import *
from .forms import *
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def is_superuser(user):
    return user.is_superuser

@user_passes_test(is_superuser)
def add_user_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'visas/add_user.html', {'form': form})

@user_passes_test(is_superuser)
def user_list_view(request):
    users = User.objects.exclude(is_superuser=True)
    return render(request, 'visas/user_list.html', {'users': users})

def in_group(name):
    def check(user):
        return user.groups.filter(name=name).exists() or user.is_superuser
    return user_passes_test(check)

@login_required
def edit_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пользователь обновлён')
            return redirect('user_list')
    else:
        form = CustomUserEditForm(instance=user)
    return render(request, 'visas/edit_user.html', {'form': form, 'user_obj': user})


@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Пользователь удалён')
        return redirect('user_list')
    return render(request, 'visas/delete_user.html', {'user_obj': user})

@login_required
def glav(request):
    online_tracking = TrackingRequest.objects.filter(is_archived=False, status='Отправлено') 
    trailer_inspections = TrailerInspection.objects.all()
    truck_inspections = TruckInspection.objects.all()
    visas = Visa.objects.all()
    trailer_insurances = TrailerInsurance.objects.all()
    truck_insurances = TruckInsurance.objects.all()
    applications = ShippingApplication.objects.filter(is_archived=False).order_by('-loading_date')[:10]

    return render(request, 'visas/glav.html', {
        'online_tracking': online_tracking,
        'trailer_inspections': trailer_inspections,
        'truck_inspections': truck_inspections,
        'visas': visas,
        'trailer_insurances': trailer_insurances,
        'truck_insurances': truck_insurances,
        'applications': applications,
    })

@in_group("Диспетчер")
def index(request):
    return render(request, 'visas/index.html')

@in_group("Логист")
def applications(request):
    return render(request, 'visas/applications.html')

@in_group("Менеджер")
def tracking_list(request):
    requests = TrackingRequest.objects.filter(is_archived=False)
    return render(request, 'visas/tracking_list.html', {'requests': requests})


def person_list(request):
    sort_field = request.GET.get('sort', 'full_name')  
    sort_order = request.GET.get('order', 'asc')  

    if sort_field == 'visa__visa_expiry_date':
        if sort_order == 'asc':
            persons = Person.objects.prefetch_related('visa').all().order_by('visa__visa_expiry_date')
        else:
            persons = Person.objects.prefetch_related('visa').all().order_by('-visa__visa_expiry_date')
    else:
        if sort_order == 'asc':
            persons = Person.objects.all().order_by('full_name')
        else:
            persons = Person.objects.all().order_by('-full_name')

    return render(request, 'visas/person_list.html', {'persons': persons, 'sort_field': sort_field, 'sort_order': sort_order})


def person_create(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('person_list')
    else:
        form = PersonForm()
    return render(request, 'visas/person_form.html', {'form': form})

def person_update(request, pk):
    person = get_object_or_404(Person, pk=pk)
    if request.method == 'POST':
        form = PersonForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            return redirect('person_list')
    else:
        form = PersonForm(instance=person)
    return render(request, 'visas/person_form.html', {'form': form})

def person_delete(request, pk):
    person = get_object_or_404(Person, pk=pk)
    if request.method == 'POST':
        person.delete()
        return redirect('person_list')
    return render(request, 'visas/person_confirm_delete.html', {'person': person})

def trailer_number_list(request):
    sort_field = request.GET.get('sort', 'number')
    sort_order = request.GET.get('order', 'asc')

    trailer_numbers = TrailerNumber.objects.all()

    if sort_field == 'number':
        if sort_order == 'asc':
            trailer_numbers = trailer_numbers.order_by('number')
        else:
            trailer_numbers = trailer_numbers.order_by('-number')
    elif sort_field == 'trailerinsurance__insurance_expiry_date':
        if sort_order == 'asc':
            trailer_numbers = trailer_numbers.order_by('trailerinsurance__insurance_expiry_date')
        else:
            trailer_numbers = trailer_numbers.order_by('-trailerinsurance__insurance_expiry_date')
    elif sort_field == 'trailerinspection__inspection_expiry_date':
        if sort_order == 'asc':
            trailer_numbers = trailer_numbers.order_by('trailerinspection__inspection_expiry_date')
        else:
            trailer_numbers = trailer_numbers.order_by('-trailerinspection__inspection_expiry_date')
    elif sort_field == 'car_number__number':
        if sort_order == 'asc':
            trailer_numbers = trailer_numbers.order_by('car_number__number')
        else:
            trailer_numbers = trailer_numbers.order_by('-car_number__number')

    return render(request, 'visas/trailer_list.html', {
        'trailer_numbers': trailer_numbers,
        'sort_field': sort_field,
        'sort_order': sort_order
    })



def trailer_number_create(request):
    if request.method == 'POST':
        form = TrailerNumberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('trailer_number_list')
    else:
        form = TrailerNumberForm()
    return render(request, 'visas/trailer_form.html', {'form': form})

def trailer_number_update(request, pk):
    trailer_number = get_object_or_404(TrailerNumber, pk=pk)
    if request.method == 'POST':
        form = TrailerNumberForm(request.POST, instance=trailer_number)
        if form.is_valid():
            form.save()
            return redirect('trailer_number_list')
    else:
        form = TrailerNumberForm(instance=trailer_number)
    return render(request, 'visas/trailer_form.html', {'form': form})

def trailer_number_delete(request, pk):
    trailer_number = get_object_or_404(TrailerNumber, pk=pk)
    if request.method == 'POST':
        trailer_number.delete()
        return redirect('trailer_number_list')
    return render(request, 'visas/trailer_confirm_delete.html', {'trailer_number': trailer_number})


def car_number_list(request):
    sort_field = request.GET.get('sort', 'number')
    sort_order = request.GET.get('order', 'asc')

    car_numbers = CarNumber.objects.all()

    if sort_field == 'number':
        if sort_order == 'asc':
            car_numbers = car_numbers.order_by('number')
        else:
            car_numbers = car_numbers.order_by('-number')
    elif sort_field == 'truckinsurance__insurance_expiry_date':
        if sort_order == 'asc':
            car_numbers = car_numbers.order_by('truckinsurance__insurance_expiry_date')
        else:
            car_numbers = car_numbers.order_by('-truckinsurance__insurance_expiry_date')
    elif sort_field == 'truckinspection__inspection_expiry_date':
        if sort_order == 'asc':
            car_numbers = car_numbers.order_by('truckinspection__inspection_expiry_date')
        else:
            car_numbers = car_numbers.order_by('-truckinspection__inspection_expiry_date')
    elif sort_field == 'trailers__number':
        if sort_order == 'asc':
            car_numbers = car_numbers.order_by('trailers__number')
        else:
            car_numbers = car_numbers.order_by('-trailers__number')
    

    return render(request, 'visas/car_number_list.html', {
        'car_numbers': car_numbers,
        'sort_field': sort_field,
        'sort_order': sort_order
    })



def car_number_create(request):
    if request.method == 'POST':
        form = CarNumberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('car_number_list')
    else:
        form = CarNumberForm()
    return render(request, 'visas/car_number_form.html', {'form': form})

def car_number_update(request, pk):
    car_number = get_object_or_404(CarNumber, pk=pk)
    if request.method == 'POST':
        form = CarNumberForm(request.POST, instance=car_number)
        if form.is_valid():
            form.save()
            return redirect('car_number_list')
    else:
        form = CarNumberForm(instance=car_number)
    return render(request, 'visas/car_number_form.html', {'form': form})

def car_number_delete(request, pk):
    car_number = get_object_or_404(CarNumber, pk=pk)
    if request.method == 'POST':
        car_number.delete()
        return redirect('car_number_list')
    return render(request, 'visas/car_number_confirm_delete.html', {'car_number': car_number})



def visa_list(request):
    sort_field = request.GET.get('sort', 'person__full_name')  
    sort_order = request.GET.get('order', 'asc') 
    visas = Visa.objects.all()
    full_name_filter = request.GET.get('full_name')
    if full_name_filter:
        visas = visas.filter(person__full_name__icontains=full_name_filter)

    visa_issue_date_filter = request.GET.get('visa_issue_date')
    if visa_issue_date_filter:
        visas = visas.filter(visa_issue_date__lte=visa_issue_date_filter)

    visa_expiry_date_filter = request.GET.get('visa_expiry_date')
    if visa_expiry_date_filter:
        visas = visas.filter(visa_expiry_date__lte=visa_expiry_date_filter)

    if sort_field == 'person__full_name':
        if sort_order == 'asc':
            visas = visas.order_by('person__full_name')
        else:
            visas = visas.order_by('-person__full_name')
    elif sort_field == 'visa_expiry_date':
        if sort_order == 'asc':
            visas = visas.order_by('visa_expiry_date')
        else:
            visas = visas.order_by('-visa_expiry_date')
    elif sort_field == 'visa_issue_date':
        if sort_order == 'asc':
            visas = visas.order_by('visa_issue_date')
        else:
            visas = visas.order_by('-visa_issue_date')

    return render(request, 'visas/visa_list.html', {'visas': visas, 'sort_field': sort_field, 'sort_order': sort_order})


def visa_create(request):
    if request.method == 'POST':
        form = VisaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('visa_list')
    else:
        form = VisaForm()
    return render(request, 'visas/visa_form.html', {'form': form})

def visa_update(request, pk):
    visa = get_object_or_404(Visa, pk=pk)
    if request.method == 'POST':
        form = VisaForm(request.POST, instance=visa)
        if form.is_valid():
            form.save()
            return redirect('visa_list')
    else:
        form = VisaForm(instance=visa)
    return render(request, 'visas/visa_form.html', {'form': form})

def visa_delete(request, pk):
    visa = get_object_or_404(Visa, pk=pk)
    if request.method == 'POST':
        visa.delete()
        return redirect('visa_list')
    return render(request, 'visas/visa_confirm_delete.html', {'visa': visa})


def truck_insurance_list(request):
    sort_field = request.GET.get('sort', 'truck_number')  
    sort_order = request.GET.get('order', 'asc') 
    insurances = TruckInsurance.objects.all()
    truck_number_filter = request.GET.get('truck_number')
    if truck_number_filter:
        insurances = insurances.filter(truck_number__icontains=truck_number_filter)

    insurance_issue_date_filter = request.GET.get('insurance_issue_date')
    if insurance_issue_date_filter:
        insurances = insurances.filter(insurance_issue_date__lte=insurance_issue_date_filter)

    insurance_expiry_date_filter = request.GET.get('insurance_expiry_date')
    if insurance_expiry_date_filter:
        insurances = insurances.filter(insurance_expiry_date__lte=insurance_expiry_date_filter)

    if sort_field == 'truck_number':
        if sort_order == 'asc':
            insurances = insurances.order_by('truck_number')
        else:
            insurances = insurances.order_by('-truck_number')
    elif sort_field == 'insurance_expiry_date':
        if sort_order == 'asc':
            insurances = insurances.order_by('insurance_expiry_date')
        else:
            insurances = insurances.order_by('-insurance_expiry_date')
    elif sort_field == 'insurance_issue_date':
        if sort_order == 'asc':
            insurances = insurances.order_by('insurance_issue_date')
        else:
            insurances = insurances.order_by('-insurance_issue_date')

    return render(request, 'visas/truck_insurance_list.html', {'insurances': insurances, 'sort_field': sort_field, 'sort_order': sort_order})

def truck_insurance_create(request):
    if request.method == 'POST':
        form = TruckInsuranceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('truck_insurance_list')
    else:
        form = TruckInsuranceForm()
    return render(request, 'visas/truck_insurance_form.html', {'form': form})

def truck_insurance_update(request, pk):
    insurance = get_object_or_404(TruckInsurance, pk=pk)
    if request.method == 'POST':
        form = TruckInsuranceForm(request.POST, instance=insurance)
        if form.is_valid():
            form.save()
            return redirect('truck_insurance_list')
    else:
        form = TruckInsuranceForm(instance=insurance)
    return render(request, 'visas/truck_insurance_form.html', {'form': form})

def truck_insurance_delete(request, pk):
    insurance = get_object_or_404(TruckInsurance, pk=pk)
    if request.method == 'POST':
        insurance.delete()
        return redirect('truck_insurance_list')
    return render(request, 'visas/truck_insurance_confirm_delete.html', {'insurance': insurance})


def trailer_insurance_list(request):
    sort_field = request.GET.get('sort', 'trailer_number')  
    sort_order = request.GET.get('order', 'asc') 
    insurances = TrailerInsurance.objects.all()

    trailer_number_filter = request.GET.get('trailer_number')
    if trailer_number_filter:
        insurances = insurances.filter(trailer_number__icontains=trailer_number_filter)

    insurance_issue_date_filter = request.GET.get('insurance_issue_date')
    if insurance_issue_date_filter:
        insurances = insurances.filter(insurance_issue_date__lte=insurance_issue_date_filter)

    insurance_expiry_date_filter = request.GET.get('insurance_expiry_date')
    if insurance_expiry_date_filter:
        insurances = insurances.filter(insurance_expiry_date__lte=insurance_expiry_date_filter)

    if sort_field == 'trailer_number':
        if sort_order == 'asc':
            insurances = insurances.order_by('trailer_number')
        else:
            insurances = insurances.order_by('-trailer_number')
    elif sort_field == 'insurance_expiry_date':
        if sort_order == 'asc':
            insurances = insurances.order_by('insurance_expiry_date')
        else:
            insurances = insurances.order_by('-insurance_expiry_date')
    elif sort_field == 'insurance_issue_date':
        if sort_order == 'asc':
            insurances = insurances.order_by('insurance_issue_date')
        else:
            insurances = insurances.order_by('-insurance_issue_date')

    return render(request, 'visas/trailer_insurance_list.html', {
        'insurances': insurances, 
        'sort_field': sort_field, 
        'sort_order': sort_order
    })


def trailer_insurance_create(request):
    if request.method == 'POST':
        form = TrailerInsuranceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('trailer_insurance_list')
    else:
        form = TrailerInsuranceForm()
    return render(request, 'visas/trailer_insurance_form.html', {'form': form})

def trailer_insurance_update(request, pk):
    insurance = get_object_or_404(TrailerInsurance, pk=pk)
    if request.method == 'POST':
        form = TrailerInsuranceForm(request.POST, instance=insurance)
        if form.is_valid():
            form.save()
            return redirect('trailer_insurance_list')
    else:
        form = TrailerInsuranceForm(instance=insurance)
    return render(request, 'visas/trailer_insurance_form.html', {'form': form})

def trailer_insurance_delete(request, pk):
    insurance = get_object_or_404(TrailerInsurance, pk=pk)
    if request.method == 'POST':
        insurance.delete()
        return redirect('trailer_insurance_list')
    return render(request, 'visas/trailer_insurance_confirm_delete.html', {'insurance': insurance})


def truck_inspection_list(request):
    sort_field = request.GET.get('sort', 'truck_number')
    sort_order = request.GET.get('order', 'asc')
    inspections = TruckInspection.objects.all()

    truck_number_filter = request.GET.get('truck_number')
    if truck_number_filter:
        inspections = inspections.filter(truck_number__icontains=truck_number_filter)

    inspection_issue_date_filter = request.GET.get('inspection_issue_date')
    if inspection_issue_date_filter:
        inspections = inspections.filter(inspection_issue_date__lte=inspection_issue_date_filter)

    inspection_expiry_date_filter = request.GET.get('inspection_expiry_date')
    if inspection_expiry_date_filter:
        inspections = inspections.filter(inspection_expiry_date__lte=inspection_expiry_date_filter)

    if sort_field == 'truck_number':
        if sort_order == 'asc':
            inspections = inspections.order_by('truck_number')
        else:
            inspections = inspections.order_by('-truck_number')
    elif sort_field == 'inspection_expiry_date':
        if sort_order == 'asc':
            inspections = inspections.order_by('inspection_expiry_date')
        else:
            inspections = inspections.order_by('-inspection_expiry_date')
    elif sort_field == 'inspection_issue_date':
        if sort_order == 'asc':
            inspections = inspections.order_by('inspection_issue_date')
        else:
            inspections = inspections.order_by('-inspection_issue_date')

    return render(request, 'visas/truck_inspection_list.html', {
        'inspections': inspections, 
        'sort_field': sort_field, 
        'sort_order': sort_order
    })

def truck_inspection_create(request):
    if request.method == 'POST':
        form = TruckInspectionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('truck_inspection_list')
    else:
        form = TruckInspectionForm()
    return render(request, 'visas/truck_inspection_form.html', {'form': form})

def truck_inspection_update(request, pk):
    inspection = get_object_or_404(TruckInspection, pk=pk)
    if request.method == 'POST':
        form = TruckInspectionForm(request.POST, instance=inspection)
        if form.is_valid():
            form.save()
            return redirect('truck_inspection_list')
    else:
        form = TruckInspectionForm(instance=inspection)
    return render(request, 'visas/truck_inspection_form.html', {'form': form})

def truck_inspection_delete(request, pk):
    inspection = get_object_or_404(TruckInspection, pk=pk)
    if request.method == 'POST':
        inspection.delete()
        return redirect('truck_inspection_list')
    return render(request, 'visas/truck_inspection_confirm_delete.html', {'inspection': inspection})


def trailer_inspection_list(request):
    sort_field = request.GET.get('sort', 'trailer_number')
    sort_order = request.GET.get('order', 'asc')
    inspections = TrailerInspection.objects.all()

    trailer_number_filter = request.GET.get('trailer_number')
    if trailer_number_filter:
        inspections = inspections.filter(trailer_number__icontains=trailer_number_filter)

    inspection_issue_date_filter = request.GET.get('inspection_issue_date')
    if inspection_issue_date_filter:
        inspections = inspections.filter(inspection_issue_date__lte=inspection_issue_date_filter)

    inspection_expiry_date_filter = request.GET.get('inspection_expiry_date')
    if inspection_expiry_date_filter:
        inspections = inspections.filter(inspection_expiry_date__lte=inspection_expiry_date_filter)

    if sort_field == 'trailer_number':
        if sort_order == 'asc':
            inspections = inspections.order_by('trailer_number')
        else:
            inspections = inspections.order_by('-trailer_number')
    elif sort_field == 'inspection_expiry_date':
        if sort_order == 'asc':
            inspections = inspections.order_by('inspection_expiry_date')
        else:
            inspections = inspections.order_by('-inspection_expiry_date')
    elif sort_field == 'inspection_issue_date':
        if sort_order == 'asc':
            inspections = inspections.order_by('inspection_issue_date')
        else:
            inspections = inspections.order_by('-inspection_issue_date')

    return render(request, 'visas/trailer_inspection_list.html', {
        'inspections': inspections, 
        'sort_field': sort_field, 
        'sort_order': sort_order
    })


def trailer_inspection_create(request):
    if request.method == 'POST':
        form = TrailerInspectionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('trailer_inspection_list')
    else:
        form = TrailerInspectionForm()
    return render(request, 'visas/trailer_inspection_form.html', {'form': form})

def trailer_inspection_update(request, pk):
    inspection = get_object_or_404(TrailerInspection, pk=pk)
    if request.method == 'POST':
        form = TrailerInspectionForm(request.POST, instance=inspection)
        if form.is_valid():
            form.save()
            return redirect('trailer_inspection_list')
    else:
        form = TrailerInspectionForm(instance=inspection)
    return render(request, 'visas/trailer_inspection_form.html', {'form': form})


def trailer_inspection_delete(request, pk):
    inspection = get_object_or_404(TrailerInspection, pk=pk)
    if request.method == 'POST':
        inspection.delete()
        return redirect('trailer_inspection_list')
    return render(request, 'visas/trailer_inspection_confirm_delete.html', {'inspection': inspection})


def view_companies(request):
    companies = Company.objects.all()
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_companies')
    else:
        form = CompanyForm()
    
    return render(request, 'visas/view_companies.html', {'companies': companies, 'form': form})


def select_subcompany(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    subcompanies = company.subcompanies.all()

    if request.method == 'POST':
        form = SubCompanyForm(request.POST)
        if form.is_valid():
            new_subcompany = form.save(commit=False)
            new_subcompany.company = company
            new_subcompany.save()
            return redirect('subcompany_details', subcompany_id=new_subcompany.id)
    else:
        form = SubCompanyForm()

    return render(request, 'visas/select_subcompany.html', {
        'company': company,
        'subcompanies': subcompanies,
        'form': form
    })


def subcompany_details(request, subcompany_id):
    subcompany = get_object_or_404(SubCompany, id=subcompany_id)
    
    if request.method == 'POST':
        form = SubCompanyDataForm(request.POST, instance=subcompany)
        if form.is_valid():
            form.save()
            return redirect('select_subcompany', company_id=subcompany.company.id)
    else:
        form = SubCompanyDataForm(instance=subcompany)
    
    return render(request, 'visas/subcompany_details.html', {
        'form': form,
        'subcompany': subcompany
    })

def delete_subcompany(request, subcompany_id):
    subcompany = get_object_or_404(SubCompany, id=subcompany_id)
    company_id = subcompany.company.id 
    subcompany.delete()
    return redirect('view_subcompanies', company_id=company_id)

def select_freight_company(request):
    freight_companies = FreightCompany.objects.all()
    form = FreightCompanyForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('select_freight_company')  

    return render(request, 'visas/select_freight_company.html', {'freight_companies': freight_companies, 'form': form})

def create_freight_company(request):
    if request.method == 'POST':
        form = FreightCompanyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('select_freight_company') 
    else:
        form = FreightCompanyForm()

    return render(request, 'visas/create_freight_company.html', {'form': form})

def edit_freight_company(request, company_id):
    company = get_object_or_404(FreightCompany, id=company_id)
    if request.method == 'POST':
        form = FreightCompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            return redirect('select_freight_company') 
    else:
        form = FreightCompanyForm(instance=company)

    return render(request, 'visas/edit_freight_company.html', {'form': form, 'company': company})

def select_company_for_application(request, freight_company_id):
    freight_company = get_object_or_404(FreightCompany, id=freight_company_id)
    companies = Company.objects.all()
    return render(request, 'visas/select_company_for_application.html', {'freight_company': freight_company, 'companies': companies})

def select_subcompany_for_application(request, freight_company_id, company_id):
    company = get_object_or_404(Company, id=company_id)
    freight_company = get_object_or_404(FreightCompany, id=freight_company_id)
    subcompanies = company.subcompanies.all()
    return render(request, 'visas/select_subcompany_for_application.html', {'company': company, 'freight_company': freight_company, 'subcompanies': subcompanies})

def create_application(request, freight_company_id, subcompany_id):
    freight_company = get_object_or_404(FreightCompany, id=freight_company_id)
    subcompany = get_object_or_404(SubCompany, id=subcompany_id)

    initial_data = {
        'consignee': subcompany.consignee_info,
        'loading_address': subcompany.loading_address,
        'sender_contact': subcompany.sender_contact_info,
    }
    
    if request.method == "POST":
        form = ShippingApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.freight_company = freight_company
            application.subcompany = subcompany
            application.save()
            return redirect('view_requests') 
    else:
        form = ShippingApplicationForm(initial=initial_data)

    return render(request, 'visas/create_application_form.html', {
        'form': form,
        'freight_company': freight_company,
        'subcompany': subcompany
    })


def edit_application(request, application_id):
    application = get_object_or_404(ShippingApplication, id=application_id)
    if request.method == 'POST':
        form = ShippingApplicationForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            return redirect('view_requests')
    else:
        form = ShippingApplicationForm(instance=application)
    return render(request, 'visas/edit_application.html', {'form': form})


def delete_application(request, application_id):
    application = get_object_or_404(ShippingApplication, id=application_id)
    if request.method == 'POST':
        application.delete()
        return redirect('view_requests')
    return render(request, 'visas/delete_application.html', {'application': application})

def archive_application_list(request):
    archived_requests = ShippingApplication.objects.filter(is_archived=True)
    return render(request, 'visas/archive_application.html', {'archived_requests': archived_requests})

def archive_application(request, pk):
    application = get_object_or_404(ShippingApplication, pk=pk)
    application.is_archived = True
    application.save()
    return redirect('view_requests')

def restore_application(request, pk):
    application = get_object_or_404(ShippingApplication, pk=pk)
    application.is_archived = False
    application.save()
    return redirect('archive_application_list')

@csrf_exempt
def add_route(request):
    if request.method == "POST":
        data = json.loads(request.body)
        route_name = data.get("name", "")
        
        if route_name:
            new_route = Route.objects.create(name=route_name)
            return JsonResponse({"success": True, "route_id": new_route.id})
        else:
            return JsonResponse({"success": False, "error": "Название маршрута не может быть пустым"})
    return JsonResponse({"success": False, "error": "Неверный запрос"})

def delete_company(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    company.delete()
    return redirect('view_companies')

def delete_freight_company(request, freight_company_id):
    freight_company = get_object_or_404(FreightCompany, id=freight_company_id)
    freight_company.delete()
    return redirect('select_freight_company')

def get_shippingapplication_by_id(shippingapplication_id):
    try:
        return ShippingApplication.objects.get(id=shippingapplication_id)
    except ShippingApplication.DoesNotExist:
        return None

def preview_request(request, shippingapplication_id):
    request_obj = get_shippingapplication_by_id(shippingapplication_id)

    if not request_obj:
        return render(request, 'visas/error_template.html', {'error': 'Заявка не найдена'})

    context = {
        'request_obj': request_obj,
    }
    return render(request, 'visas/preview.html', context)

def view_requests(request):
    requests = ShippingApplication.objects.filter(is_archived=False)
    return render(request, 'visas/view_requests.html', {'requests': requests})


def archive_tracking_list(request):
    requests = TrackingRequest.objects.filter(is_archived=True)
    return render(request, 'visas/archive_tracking.html', {'requests': requests})

def create_tracking(request):
    if request.method == 'POST':
        form = TrackingRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tracking_list')
    else:
        form = TrackingRequestForm()
    return render(request, 'visas/tracking_form.html', {'form': form})

def edit_tracking(request, pk):
    tracking = get_object_or_404(TrackingRequest, pk=pk)
    if request.method == 'POST':
        form = TrackingRequestForm(request.POST, instance=tracking)
        if form.is_valid():
            form.save()
            return redirect('tracking_list')
    else:
        form = TrackingRequestForm(instance=tracking)
    return render(request, 'visas/tracking_form.html', {'form': form})


def delete_tracking(request, pk):
    tracking = get_object_or_404(TrackingRequest, pk=pk)
    if request.method == 'POST':
        tracking.delete()
        return redirect('tracking_list')
    return render(request, 'visas/tracking_confirm_delete.html', {'tracking': tracking})

def archive_tracking(request, pk):
    tracking = get_object_or_404(TrackingRequest, pk=pk)
    tracking.is_archived = True
    tracking.save()
    return redirect('tracking_list') 

def restore_tracking(request, pk):
    tracking = get_object_or_404(TrackingRequest, pk=pk)
    tracking.is_archived = False
    tracking.save()
    return redirect('archive_tracking_list')

def tracking_detail(request, tracking_id):
    tracking = get_object_or_404(TrackingRequest, id=tracking_id)
    stages = Stage.objects.filter(tracking_request=tracking)
    cargo_infos = CargoInfo.objects.filter(tracking_request=tracking)
    stage_templates = StageTemplate.objects.all()
    
    return render(request, 'visas/tracking_details.html', {
        'tracking': tracking, 
        'stages': stages, 
        'cargo_infos': cargo_infos, 
        'stage_templates': stage_templates
    })


@csrf_exempt
def add_stage_template(request):
    if request.method == 'POST':
        stage_name = request.POST.get('stage_name')
        if stage_name and not StageTemplate.objects.filter(name=stage_name).exists():
            StageTemplate.objects.create(name=stage_name)
            return JsonResponse({'status': 'success', 'stage_name': stage_name})
    return JsonResponse({'status': 'error'}, status=400)

@csrf_exempt
def add_stage_from_template(request, tracking_id):
    if request.method == 'POST':
        tracking = get_object_or_404(TrackingRequest, id=tracking_id)
        template_id = request.POST.get('template_id')
        template = get_object_or_404(StageTemplate, id=template_id)
        Stage.objects.create(tracking_request=tracking, template=template)
        return JsonResponse({'status': 'success', 'stage_name': template.name})
    return JsonResponse({'status': 'error'}, status=400)

@csrf_exempt
def add_cargo_info(request, tracking_id):
    if request.method == 'POST' and request.FILES.get('file'):
        tracking = get_object_or_404(TrackingRequest, id=tracking_id)
        name = request.POST.get('name')
        file = request.FILES['file']

        if not name or not file:
            return JsonResponse({'status': 'error', 'message': 'Заполните все поля'}, status=400)

        cargo = CargoInfo.objects.create(tracking_request=tracking, name=name, file=file)

        return JsonResponse({'status': 'success', 'name': cargo.name, 'file_url': cargo.file.url})
    
    return JsonResponse({'status': 'error', 'message': 'Ошибка загрузки'}, status=400)



