#import keras
from django.db import models
from django.utils.safestring import mark_safe
from ckeditor.fields import RichTextFormField
from ckeditor_uploader.fields import RichTextUploadingField
from .choices import *
from jsignature.mixins import JSignatureFieldsMixin

import tensorflow as tf
import numpy as np

#import keras
#from keras import backend as K
#from keras.layers.core import Dense, Dropout
#from keras.optimizers import Adam
#from keras.preprocessing.image import ImageDataGenerator
#from keras.models import Model
#from keras.callbacks import ReduceLROnPlateau, ModelCheckpoint
#from keras.models import Sequential, Model
#from keras.layers import Conv2D, MaxPooling2D, Dense, Dropout, Input, Flatten, SeparableConv2D
#from keras.layers import GlobalMaxPooling2D
#from keras.layers.normalization import BatchNormalization
#from keras.optimizers import Adam, SGD, RMSprop
from django.http import HttpResponse , HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render,redirect
from django.db import models
#from DOCTER.models import Docter
# import in-Built User Models
from django.contrib.auth.models import User


# Create your models here.
class Patient(models.Model):
    #drSchedule_date = models.DateField(null=True, blank=True)
    patient_id = models.AutoField(primary_key=True)
    patient_name = models.CharField(max_length=60, null=True, blank=True)
    #phone_number = CharField(max_length=60)
    email = models.EmailField()
    #def get_absolute_url(self):
        #return f"/visits/{self.pk}/"
    #drSchedule = models.OneToOneField(DrSchedule, on_delete=models.CASCADE, null=True, blank=True)
    #start = models.ForeignKey(TimeSlots, on_delete=models.CASCADE, null=True, verbose_name='Slot time')
    #paid = models.BooleanField(default=False)
    #skype_key = models.CharField(max_length=60, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('visit-auoto', kwargs={'pk' : self.object.pk})


class Diagnosis(models.Model):

    name = models.CharField(max_length=20, default="Empty",primary_key=True)

    def __str__(self):
        return self.name
#import datetime






class PatientVisit(models.Model):


    patient = models.ForeignKey(Patient, null=True, on_delete=models.CASCADE)
    dermatologist= models.ForeignKey(User, null=True,related_name='doctorvisits', on_delete=models.CASCADE)
    lesion_site = models.CharField(max_length=200,choices=SITES)#add mark on image site save in db multiple point draw
    location_site_image = models.ImageField(upload_to='location_pics',default='default.jpg')
    lesion_number = models.IntegerField(default=1)
    lesion_size = models.CharField(max_length=200)
    Biopsy_Request = RichTextUploadingField(verbose_name="Biopsy Request")#how add template doc as template to fill it
    Diagnosis = models.ForeignKey(Diagnosis,on_delete=models.CASCADE)
    signature = models.BinaryField(null=True, blank=True)#didnt appear in html and save in db


    #def create_PatientVisit(sender, **kwargs):
        #if kwargs['created']:
            #patient = Patient.objects.create(patient=kwargs['instance'], pk=kwargs['instance'])

    #def get_absolute_url(self):
        #return reverse('visit-auoto', kwargs={'pk' : self.object.pk})




    class Meta:
        verbose_name_plural = "PatientVisit"

        #ordering = ('created',)

    def __unicode__(self):
        return u'%s' % self.pk






        #indexes = [models.Index(fields=["slug", "user"])]

    # Fields






# Create your models here.

    # def save(self, *args, **kwargs):
        # if not self.id:
        #     self.due_date = datetime.datetime.now()+ datetime.timedelta(days=15)
        # return super(Invoice, self).save(*args, **kwargs)






class LabTest(models.Model):

    title = models.TextField(null=False, blank=True)

class Specimen(models.Model):

    title = models.TextField(null=False, blank=True)






class LabRequest(models.Model):

    patient          = models.ForeignKey(Patient, on_delete=models.CASCADE, blank=True, null=True)
    test             = models.ForeignKey(LabTest, on_delete=models.CASCADE)
    accepted         = models.BooleanField(default=False)
    decline          = models.BooleanField(default=False)
    done             = models.BooleanField(default=False)
    created_by       = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    date_created     = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated          = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return str(self.patient.id)
    def get_absolute_url(self):
        return reverse('order-detail', args=[self.id])

class LabResult(models.Model):
    lab_request   = models.ForeignKey(LabRequest, on_delete=models.CASCADE, blank=True, null=True)
    result        = models.CharField(max_length=225)
    created_by    = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    date_created  = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated       = models.DateTimeField(auto_now_add=False, auto_now=True)
    def __str__(self):
        return str(self.lab_request)




class Medicine(models.Model):
    id=models.AutoField(primary_key=True)
    title = models.CharField(max_length=100,null=True, blank=True,)
    preparation = models.DecimalField(max_digits=5, decimal_places=2)
    manufacturer = models.CharField(max_length=100)
    genric = models.CharField(max_length=300)
    #image=models.FileField(max_length=255)
    form = models.CharField(max_length=300)
    conecentarion = models.CharField(max_length=300)
    #photo = models.ImageField(max_length=40,blank=True)

    def __str__(self):
        return self.title




