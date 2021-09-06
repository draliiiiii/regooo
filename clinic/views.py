from django.shortcuts import render
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import *
from .forms import *
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth.models import User
#from utils import Prescription
# Create your views here.
#from .forms import PositionFormSet
class PatientVisitCreate(CreateView):
    class PatientVisit3Form(ModelForm):
        class Meta:
            model = PatientVisit
            fields = '__all__'


    model = PatientVisit
    template_name = 'clinic/visit_form.html'
    #form_class = PatientVisit3Form
    success_url = None


    '''def get_initial(self):#add on
        patient = get_object_or_404(Patient, pk=self.kwargs.get('patient_id'))
        return {
        'patient': patient,
    }'''
class PtCreate(CreateView):
    model = Patient
    template_name = 'clinic/pt_form.html'
    form_class = PatientForm
    success_url = None


class PtList(ListView):
    model = Patient
    template_name = 'clinic/pt_list.html'
    form_class = PatientForm
    success_url = None
    #def get_context_data(self, *args, **kwargs):
        #ctx = super().get_context_data(*args, **kwargs)
        #ctx['form'] = PatientForm(self.request.POST or None)
        #return ctx
    def get_context_data(self, **kwargs):
        patient = super(PtList, self).get_context_data(**kwargs)
        patient['form'] = PatientVisitCreate.PatientVisit3Form
        return patient




class HomepageView(TemplateView):
    template_name = "clinic/pt_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patients'] = Patient.objects.order_by('id')
        return context


##########################################################################
#                           vis views                             #
##########################################################################

class VisDetailView(DetailView):
    model = PatientVisit
    template_name = 'clinic/vis_detail.html'

    def get_context_data(self, **kwargs):
        context = super(VisDetailView, self).get_context_data(**kwargs)
        return context


