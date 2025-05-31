from django.db import models
from datetime import date

class Person(models.Model):
    full_name = models.CharField(max_length=255, unique=True, verbose_name="ФИО")

    def __str__(self):
        return self.full_name
    
class CarNumber(models.Model):
    number = models.CharField(max_length=20, unique=True, verbose_name="Номер машины")

    def get_truck_insurance(self):
        return getattr(self.truckinsurance, "insurance_expiry_date", None)
    
    def __str__(self):
        return self.number
    
class TrailerNumber(models.Model):
    number = models.CharField(max_length=20, unique=True, verbose_name="Номер прицепа")
    car_number = models.ForeignKey(CarNumber, related_name="trailers", on_delete=models.CASCADE, null=True, blank=True)

    def get_trailer_insurance(self):
        return getattr(self.trailerinsurance, "insurance_expiry_date", None)
    
    def get_trailer_inspection(self):
        return getattr(self.trailerispection, "insurance_expiry_date", None)
    
    def __str__(self):
        return self.number



class Visa(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE, verbose_name="Человек")
    visa_issue_date = models.DateField(null=True, blank=True, verbose_name="Дата получения визы")
    visa_expiry_date = models.DateField(null=True, blank=True, verbose_name="Дата окончания визы")

    def visa_status(self):
        if not self.visa_expiry_date:
            return "Нет данных о визе"
        
        today = date.today()
        delta = (self.visa_expiry_date - today).days

        if delta > 90:
            return "green"
        elif 30 <= delta <= 90:
            return "yellow"
        else:
            return "red"

    def visa_status_text(self):
        if not self.visa_expiry_date:
            return "Нет данных о визе"
        
        today = date.today()
        delta = (self.visa_expiry_date - today).days

        if delta > 90:
            return "Всё в порядке. Осталось более 3 месяцев."
        elif 30 <= delta <= 90:
            return "Осталось половина срока. Рекомендуется проверить."
        else:
            return "Требуется продление! Осталось менее 1 месяца."

    def __str__(self):
        return f"{self.person.full_name} - Виза"

class TruckInsurance(models.Model):
    truck_number = models.OneToOneField(CarNumber, on_delete=models.CASCADE, unique=True, verbose_name="Машина", blank=True, null=True)
    insurance_issue_date = models.DateField(null=True, blank=True, verbose_name="Дата получения страховки")
    insurance_expiry_date = models.DateField(null=True, blank=True, verbose_name="Дата окончания страховки")

    def insurance_status(self):
        if not self.insurance_expiry_date:
            return "Нет данных о страховке"
        
        today = date.today()
        delta = (self.insurance_expiry_date - today).days

        if delta > 90:
            return "green"
        elif 30 <= delta <= 90:
            return "yellow"
        else:
            return "red"

    def insurance_status_text(self):
        if not self.insurance_expiry_date:
            return "Нет данных о страховке"
        
        today = date.today()
        delta = (self.insurance_expiry_date - today).days

        if delta > 90:
            return "Всё в порядке. Осталось более 3 месяцев."
        elif 30 <= delta <= 90:
            return "Осталось половина срока. Рекомендуется проверить."
        else:
            return "Требуется продление! Осталось менее 1 месяца."

    def __str__(self):
        return f"{self.truck_number} - Страховка (тягач)"
    
class TrailerInsurance(models.Model):
    trailer_number = models.OneToOneField(TrailerNumber, on_delete=models.CASCADE, unique=True, verbose_name="Машина", blank=True, null=True)
    insurance_issue_date = models.DateField(null=True, blank=True, verbose_name="Дата получения страховки")
    insurance_expiry_date = models.DateField(null=True, blank=True, verbose_name="Дата окончания страховки")

    def insurance_status(self):
        if not self.insurance_expiry_date:
            return "Нет данных о страховке"
        
        today = date.today()
        delta = (self.insurance_expiry_date - today).days

        if delta > 90:
            return "green"
        elif 30 <= delta <= 90:
            return "yellow"
        else:
            return "red"

    def insurance_status_text(self):
        if not self.insurance_expiry_date:
            return "Нет данных о страховке"
        
        today = date.today()
        delta = (self.insurance_expiry_date - today).days

        if delta > 90:
            return "Всё в порядке. Осталось более 3 месяцев."
        elif 30 <= delta <= 90:
            return "Осталось половина срока. Рекомендуется проверить."
        else:
            return "Требуется продление! Осталось менее 1 месяца."

    def __str__(self):
        return f"{self.trailer_number} - Страховка (прицеп)"
    

class TruckInspection(models.Model):
    truck_number = models.OneToOneField(CarNumber, on_delete=models.CASCADE, unique=True, verbose_name="Машина (Тягач)", blank=True, null=True)
    inspection_issue_date = models.DateField(null=True, blank=True, verbose_name="Дата техосмотра")
    inspection_expiry_date = models.DateField(null=True, blank=True, verbose_name="Дата окончания техосмотра")

    def inspection_status(self):
        if not self.inspection_expiry_date:
            return "Нет данных о техосмотре"
        
        today = date.today()
        delta = (self.inspection_expiry_date - today).days

        if delta > 90:
            return "green"
        elif 30 <= delta <= 90:
            return "yellow"
        else:
            return "red"

    def inspection_status_text(self):
        if not self.inspection_expiry_date:
            return "Нет данных о техосмотре"
        
        today = date.today()
        delta = (self.inspection_expiry_date - today).days

        if delta > 90:
            return "Всё в порядке. Осталось более 3 месяцев."
        elif 30 <= delta <= 90:
            return "Осталось половина срока. Рекомендуется проверить."
        else:
            return "Требуется продление! Осталось менее 1 месяца."

    def __str__(self):
        return f"{self.truck_number} - Техосмотр (Тягач)"
    

