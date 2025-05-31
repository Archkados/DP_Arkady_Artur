from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # Главная страница
    path('', glav, name='glav'),
    path('index/', index, name='index'),
    path('applications/', applications, name='applications'),

    # Люди
    path('persons/', person_list, name='person_list'),
    path('persons/create/', person_create, name='person_create'),
    path('persons/update/<int:pk>/', person_update, name='person_update'),
    path('persons/delete/<int:pk>/', person_delete, name='person_delete'),

    # Номера машин
    path('cars/', car_number_list, name='car_number_list'),
    path('cars/add/', car_number_create, name='car_number_create'),
    path('cars/edit/<int:pk>/', car_number_update, name='car_number_update'),
    path('cars/delete/<int:pk>/', car_number_delete, name='car_number_delete'),

    # Номера прицепов
    path('trailers/', trailer_number_list, name='trailer_number_list'),
    path('trailers/add/', trailer_number_create, name='trailer_number_create'),
    path('trailers/edit/<int:pk>/', trailer_number_update, name='trailer_number_update'),
    path('trailers/delete/<int:pk>/', trailer_number_delete, name='trailer_number_delete'),



    # Визы
    path('visas/', visa_list, name='visa_list'),
    path('visas/create/', visa_create, name='visa_create'),
    path('visas/update/<int:pk>/', visa_update, name='visa_update'),
    path('visas/delete/<int:pk>/', visa_delete, name='visa_delete'),

    # Страховка тягача
    path('truck/', truck_insurance_list, name='truck_insurance_list'),
    path('truck/create/', truck_insurance_create, name='truck_insurance_create'),
    path('truck/update/<int:pk>/', truck_insurance_update, name='truck_insurance_update'),
    path('truck/delete/<int:pk>/', truck_insurance_delete, name='truck_insurance_delete'),

    # Страховка прицепа
    path('trailer/', trailer_insurance_list, name='trailer_insurance_list'),
    path('trailer/create/', trailer_insurance_create, name='trailer_insurance_create'),
    path('trailer/update/<int:pk>/', trailer_insurance_update, name='trailer_insurance_update'),
    path('trailer/delete/<int:pk>/', trailer_insurance_delete, name='trailer_insurance_delete'),
    
    # Техосмотры оба
    path('truck/inspections/', truck_inspection_list, name='truck_inspection_list'),
    path('truck/inspections/create/', truck_inspection_create, name='truck_inspection_create'),
    path('truck/inspections/update/<int:pk>/', truck_inspection_update, name='truck_inspection_update'),
    path('truck/inspections/delete/<int:pk>/', truck_inspection_delete, name='truck_inspection_delete'),
    path('trailer/inspections/', trailer_inspection_list, name='trailer_inspection_list'),
    path('trailer/inspections/create/', trailer_inspection_create, name='trailer_inspection_create'),
    path('trailer/inspections/update/<int:pk>/', trailer_inspection_update, name='trailer_inspection_update'),
    path('trailer/inspections/delete/<int:pk>/', trailer_inspection_delete, name='trailer_inspection_delete'),


   #заявки и всё что с ними связано
    path('view-companies/', view_companies, name='view_companies'),
    path('view-companies/<int:company_id>/subcompanies/', select_subcompany, name='view_subcompanies'),
    path('subcompany-details/<int:subcompany_id>/', subcompany_details, name='subcompany_details'),
    path('delete-subcompany/<int:subcompany_id>/', delete_subcompany, name='delete_subcompany'),
    path('select-subcompany/<int:company_id>/', select_subcompany, name='select_subcompany'),
    
    path('select-freight-company/', select_freight_company, name='select_freight_company'),
    path('select-company/<int:freight_company_id>/', select_company_for_application, name='select_company_for_application'),
    path('select-subcompany-for-application/<int:freight_company_id>/<int:company_id>/', select_subcompany_for_application, name='select_subcompany_for_application'),
    path('create-application/<int:freight_company_id>/<int:subcompany_id>/', create_application, name='create_application'),
    path('add-route/', add_route, name='add_route'),
    path('requests/', view_requests, name='view_requests'),
    path('preview/<int:shippingapplication_id>/', preview_request, name='preview_request'),
    path('edit/<int:application_id>/', edit_application, name='edit_application'),
    path('delete/<int:application_id>/', delete_application, name='delete_application'),
    path('create-freight-company/', create_freight_company, name='create_freight_company'),
    path('edit-freight-company/<int:company_id>/', edit_freight_company, name='edit_freight_company'), 
    path('delete-company/<int:company_id>/', delete_company, name='delete_company'),
    path('delete-freight-company/<int:freight_company_id>/', delete_freight_company, name='delete_freight_company'),
    path('requests/archive/<int:pk>/', archive_application, name='archive_application'),
    path('requests/archive/', archive_application_list, name='archive_application_list'),
    path('requests/archive/<int:pk>/restore/', restore_application, name='restore_application'),


    # Трекинг документов
    path('tracking/', tracking_list, name='tracking_list'),
    path('tracking/create/', create_tracking, name='create_tracking'),
    path('tracking/edit/<int:pk>/', edit_tracking, name='edit_tracking'),
    path('tracking/delete/<int:pk>/', delete_tracking, name='delete_tracking'),
    path('tracking/archive/<int:pk>/', archive_tracking, name='archive_tracking'),  
    path('tracking/archive/', archive_tracking_list, name='archive_tracking_list'), 
    path('tracking/archive/<int:pk>/restore/', restore_tracking, name='restore_tracking'), 
    path('tracking/details/<int:tracking_id>/', tracking_detail, name='tracking_detail'),
    path('tracking/add_stage_template/', add_stage_template, name='add_stage_template'),
    path('tracking/add_stage_from_template/<int:tracking_id>/', add_stage_from_template, name='add_stage_from_template'),
    path('tracking/add_cargo_info/<int:tracking_id>/', add_cargo_info, name='add_cargo_info'),

    # Пользователи
    path('add-user/', add_user_view, name='add_user'),
    path('users/', user_list_view, name='user_list'),
    path('users/edit/<int:user_id>/', edit_user, name='edit_user'),
    path('users/delete/<int:user_id>/', delete_user, name='delete_user'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)