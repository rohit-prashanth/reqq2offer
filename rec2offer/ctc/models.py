from django.db import models

class HrTeam(models.Model):
    employee_id = models.CharField(primary_key=True, max_length=10)
    employee_name = models.CharField(max_length=50,null=True)
    reference_number = models.IntegerField(null=True)
    designation = models.CharField(max_length=100, null=True)
    ctc = models.IntegerField(null=True)
    job_location = models.CharField(max_length=100, null=True)  # Adjusted max_length for consistency
    date_of_joining = models.DateField(null=True)
    offer_validity_date = models.DateField(null=True)
    system_date = models.DateTimeField(auto_now_add=True, null=True)
    flag = models.CharField(max_length=10, null=True)

    def __str__(self):
        return f"{self.employee_id} - {self.designation}"

class Customer(models.Model):
    customer_id = models.CharField(unique=True, max_length=50)  # Added max_length for consistency
    customer_name = models.CharField(max_length=75, null=True)
    spoc = models.CharField(max_length=50, null=True)  # Single Point of Contact
    email_id = models.EmailField(max_length=100, null=True)  # Changed to EmailField for validation
    contact_number = models.CharField(max_length=30, null=True)
    location = models.CharField(max_length=70, null=True)
    address = models.CharField(max_length=150, null=True)
    creation_date = models.DateField(null=True)
    flag = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.customer_name

class EmployeeDetails(models.Model):  # Renamed for consistent camel case naming
    emp_id = models.ForeignKey(HrTeam, related_name="employee_details", on_delete=models.CASCADE)
    years_of_experience = models.FloatField(null=True)
    user_id = models.IntegerField(null=True)
    sub_business_unit = models.IntegerField(null=True)
    skills = models.CharField(max_length=50, null=True)
    request_raised_date = models.DateTimeField(null=True)
    notice_period = models.DateField(null=True)
    int_req_id = models.CharField(max_length=10, null=True)
    flag = models.CharField(max_length=10, null=True)
    employee_type = models.IntegerField(null=True)
    date_of_joining = models.DateField(null=True)
    cost_center_id = models.IntegerField(null=True)
    business_unit = models.IntegerField(null=True)
    budget = models.IntegerField(null=True)

    def __str__(self):
        return f"User ID: {self.user_id}, Skills: {self.skills}"
    
# class TagTeam(models.Model):
#     reference_number = models.IntegerField(primary_key=True)  # Primary key
#     req_id = models.CharField(max_length=8, null=True, blank=True)
#     raised_by = models.IntegerField(null=True, blank=True)  # Assuming ForeignKey relationship
#     candidate_name = models.CharField(max_length=50, null=True, blank=True)
#     candidate_type = models.IntegerField(null=True, blank=True)  # Assuming ForeignKey relationship
#     technology = models.CharField(max_length=20, null=True, blank=True)
#     others = models.CharField(max_length=120, null=True, blank=True)
#     experience = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
#     contact_number = models.CharField(max_length=20, null=True, blank=True)
#     email = models.CharField(max_length=30, null=True, blank=True)
#     interviewer = models.CharField(max_length=20, null=True, blank=True)
#     interview_date = models.DateField(primary_key=True)  # Primary key
#     candidate_address = models.CharField(max_length=250, null=True, blank=True)
#     resume = models.BinaryField(null=True, blank=True)
#     created_date = models.DateTimeField(null=True, blank=True)
#     flag = models.CharField(max_length=10, null=True, blank=True)

#     def __str__(self):
#         return f"Interview {self.reference_number} on {self.interview_date}"