class TrailerInspection(models.Model):
    trailer_number = models.OneToOneField(TrailerNumber, on_delete=models.CASCADE, unique=True, verbose_name="Машина (Прицеп)", blank=True, null=True)
    inspection_issue_date = models.DateField(null=True, blank=True, verbose_name="Дата техосмотра")
    inspection_expiry_date = models.DateField(null=True, blank=True, verbose_name="Дата окончания техосмотра")

    def inspection_status(self):
        if not self.inspection_expiry_date:
            return "Нет данных о техосмотре"
        
        today = date.today()
        delta = (self.inspection_expiry_date - today).days

        if delta > 90:
            return "green"
        elif 30 <= delta <= 90:
            return "yellow"
        else:
            return "red"

    def inspection_status_text(self):
        if not self.inspection_expiry_date:
            return "Нет данных о техосмотре"
        
        today = date.today()
        delta = (self.inspection_expiry_date - today).days

        if delta > 90:
            return "Всё в порядке. Осталось более 3 месяцев."
        elif 30 <= delta <= 90:
            return "Осталось половина срока. Рекомендуется проверить."
        else:
            return "Требуется продление! Осталось менее 1 месяца."

    def __str__(self):
        return f"{self.trailer_number} - Техосмотр (Прицеп)"



class Company(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class SubCompany(models.Model):
    name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="subcompanies")
    
    consignee_info = models.TextField("Грузополучатель, адрес, телефон, контактное лицо", blank=True)
    loading_address = models.TextField("Адрес пункта погрузки", blank=True)
    sender_contact_info = models.TextField("Контактное лицо и телефон Отправителя", blank=True)

    def __str__(self):
        return self.name

class FreightCompany(models.Model):
    name = models.CharField(max_length=255)
    contact_info = models.TextField("Реквизиты компании", blank=True)  

    def __str__(self):
        return self.name

class Route(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class ShippingApplication(models.Model):
    subcompany = models.ForeignKey(SubCompany, on_delete=models.CASCADE)
    freight_company = models.ForeignKey(FreightCompany, on_delete=models.CASCADE)
    consignee = models.TextField("Грузополучатель, адрес, телефон, контактное лицо", blank=True)
    loading_address = models.TextField("Адрес пункта погрузки", blank=True)
    sender_contact = models.TextField("Контактное лицо и телефон Отправителя", blank=True)
    loading_date = models.DateField("Дата погрузки", blank=True, null=True)
    route = models.ForeignKey(Route, on_delete=models.SET_NULL, null=True, blank=True)
    cargo_name = models.CharField("Наименование груза", max_length=255, blank=True)
    cargo_details = models.TextField("Вес, размеры, объём, стоимость", blank=True)
    freight_cost = models.DecimalField("Стоимость фрахта", max_digits=15, decimal_places=2, blank=True, null=True)
    insurance = models.BooleanField("Страхование груза", default=False)
    delivery_term = models.CharField("Срок доставки", max_length=50, default="12-14 дней")
    transportation_features = models.TextField("Особенности транспортировки груза", default="Грузить в один ярус, на наши коробки не ставить коробки и паллеты других отправителей.")
    payment_terms = models.CharField("Условия оплаты", max_length=50, default="100% оплата по факту прибытия")
    is_archived = models.BooleanField(default=False, verbose_name="В архиве")

    def __str__(self):
        return f"Заявка для {self.subcompany.name} через {self.freight_company.name}"
    

class TrackingRequest(models.Model):
    STATUS_CHOICES = [
        ('Отправлено', 'Отправлено'),
        ('Доставлен', 'Доставлен'),
    ]

    vehicle = models.ForeignKey("CarNumber", on_delete=models.SET_NULL, null=True, verbose_name="Машина")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name="Статус", blank=True, null=True)
    departure = models.CharField(max_length=100, verbose_name="Место отправки")
    destination = models.CharField(max_length=100, verbose_name="Место получения")
    departure_date = models.DateField(verbose_name="Дата выезда", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_archived = models.BooleanField(default=False, verbose_name="В архиве")

    def __str__(self):
        return f"Заявка {self.id} - {self.vehicle.number if self.vehicle else 'Без машины'}"


class StageTemplate(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Название шаблона этапа")

    def __str__(self):
        return self.name

class Stage(models.Model):
    tracking_request = models.ForeignKey(TrackingRequest, on_delete=models.CASCADE, related_name="stages")
    template = models.ForeignKey(StageTemplate, on_delete=models.PROTECT, verbose_name="Шаблон этапа", blank=True, null=True)

    def __str__(self):
        template_name = self.template.name if self.template else "No Template"
        return f"{self.tracking_request} - {template_name}"

class CargoInfo(models.Model):
    tracking_request = models.ForeignKey(TrackingRequest, on_delete=models.CASCADE, related_name="cargo_infos")
    name = models.CharField(max_length=255, verbose_name="Название груза")
    file = models.FileField(upload_to="cargo_files/", verbose_name="Файл груза")

    def __str__(self):
        return self.name