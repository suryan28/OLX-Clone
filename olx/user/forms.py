# import the standard Django Forms
# from built-in library
from curses import meta
from pyexpat import model
from secrets import choice
from django import forms

from user.models import Product, Category, ProductImage, Subcategory



class InputForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Subcategory.objects.all())
    class Meta:
        model= Product
        fields = ['product_title', 'product_price','product_description','category','product_location','image']
    
   
class UpdateForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Subcategory.objects.all())
    class Meta:
        model= Product
        fields = ['product_title', 'product_price','product_description','category','product_location','image']


class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')    
    class Meta:
        model = ProductImage
        fields = ('image', )