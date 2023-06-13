from django import forms
from django.core.files.base import ContentFile
from django.utils.text import slugify
import requests
from .models import Image


class ImageCreateForms(forms.ModelForm):
    class Meta:
        model = Image
        fields = ["title", "url", "description"]
        widgets = {
            "url": forms.HiddenInput,
        }

    def clean_url(self):
        """Check url of the image"""
        url = self.cleaned_data["url"]
        valid_extensions = ["jpg", "jpeg", "png"]
        extension = url.rsplit(".", 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError("The given URL doesn't match valid image extensions.")
        return url

    def save(self, force_insert=False, force_update=False, commit=True):
        image = super().save(commit=False)  # create new instance without saving in DB
        image_url = self.cleaned_data["url"]  # get url of the image from form
        name = slugify(image.title)  # create the name from the title
        extension = image_url.rsplit(".", 1)[1].lower()  # get the extension of the image
        image_name = f"{name}.{extension}"  # create the name + the extension
        response = requests.get(url=image_url)  # get data from an external web-site
        print(image.__dict__)
        image.image.save(image_name, ContentFile(response.content), save=False)
        # current instance call save(). save image on the disk without saving in DB
        print(image.__dict__)
        if commit:  # commit == True. Save form in DB.
            image.save()
        print(image.__dict__)
        return image
