from django.db import models

# Create your models here.
from accounts.models import AccountImage, Account, AccountLayout


class Layout(models.Model):
    title = models.CharField(max_length=200)
    type = models.CharField(max_length=50)
    style = models.CharField(max_length=50)
    account_layout = models.ForeignKey(AccountLayout, related_name='layouts', on_delete=models.CASCADE)
    def __str__(self):
        return self.title


class LayoutComponent(models.Model):
    component = models.IntegerField()
    images = models.ManyToManyField(AccountImage, related_name='components')
    def __str__(self):
        return f"Component {self.component}"


class LayoutHeader(models.Model):
    layout = models.ForeignKey(Layout, related_name="headers", on_delete=models.CASCADE)
    components = models.ManyToManyField(LayoutComponent, related_name="header_components")

    def __str__(self):
        return f"Header for {self.layout.title}"


class LayoutBody(models.Model):
    layout = models.ForeignKey(Layout, related_name="bodies", on_delete=models.CASCADE)
    components = models.ManyToManyField(LayoutComponent, related_name="body_components")

    def __str__(self):
        return f"Body for {self.layout.title}"


class LayoutFooter(models.Model):
    layout = models.ForeignKey(Layout, related_name="footers", on_delete=models.CASCADE)
    components = models.ManyToManyField(LayoutComponent, related_name="footer_components")

    def __str__(self):
        return f"Footer for {self.layout.title}"


class LayoutText(models.Model):
    text = models.CharField(max_length=1000)
    component = models.ForeignKey(LayoutComponent, related_name="texts", on_delete=models.CASCADE)

    def __str__(self):
        return f"Text: {self.text[:50]}..."  # Display the first 50 characters


class LayoutSetting(models.Model):
    setting = models.JSONField()
    component = models.ForeignKey(LayoutComponent, related_name="settings", on_delete=models.CASCADE)

    def __str__(self):
        return f"Settings for Component {self.component.component}"