class VisCreate(CreateView):
    model = PatientVisit
    template_name = 'clinic/prs_form.html'
    form_class = PatientVisit2Form
    success_url = None



    def get_context_data(self, **kwargs):
        data = super(VisCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['titles'] = PrescriptionFormSet(self.request.POST)
        else:
            data['titles'] = PrescriptionFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        titles = context['titles']
        with transaction.atomic():
            form.instance.created_by = self.request.user
            self.object = form.save()
            if titles.is_valid():
                titles.instance = self.object
                titles.save()
        return super(VisCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('myviss:vis_detail', kwargs={'pk': self.object.pk})


    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs):
    #     return super(visCreate, self).dispatch(*args, **kwargs)


class VisUpdate(UpdateView):
    model = PatientVisit
    form_class = PatientVisit2Form
    template_name = 'myviss/vis_create.html'

    def get_context_data(self, **kwargs):
        data = super(VisUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['titles'] = PrescriptionFormSet(self.request.POST, instance=self.object)
        else:
            data['titles'] = PrescriptionFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        titles = context['titles']
        with transaction.atomic():
            form.instance.created_by = self.request.user
            self.object = form.save()
            if titles.is_valid():
                titles.instance = self.object
                titles.save()
        return super(VisUpdate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('myviss:vis_detail', kwargs={'pk': self.object.pk})

    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs):
    #     return super(visUpdate, self).dispatch(*args, **kwargs)


class VisDelete(DeleteView):
    model = PatientVisit
    template_name = 'myviss/confirm_delete.html'
    success_url = reverse_lazy('myviss:homepage')





from dal import autocomplete
from .models import Diagnosis


class DigAutocomplete(autocomplete.Select2QuerySetView):#i cant add new choice in name to add to list
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Diagnosis.objects.none()
        qs = Diagnosis.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs
# Create your views here.


class LabCreate(CreateView):
    model = LabRequest
    template_name = 'clinic/pt_form.html'
    form_class = LabRequestForm
    success_url = None







#from prescription import forms



#protect prescriptions by blockchain and ocr upload
from .models import *
import numpy as np
import cv2
import os
import PIL.Image
from PIL import Image
import pytesseract
from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage
from .models import Prescriptions
from web3 import Web3
import json
from .models import Prescriptions ,XRay
from . import forms
from django.http import HttpResponse , HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import web3



bytecode = "608060405234801561001057600080fd5b506101c6806100206000396000f3fe608060405260043610610046576000357c01000000000000000000000000000000000000000000000000000000009004806366e34cf11461004b578063af5135fd1461009e575b600080fd5b34801561005757600080fd5b506100846004803603602081101561006e57600080fd5b81019080803590602001909291905050506100f1565b604051808215151515815260200191505060405180910390f35b3480156100aa57600080fd5b506100d7600480360360208110156100c157600080fd5b8101908080359060200190929190505050610140565b604051808215151515815260200191505060405180910390f35b60006100fc82610140565b1561010a576000905061013b565b6000829080600181540180825580915050906001820390600052602060002001600090919290919091505550600190505b919050565b60008060009050600090505b60008054905081101561018f578260008281548110151561016957fe5b90600052602060002001541415610184576001915050610195565b80600101905061014c565b60009150505b91905056fea165627a7a72305820577f0c80bf483610360752f4736f01428e4edf66c5102792faaf73951fb4cf2b0029"
abi = json.loads("""[
    {
        "constant": false,
        "inputs": [
            {
                "name": "hash",
                "type": "bytes32"
            }
        ],
        "name": "add_hash",
        "outputs": [
            {
                "name": "",
                "type": "bool"
            }
        ],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "constant": true,
        "inputs": [
            {
                "name": "hash",
                "type": "bytes32"
            }
        ],
        "name": "check_existence",
        "outputs": [
            {
                "name": "",
                "type": "bool"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    }
]""")

class Blockchain():
    def __init__(self, url=None, abi=None, bytecode=None):
        """
        Constructor

        Parameters:
        url : string: url of blockchain
        """

        self.url = url
        self.contract_address = ""
        self.abi = abi
        self.bytecode = bytecode
        print("type of abi")
        print(type(self.abi))
        print(abi)

    def connect(self, url=None):
        """
        Connects app to blockchain

        Parameters:
        url : string: url of blockchain
        """

        self.web3 = Web3(Web3.HTTPProvider(self.url))

        return self.web3.isConnected()


    def instantiate_contract(self):
        """
        Instantiates smart contract object
        """
        self.web3.eth.defaultAccount = self.web3.eth.accounts[0]
        block = self.web3.eth.getBlock('latest')

        if block['number']==0:
            Prescription = self.web3.eth.contract(abi=abi, bytecode=bytecode)
            tx_hash = Prescription.constructor().transact()
            tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)
            print("Contract creation tx receipt")
            print(tx_receipt)

            try:
                self.contract = self.web3.eth.contract(
                address=tx_receipt.contractAddress,
                abi=self.abi,
            )
            except:
                print("Instantiation false")
                return False
        else:
            block = self.web3.eth.getBlock(1)
            hex_hash = self.web3.toHex(block['transactions'][0])
            tx_hash = self.web3.eth.getTransactionReceipt(hex_hash)
            contract_address = tx_hash['contractAddress']
            try:
                self.contract = self.web3.eth.contract(
                    address=contract_address,
                    abi=abi,
                    )
            except:
                print("Instantiation false")
                return False

        return True

    def check_hash(self, hash_):
        """
        Checks if hash exists in blockchain

        Parameters:
        hash : string: hash of 256 bits length
        """
        print("Check hash function")
        if self.instantiate_contract():
            # exists = Prescription.functions.check_existence("0x1b16b1df538ba12dc3f97edbb85caa7050d46c148134290feba80f8236c83db9").call()
            exists = self.contract.functions.check_existence(hash_).call()
            # print(exists)
            return exists

    def insert_hash(self, hash_):
        """
        Inserts hash into blockchain
        """
        # print(hash_)
        # print(type(hash_))
        print("Insert hash function")
        if self.instantiate_contract():
            # try:
            #     self.Prescription.functions.add_hash(hash_).transact()
            # except:
            #     return False
            success = self.contract.functions.add_hash(hash_).transact()
            return success

        # return False


if __name__ == "__main__":
    b = Blockchain("http://127.0.0.1:7545", abi, bytecode)
    hash1 = "0x1b16b1df538ba12dc3f97edbb85caa7050d46c148134290feba80f8236c83db9"
    new_hash = "0x1b16b1df538ba12dc3f97edbb85caa7050d46c148134290feba80f8236c83db0"
    print(b.connect())
    # print(b.check_hash(hash1))
    # print(b.check_hash(new_hash))
    print(b.insert_hash(hash1))
    # print(b.return_hash(hash1))



class Prescription():

	def __init__(self):
		pass

	def ocr(self,request,pk):
		'''
		Converts the image into text form

		prescriptions contains instance of the image
		text stores the plain text obtained from image

		'''
		# if request.method =='POST':
		prescriptions=Prescriptions.objects.get(pk=pk)
		pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
		text = pytesseract.image_to_string(Image.open(prescriptions.image))
		self.text = text
		self.image = prescriptions.image
		self.user = prescriptions.username
		return text,prescriptions

	def upload(self,request):
		'''
		To Upload New Records

		'''
		if request.method == 'POST':
			form = forms.UploadPrescription(request.POST,request.FILES)
			if form.is_valid():
				instance = form.save(commit=False)
				instance.username = request.user
				instance.save()
				pk = instance.pk
				return True , pk
		else:
			form = forms.UploadPrescription()
		return form , -1

	def record_list(self,request):
		'''
		To Display A List of All Existing Records
		'''
		prescriptions=Prescriptions.objects.all()
		return prescriptions

	def delete_record(self,request,pk):
		'''
		To Delete A Particular Record
		'''
		if request.method =='POST':
			prescription = Prescriptions.objects.get(pk = pk)
			prescription.delete()

	def view(self ,request ,pk):
		instance = Prescriptions.objects.get(pk=pk)
		text = instance.text
		hash_ = Web3.soliditySha3(['string'],[text])
		hash_hex = hash_.hex()

		b = blockchain.Blockchain(url="http://127.0.0.1:7545", abi=abi)
		b.connect()
		exists = b.check_hash(hash_hex)
		return exists , instance

bytecode = "608060405234801561001057600080fd5b506101c6806100206000396000f3fe608060405260043610610046576000357c01000000000000000000000000000000000000000000000000000000009004806366e34cf11461004b578063af5135fd1461009e575b600080fd5b34801561005757600080fd5b506100846004803603602081101561006e57600080fd5b81019080803590602001909291905050506100f1565b604051808215151515815260200191505060405180910390f35b3480156100aa57600080fd5b506100d7600480360360208110156100c157600080fd5b8101908080359060200190929190505050610140565b604051808215151515815260200191505060405180910390f35b60006100fc82610140565b1561010a576000905061013b565b6000829080600181540180825580915050906001820390600052602060002001600090919290919091505550600190505b919050565b60008060009050600090505b60008054905081101561018f578260008281548110151561016957fe5b90600052602060002001541415610184576001915050610195565b80600101905061014c565b60009150505b91905056fea165627a7a72305820577f0c80bf483610360752f4736f01428e4edf66c5102792faaf73951fb4cf2b0029"

abi = json.loads("""[
	{
		"constant": false,
		"inputs": [
			{
				"name": "hash",
				"type": "bytes32"
			}
		],
		"name": "add_hash",
		"outputs": [
			{
				"name": "",
				"type": "bool"
			}
		],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "hash",
				"type": "bytes32"
			}
		],
		"name": "check_existence",
		"outputs": [
			{
				"name": "",
				"type": "bool"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	}
]""")


# import keras

class XRay_class():
	# path = "./model.h5"
	# ml_model = model.XRayModel(path)

	def __init__(self):
		# self.image = image
		pass
	def upload_xray(self , request):
		# if request.method=="POST":
		# 	form = forms.UploadXRay(request.POST, request.FILES)
		# 	if form.is_valid():
		# 		self.image = request.image
		# 		return True
		# else:
		# 	form = forms.UploadXRay()
		# return form
		if request.method == 'POST':
			form = forms.UploadXRay(request.POST,request.FILES)
			if form.is_valid():
				instance = form.save(commit=False)
				instance.username = request.user
				instance.save()
				pk = instance.pk
				self.pk = pk
				return True , pk
		else:
			form = forms.UploadXRay()
		return form , -1

	def get_results(self,request,path):
		# ml_model = model.XRayModel(path)
		path = "./model.h5"
		ml_model = model.XRayModel(path)

		ml_model.load_model()

		xray_obj = XRay.objects.get(pk = self.pk)
		# print(type(xray_obj.image))
		# img = np.asarray(xray_obj.image)
		print(os.getcwd())
		print(xray_obj.image.url)
		# path_ = os.path.join('.',xray_obj.image.url)
		path_ = xray_obj.image.path
		print(path_)
		img = cv2.imread(xray_obj.image.path)
		print(type(img))
		print(img.shape)
		img = img/255.0
		img = cv2.resize(img , (224 ,224))
		print(type(img))
		pred = np.argmax(ml_model.model.predict(img.reshape([-1,224,224,3])))
		# pred = np.argmax(ml_model.model.predict(img))[0]
		# if pred==1:
		# 	xray_obj.predictions = "Pneumonia"
		# else:
		# 	xray_obj.predictions = "No Pneumonia"
		# xray_obj.save()
		if pred ==1:
			return "Pneumonia"
		else:
			return "No Pneumonia"


	def xray_list(self,request):
		xray = XRay.objects.all()
		return xray

	def delete_xray(self,request,pk):
		'''
		To Delete A Particular Record
		'''
		# if request.method =='POST':
		xray = XRay.objects.get(pk = pk)
		xray.delete()
# Create your views here.

# contract_address="0x68C7375827709848F649C2996fC806d10D5514d6"
path = "./model.h5"
print("THIS WORKS")
flag1=False

# Create your views here.
@login_required
def record_list(request):
	trial = prescription.Prescription()
	prescriptions = trial.record_list(request)
	return render(request,'prescription/prescription_list.html',{'prescriptions':prescriptions})

#@login_required
def upload(request):
	trial = Prescription()
	form ,pk = trial.upload(request)
	if pk!=-1:
		# return redirect('prescription:ocr/'+str(pk))
		print("a")
		return HttpResponseRedirect(reverse('ocr' , args=(pk,)))

	else:
		print("b")
		return render(request,'clinic/prescription_upload.html',{'form':form})

@login_required
def delete(request,pk):
	trial = prescription.Prescription()
	trial.delete_record(request,pk)
	# pk1 = kwargs.get('pk1', none)
	return redirect('list')

@login_required
def ocr(request,pk):
	if request.method == "GET":
		trial = prescription.Prescription()
		ocr_instance = trial.ocr(request,pk)
		# pk2 = kwargs.get('pk2', none)
		text = ocr_instance[0]
		prescriptions = ocr_instance[1]


	elif request.method == "POST":
		# form = forms.VerifyOCRText(request.POST , request.FILES)
		# if form.is_valid():
		instance = Prescriptions.objects.get(pk = pk)
		if instance is not None:
			instance.text = request.POST.get('ocr-text' , "")
			instance.save()

			instance = Prescriptions.objects.get(pk=pk)
			text = instance.text
			hash_ = Web3.sha3(text=text)
			hash_hex = hash_.hex()
			# print(hash_hex)
			# print(hash_)
			# print(len(hash_hex))
			if flag1==False:
				b = blockchain.Blockchain(url="http://127.0.0.1:7545" , abi=abi)
				# flag1=True
			if b.connect():
				inserted = b.insert_hash(hash_hex)
				print(inserted)
				if inserted:
					return redirect('prescription:list')
				else:
					return HttpResponse('<h1>Push to blockchain failed</h1>')
			else:
				return HttpResponse("<h1>Connection failed</h1>")



			# return redirect('prescription:block' , args=(pk))
			# return render(block(request,pk))
		else:
			return HttpResponse("<h1>Instance is null</h1>")

	return render(request,'clinic/prescription_ocr.html',{'prescriptions':prescriptions,'text':text })


@login_required
def download(request,pk):
	instance = Prescriptions.objects.get(pk=pk)
	text = instance.text
	hash_ = Web3.soliditySha3(['string'],[text])
	hash_hex = hash_.hex()
	if flag1==False:
		b = blockchain.Blockchain(url="http://127.0.0.1:7545", abi=abi)
		# flag1=True
	b.connect()
	exists = b.check_hash(hash_hex)

	if exists:
		return render(request , 'clinic/prescription_download.html' ,{"prescription":instance} )
	else:
		return HttpResponse("<h1>Hash does not exist in blockchain</h1>")

@login_required
def view(request,pk):
	trial = prescription.Prescription()
	print(trial)
	(exists , instance) = trial.view(request,pk)
	if exists:
		return render(request , 'clinic/prescription_view.html' , {'prescription':instance})
	else:
		return HttpResponse("<h1>Hash does not exist in blockchain</h1>")

@login_required
def xray(request):
	trial = x_ray.XRay_class()
	form , pk = trial.upload_xray(request)

	if pk!=-1:
		print(pk)
		obj = XRay.objects.get(pk=pk)

		pred = trial.get_results(request , path)
		print(pred)
		print(obj.predictions)
		obj.predictions = pred
		obj.save()
		image_path = obj.image.url
		return render(request , "prescription/xray_result.html" , {"image_path":image_path,"predictions":pred})

	# pred = "Nahi aaya"
	return render(request , "clinic/xray_upload.html" , {"form":form})

@login_required
def xray_list(request):
	trial = x_ray.XRay_class()
	xray = trial.xray_list(request)
	return render(request,'prescription/xray_list.html',{'xray':xray})

@login_required
def xray_delete(request,pk):
	# print("deelte ho rha hai" , pk)
	trial = x_ray.XRay_class()
	trial.delete_xray(request,pk)
	return redirect('prescription:xray_list')

bytecode = "608060405234801561001057600080fd5b506101c6806100206000396000f3fe608060405260043610610046576000357c01000000000000000000000000000000000000000000000000000000009004806366e34cf11461004b578063af5135fd1461009e575b600080fd5b34801561005757600080fd5b506100846004803603602081101561006e57600080fd5b81019080803590602001909291905050506100f1565b604051808215151515815260200191505060405180910390f35b3480156100aa57600080fd5b506100d7600480360360208110156100c157600080fd5b8101908080359060200190929190505050610140565b604051808215151515815260200191505060405180910390f35b60006100fc82610140565b1561010a576000905061013b565b6000829080600181540180825580915050906001820390600052602060002001600090919290919091505550600190505b919050565b60008060009050600090505b60008054905081101561018f578260008281548110151561016957fe5b90600052602060002001541415610184576001915050610195565b80600101905061014c565b60009150505b91905056fea165627a7a72305820577f0c80bf483610360752f4736f01428e4edf66c5102792faaf73951fb4cf2b0029"

abi = json.loads("""[
	{
		"constant": false,
		"inputs": [
			{
				"name": "hash",
				"type": "bytes32"
			}
		],
		"name": "add_hash",
		"outputs": [
			{
				"name": "",
				"type": "bool"
			}
		],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "hash",
				"type": "bytes32"
			}
		],
		"name": "check_existence",
		"outputs": [
			{
				"name": "",
				"type": "bool"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	}
]""")




import os
import os.path
import sys
import datetime
from builtins import int

from django.db import models
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

import pymysql
# Create your views here.

class IndexView(View):
    template_name = 'clinic/database_backup.html'


    def get(self, request):
        return render(request, 'clinic/database_backup.html',)

    def post(self, request):
        if request.method == 'POST' and 'Tgt_link' in request.POST:
        # pressed confirm in step 1. 在步骤1按下了设置目标数据库的链接

            Tgt_link = {}
            Tgt_ip = request.POST.get('Tgt_ip')
            Tgt_port = int(request.POST.get('Tgt_port'))
            Tgt_db = request.POST.get('Tgt_db')
            Tgt_name = request.POST.get('Tgt_name')
            Tgt_passwd = request.POST.get('Tgt_passwd')
            Tgt_char = request.POST.get('Tgt_char')

            # # connect to target db and get the cursor. 连接目标数据库，获取游标。
            # self.Tgt_database = pymysql.connect(
            #     host=Tgt_ip,
            #     port=Tgt_port,
            #     db=Tgt_db,
            #    user=Tgt_name,
            #     passwd=Tgt_passwd,
            #     charset='utf8'
            #     )
            # self.Tgt_cursor = database.cursor()

            Tgt_link = {'Tgt_ip':Tgt_ip, 'Tgt_port':Tgt_port,'Tgt_db':Tgt_db,'Tgt_name':Tgt_name,'Tgt_passwd':'******', 'Tgt_char':Tgt_char,}
            self.Tgt = Tgt_link
            context = Tgt_link
            # yield self.Tgt
            return render(request, 'clinic/database_backup.html', context=context)



        elif request.method == 'POST' and 'Ori_link' in request.POST:
            # pressed confirm in step 2.在步骤2按下了设置源数据库的链接
            Ori_link = {}
            # 数据源链接
            Ori_ip = request.POST.get('Ori_ip')
            Ori_port = int(request.POST.get('Ori_port'))
            Ori_db = request.POST.get('Ori_db')
            Ori_name = request.POST.get('Ori_name')
            Ori_passwd = request.POST.get('Ori_passwd')
            Ori_char = request.POST.get('Ori_char')

            # connect to origin db (data source) and get the cursor. 连接源数据库，获取游标。
            self.Ori_database = pymysql.connect(
                host=Ori_ip,
                port=Ori_port,
                db=Ori_db,
               user=Ori_name,
                passwd=Ori_passwd,
                charset='utf8'
                )

            self.Ori_cursor = self.Ori_database.cursor()
            # back up origin db to csv or sql file 备份数据库为sql文件或csv
            self.Ori_cursor.close()
            self.Ori_database.close()

            Ori_link = {'Ori_ip':Ori_ip, 'Ori_port':Ori_port, 'Ori_db':Ori_db, 'Ori_name':Ori_name, 'Ori_passwd':'******', 'Ori_char':Ori_char,}
            # context = self.Tgt.update(Ori_link)
            context = Ori_link
            return render(request, 'clinic/database_backup.html', context=context)

        elif request.method == 'POST' and 'upload_file' in request.POST:
            # uploaded a sql file or csv file in step 2. 在步骤2上传了数据包文件
            return render(request, 'clinic/database_backup.html')

        elif request.method == 'POST' and 'sheet_selected' in request.POST:
            # confirmed the data sheets in step3. 在步骤3选好了数据表
            return render(request, 'clinic/database_backup.html')


        elif request.method == 'POST' and 'start_import' in request.POST:
            # confirm alter and close db connections.在步骤4开始执行导入
            return render(request, 'clinic/database_backup.html')


class Step1View(TemplateView):
    template_name = 'clinic/database_backup.html'
    def post(self, request):
        if 'button1' is clicked:
            return redirect('/step2')
        elif 'button2' is clicked:
            return redirect('/step3')

class Step2View(Step1View):
    def post(self, request):
        if request.method == 'POST' and 'Tgt_link' in request.POST:
        # pressed confirm in step 1. 在步骤1按下了设置目标数据库的链接

            Tgt_link = {}
            Tgt_ip = request.POST.get('Tgt_ip')
            Tgt_port = int(request.POST.get('Tgt_port'))
            Tgt_db = request.POST.get('Tgt_db')
            Tgt_name = request.POST.get('Tgt_name')
            Tgt_passwd = request.POST.get('Tgt_passwd')
            Tgt_char = request.POST.get('Tgt_char')

            # # connect to target db and get the cursor. 连接目标数据库，获取游标。
            # self.Tgt_database = pymysql.connect(
            #     host=Tgt_ip,
            #     port=Tgt_port,
            #     db=Tgt_db,
            #    user=Tgt_name,
            #     passwd=Tgt_passwd,
            #     charset='utf8'
            #     )
            # self.Tgt_cursor = database.cursor()

            Tgt_link = {'Tgt_ip':Tgt_ip, 'Tgt_port':Tgt_port,'Tgt_db':Tgt_db,'Tgt_name':Tgt_name,'Tgt_passwd':'******', 'Tgt_char':Tgt_char,}
            self.Tgt = Tgt_link
            context = Tgt_link
            # yield self.Tgt
            return render(request, 'clinic/database_backup.html', context=context)



        elif request.method == 'POST' and 'Ori_link' in request.POST:
            # pressed confirm in step 2.在步骤2按下了设置源数据库的链接
            Ori_link = {}
            # 数据源链接
            Ori_ip = request.POST.get('Ori_ip')
            Ori_port = int(request.POST.get('Ori_port'))
            Ori_db = request.POST.get('Ori_db')
            Ori_name = request.POST.get('Ori_name')
            Ori_passwd = request.POST.get('Ori_passwd')
            Ori_char = request.POST.get('Ori_char')

            # connect to origin db (data source) and get the cursor. 连接源数据库，获取游标。
            self.Ori_database = pymysql.connect(
                host=Ori_ip,
                port=Ori_port,
                db=Ori_db,
               user=Ori_name,
                passwd=Ori_passwd,
                charset='utf8'
                )

            self.Ori_cursor = self.Ori_database.cursor()
            # back up origin db to csv or sql file 备份数据库为sql文件或csv
            self.Ori_cursor.close()
            self.Ori_database.close()

            Ori_link = {'Ori_ip':Ori_ip, 'Ori_port':Ori_port, 'Ori_db':Ori_db, 'Ori_name':Ori_name, 'Ori_passwd':'******', 'Ori_char':Ori_char,}
            # context = self.Tgt.update(Ori_link)
            context = Ori_link
            return render(request, 'clinic/database_backup.html', context=context)

        elif request.method == 'POST' and 'upload_file' in request.POST:
            # uploaded a sql file or csv file in step 2. 在步骤2上传了数据包文件
            return render(request, 'clinic/database_backup.html')

        elif request.method == 'POST' and 'sheet_selected' in request.POST:
            # confirmed the data sheets in step3. 在步骤3选好了数据表
            return render(request, 'clinic/database_backup.html')


        elif request.method == 'POST' and 'start_import' in request.POST:
            # confirm alter and close db connections.在步骤4开始执行导入
            return render(request, 'clinic/database_backup.html')


        # do something
