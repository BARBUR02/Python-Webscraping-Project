from django.db import models

class Offert(models.Model):
    SUBJECTS =[
        ("Język polski", "Język polski"),
        ("Język angielski", "Język angielski"),
        ("Matematyka", "Matematyka"),
        ("Fizyka", "Fizyka"),
        ("Chemia", "Chemia"),
    ]

    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255, choices=SUBJECTS)
    locations = models.TextField(null=True)
    minPrice = models.IntegerField(null=True)
    maxPrice = models.IntegerField(null=True)
    description = models.TextField(null=True)
    link = models.URLField(max_length=255)

    def __str__(self):
        return f'[{self.subject}] {self.name}'