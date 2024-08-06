from django.db import models

class Affiliate(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def create_link(self):
        return f"http://icommission.ca/landing?ref={self.id}/"

class Submission(models.Model):
    affiliate = models.ForeignKey(Affiliate, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission {self.id} by {self.affiliate}"