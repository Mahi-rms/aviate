from django.db.models import TextChoices
class Gender(TextChoices):
    MALE="Male"
    FEMALE="Female"
    NON_BINARY="Non Binary"

class Qualification(TextChoices):
    HIGH_SCHOOL="High School"
    HIGHER_SECONDARY="Higher Secondary"
    DIPLOMA="Diploma"
    BACHELORS="Bachelors"
    MASTERS="Masters"
    PHD="PHD"

class ScoreType(TextChoices):
    GPA="GPA"
    PERCENTAGE="Percentage"
    MARKS="Marks"

class ResponseType(TextChoices):
    SUCCESS="Success"
    FAILED="Failed"

class CompanySize(TextChoices):
    SMALL="1-50"
    MEDIUM="50-500"
    LARGE="500-1000"
    EXTRA_LARGE="1000+"

class OpportunityType(TextChoices):
    INTERNSHIP="Internship"
    FULL_TIME="Full-Time"
    PART_TIME="Part-Time"

class AccountType(TextChoices):
    TALENT="Talent"
    HIRER="Hirer"

class CandidatureStatus(TextChoices):
    APPLIED="Applied"
    SHORTLISTED="Shortlisted"
    SELECTED="Selected"
    NOT_CONSIDERED="Not Considered at this time"
    WITHDRAWN="Withdrawn"