class Prescriptions(models.Model):
    record = models.CharField(max_length=100)#check out about the unique field
    image = models.ImageField(upload_to='documents/',blank=False)
    username = models.ForeignKey(User,default=None,on_delete=models.PROTECT)
    text = models.TextField(default="")
    name = models.CharField(default="name",max_length=100)

    patientVisit = models.ForeignKey(PatientVisit,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    medicine = models.ManyToManyField(Medicine)#how select dropdown autocmplete medicine image thumbnail

    power =  models.PositiveIntegerField(max_length=100)
    route = models.CharField(max_length=1000)

    dosages_interval = models.PositiveIntegerField()
            #quantity = models.CharField(max_length=1000,choices=DOSE_FREQ_CHOICES)
    amount = models.CharField(max_length=1000,default=0)
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
    def __str__(self):
        return self.record
    def delete(self , *args , **kwargs):
    	self.image.delete()
    	super().delete(*args,**kwargs)










# Create your models here.
#Model prescription.
class XRay(models.Model):
	image = models.ImageField(upload_to='xrays/',blank=False)
	username = models.ForeignKey(User,default=None,on_delete=models.PROTECT)
	name = models.CharField(default="name",max_length=100)
	predictions = models.TextField(default="")
	def __str__(self):
		return self.image.path

	def delete(self , *args , **kwargs):
		self.image.delete()
		super().delete(*args,**kwargs)




class XRayModel():

	def __init__(self , model_path):
		self.model_path = model_path

	def build_model(self):
		input_img = Input(shape=(224,224,3), name='ImageInput')
		x = Conv2D(64, (3,3), activation='relu', padding='same', name='Conv1_1')(input_img)
		x = Conv2D(64, (3,3), activation='relu', padding='same', name='Conv1_2')(x)
		x = MaxPooling2D((2,2), name='pool1')(x)

		x = SeparableConv2D(128, (3,3), activation='relu', padding='same', name='Conv2_1')(x)
		x = SeparableConv2D(128, (3,3), activation='relu', padding='same', name='Conv2_2')(x)
		x = MaxPooling2D((2,2), name='pool2')(x)

		x = SeparableConv2D(256, (3,3), activation='relu', padding='same', name='Conv3_1')(x)
		x = BatchNormalization(name='bn1')(x)
		x = SeparableConv2D(256, (3,3), activation='relu', padding='same', name='Conv3_2')(x)
		x = BatchNormalization(name='bn2')(x)
		x = SeparableConv2D(256, (3,3), activation='relu', padding='same', name='Conv3_3')(x)
		x = MaxPooling2D((2,2), name='pool3')(x)

		x = SeparableConv2D(512, (3,3), activation='relu', padding='same', name='Conv4_1')(x)
		x = BatchNormalization(name='bn3')(x)
		x = SeparableConv2D(512, (3,3), activation='relu', padding='same', name='Conv4_2')(x)
		x = BatchNormalization(name='bn4')(x)
		x = SeparableConv2D(512, (3,3), activation='relu', padding='same', name='Conv4_3')(x)
		x = MaxPooling2D((2,2), name='pool4')(x)

		x = Flatten(name='flatten')(x)
		x = Dense(1024, activation='relu', name='fc1')(x)
		x = Dropout(0.7, name='dropout1')(x)
		x = Dense(512, activation='relu', name='fc2')(x)
		x = Dropout(0.5, name='dropout2')(x)
		x = Dense(2, activation='softmax', name='fc3')(x)

		model = Model(inputs=input_img, outputs=x)
		return model

	def load_model(self , model_path=None):
		if model_path==None:
			model_path = self.model_path

		self.model = self.build_model()
		try:
			self.model.load_weights(model_path)
		except:
			print("Model weights not found")
		#TODO code for loading the model from .h5 file
class Invoice(models.Model):
    patient = models.ForeignKey(Patient, null=True, on_delete= models.SET_NULL)
    patient_email = models.EmailField(null=True, blank=True)
    billing_address = models.TextField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    message = models.TextField(default= "this is a default message.")
    vat = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)

    status = models.BooleanField(default=False)
    def __str__(self):
        return str(self.patient)

    def get_status(self):
        return self.status


class ExpenseItem(models.Model):
    patient = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    #service = models.ForeignKey("Medicalproced",verbose_name=("Medicalproced"),on_delete=models.PROTECT)
    description = models.TextField()
    quantity = models.IntegerField()
    rate = models.DecimalField(max_digits=9, decimal_places=2)
    amount = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return str(self.patient)

class Income(models.Model):
    dr = models.ForeignKey(User, on_delete=models.CASCADE)
    #service = models.ForeignKey("Medicalproced",verbose_name=("Medicalproced"),on_delete=models.PROTECT)
    description = models.TextField()
    quantity = models.IntegerField()
    rate = models.DecimalField(max_digits=9, decimal_places=2)
    amount = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return str(self.dr)




class CalculatesystSteroidManager(models.Manager):

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).annotate(
            dexamethason_amount=F('triamcinlone4mg')*F('betamethasone6mg')*F('perdinslone5mg') /1.25)


#class Materiale(models.Model):
    #quantity=models.DecimalField(max_digits=5, decimal_places=2, default=0)
    #price=models.DecimalField( max_digits=5, decimal_places=2, default=0)
    #VAT=models.DecimalField(max_digits=5, decimal_places=2, default=0)

    #objects = MaterialeManager()

class CalculatesystSteroid(models.Model):

    steroid_type = models.CharField(max_length=250, choices=SYSTSTEROID_POTENCY)
    perdinslone5mg = models.IntegerField()
    methylperdinslon4mg = models.IntegerField()
    triamcinlone4mg = models.IntegerField()
    dexamethason75mg = models.IntegerField()
    betamethasone6mg = models.IntegerField()
    objects = CalculatesystSteroidManager()



    def __str__(self):
        return str(self.steroid_type)
