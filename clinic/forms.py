from django import forms
from . import models
from .models import *
import sys
from ckeditor.widgets import CKEditorWidget

from colorfield.widgets import ColorWidget
import django_filters
from django.urls import reverse
from django.utils.functional import lazy
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
import inspect
from django import forms
from django.apps import apps

from django.contrib.auth.models import User
from . import models
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, ButtonHolder, Submit
from crispy_forms.bootstrap import InlineRadios
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
#from .custom_layout_object import *
from django.forms import (formset_factory, modelformset_factory)
from django.forms import ModelForm
from django.contrib.admin.widgets import AutocompleteSelect
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, ModelChoiceField
from django.forms.widgets import CheckboxSelectMultiple
from django.forms import ModelForm, ModelChoiceField,inlineformset_factory
from django.forms.widgets import CheckboxSelectMultiple
from django_select2.forms import ModelSelect2MultipleWidget, ModelSelect2Widget
from django.contrib.admin.widgets import AutocompleteSelect
from dal import autocomplete
from simple_select2 import AutoCompleteSelect2Multiple, AutoCompleteSelect2
from django.utils.safestring import mark_safe
from django.forms import RadioSelect
from django_select2.forms import ModelSelect2MultipleWidget, ModelSelect2Widget
from django.utils.functional import keep_lazy_text, lazystr
from django.template.loader import render_to_string


lazy_render_to_string = keep_lazy_text(render_to_string)


def lazy_render(template_name):
    """
    Keep laziness for rendering to string from template
    """
    return lazy_render_to_string(lazystr(template_name))






class SingleSelectWidget(ModelSelect2Widget):
    def filter_queryset(self, request, term, queryset, **dependent_fields):
        qs = super().filter_queryset(request, term, queryset, **dependent_fields)
        if not self.ordering:
            return qs
        return qs.order_by(*self.ordering)

class MultipleSelectWidget(ModelSelect2MultipleWidget):
    def filter_queryset(self, request, term, queryset, **dependent_fields):
        qs = super().filter_queryset(request, term, queryset, **dependent_fields)
        if not self.ordering:
            return qs
        return qs.order_by(*self.ordering)



#from django.contrib.auth import (













class PatientVisit2Form(forms.ModelForm):


 class Meta:
    model = PatientVisit
    fields = '__all__'
        #'Diagnosis',


    widgets = {

        'Diagnosis': autocomplete.ModelSelect2(url='diagnoo-auoto', attrs={'data-placeholder': 'Royal ...', 'data-minimum-input-length': 2}),
        #'examination':forms.NumberInput(attrs={'class':'form-control cantidad'}),
        #'lesion_number':forms.NumberInput(attrs={'class':'form-control'}),
        #'lesion_size':forms.NumberInput(attrs={'class':'form-control subtotal', 'readonly':True}),
    }
PrescriptionFormSet = inlineformset_factory(PatientVisit, Prescriptions,
                                   form=PatientVisit2Form, extra=1)





class PatientForm(forms.ModelForm):
    #test = forms.ModelChoiceField(widget=MultipleTestSelectWidget,queryset=Test.objects.all())

    class Meta:
        model = Patient
        fields = '__all__'



class addDiagnosisForm(ModelForm):

    class Meta:
        model = Diagnosis
        fields = ['name',]

class EditDiagnosisForm(forms.ModelForm):

    class Meta:
        model = Diagnosis
        fields = ['name',]


class LabRequestForm(forms.ModelForm):
    #test = forms.ModelChoiceField(widget=MultipleTestSelectWidget,queryset=Test.objects.all())

    class Meta:
        model = LabRequest
        fields = '__all__'



class HorizontalRadioSelect(forms.RadioSelect):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        css_style = 'style="display: inline-block; margin-right: 10px;"'

        self.renderer.inner_html = '<li ' + css_style + '>{PALPATION_FINDING}{sub_widgets}</li>'


#for admin signup
COLORS = (
         ("#FFFFFF", "white"),
         ("#000000", "black"),

        ('red', 'red'),
        ('pink', 'pink'),
        ('erythematous', 'erythematous'),
		('violecus', 'violecus'),
		('skin colored', 'skin colored'),
		('brown', 'brown'),
		('blue', 'blue'),
		('white', 'white'),
		('yellow', 'yellow'),

		)


class MultipleDiagnosisSelectWidget(MultipleSelectWidget):
    search_fields = ['name__icontains']
    ordering = []


class PatientVisitForm(forms.ModelForm):

    class Meta:
        model = PatientVisit
        fields = '__all__'

        widgets = {

             'Diagnosis': autocomplete.ModelSelect2(url='diagnoo-auoto'),

        }



from django.forms.formsets import DELETION_FIELD_NAME
from django.forms import ModelForm
from django.forms import ModelForm, ModelChoiceField

from django.forms import (formset_factory, modelformset_factory)
import django_filters

#from django_crispy.bootstrap import InlineCheckboxes
from .choices import *
from django.forms import inlineformset_factory
from django_select2.forms import ModelSelect2Widget
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from django.utils.safestring import mark_safe

from django.forms import ModelChoiceField






class PatientVisit3Form(forms.ModelForm):
    title = "Full Skin Exmination On Good Light and Exposure All Sites"

    Biopsy_Request = forms.CharField(initial=mark_safe('my label<br/>next line<br/>label<br/>next '),
        widget=CKEditorWidget(attrs={
            'required': False,
            'class': 'pasthis',
            'label':"nbvvv",



            #'name': 'his',
            #'id': 'mceNoEditor',

            #'cols': 30,
            #'rows': 10
        }))







    lesion_site = forms.MultipleChoiceField(
    choices=SITES,widget=forms.CheckboxSelectMultiple,label=mark_safe('SKIN LESIONS SITES ON BODY MARK IT OR ADD OTHER.'))
    diagnoisise = forms.ModelChoiceField(widget=MultipleDiagnosisSelectWidget,queryset=Diagnosis.objects.all(),label=mark_safe('SKIN LESIONS Diagnosis or OR ADD OTHER.<a id="add-diag" data-toggle="modal" href="#myModal" class="btn btn-dark">Add New DX With ICD CODE</a>'),)
    #diagnoisis = MyUserModelChoiceField(queryset=Diagnosis.objects.all())




    class Meta:
        model = PatientVisit
        fields = '__all__'
        def __init__(self, **kwargs):
            super(PatientVisitTitleForm, self).__init__(**kwargs)
            KOH_Test = reverse_lazy("homee")
            self.fields['KOH_Test'].label = mark_safe(_("I have read and agree with the "
                                                          "<a href='%s'>Terms and Conditions</a>")) % (KOH_Test)

        widgets = {

            'diagnosis': AutoCompleteSelect2Multiple(url='diagnoo-auoto', attrs={'data-placeholder': 'Royal ...','style': 'width: 300px', 'data-minimum-input-length': 2,}),



            }
            #'Diagnosis': AutoCompleteSelect2Multiple(url='diagn-auoto'),
            #'special_sign': AutoCompleteSelect2Multiple(url='espcialSign-autocomplete'),
            #'budget_item_quantity': forms.NumberInput(attrs={'size': 6}),









class UploadPrescription(forms.ModelForm):
	class Meta:
		model=models.Prescriptions
		fields = ['image','record','name']#required fields(input by user)

class VerifyOCRText(forms.ModelForm):
	class Meta:
		model=models.Prescriptions
		fields = ['text']

class UploadXRay(forms.ModelForm):
	class Meta:
		model = models.XRay
		fields = ['image','name']
