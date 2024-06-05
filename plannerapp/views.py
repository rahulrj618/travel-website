from django.shortcuts import render,redirect,get_object_or_404
from .models import Trip, Destination, Stay, UserProfile,Restaurants,Stay,Spots,Contact
from django.http import Http404,HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from .forms import UserRegistrationForm
from django.contrib.auth.models import Group 
from django.contrib.auth.models import User
from django.conf import settings
from .import models
from .import forms
from django.contrib import messages
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest


def index(request):
    return render(request, 'index.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('user_dashboard')  
        else:
            messages.success(request, 'Invalid login credentials.')
            return render(request, 'login.html') 

     

def logout_view(request):
    logout(request)
    messages.success(request, 'Logout successful.')
    return render(request,'index.html')  

@login_required
def user_dashboard(request):    
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'user_dashboard.html', {'user_profile': user_profile})


def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data['username']
            password=form.cleaned_data['password1']
            user=authenticate(request,username=username,password=password)
            login(request, user)            
            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, 'sign_up.html', {'form': form}) 






    
#about us

def aboutus_view(request):
    return render(request,'aboutus.html')

# def contactus_view(request):
#     return render(request,'contactus.html')

from .forms import ContactForm

def contactus_view(request):
    form = ContactForm()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form data (e.g., send an email, save to database)
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Add your processing logic here
            contact = Contact(name=name, email=email, message=message)
            contact.save()

            
            return render(request,'user_dashboard.html')

    return render(request, 'contactus.html', {'form': form})

# Destinations

def destination_list(request):
    destinations = Destination.objects.all()
    return render(request, 'destination_list.html', {'destinations': destinations})

#trips

def trip_list(request):
    trips = Trip.objects.all()
    return render(request, 'trip_list.html', {'trips': trips})

# Accomodations 

def stay_list(request):
    stays = Stay.objects.all()
    return render(request, 'stay_list.html', {'stays': stays})

def stay_detail(request, stay_id):
    stay = get_object_or_404(Stay, pk=stay_id)

    return render(request, 'stay_detail.html', {'stay': stay})

# Restaurants

def restaurant_list(request, destination_id=None, stay_id=None):
    restaurants = Restaurants.objects.all()

    if destination_id:
        restaurants = restaurants.filter(destination_id=destination_id)

    if stay_id:
        stays = Stay.objects.filter(pk=stay_id)
        restaurants = restaurants.filter(destination__stays__in=stays)

    return render(request, 'restaurant_list.html', {'restaurants': restaurants})

def restaurant_detail(request, restaurant_id):
    try:
        restaurant = Restaurants.objects.get(pk=restaurant_id)
    except Restaurants.DoesNotExist:
        raise Http404("Restaurant does not exist")
    return render(request, 'restaurant_detail.html', {'restaurant': restaurant})

#Spots

def spot_list(request, destination_id):
    spots = Spots.objects.filter(destination_id=destination_id)
    
    if spots:
        destination_name = spots.first().destination.name

    return render(request, 'spot_list.html', {'spots': spots, 'destination_name': destination_name})


def spot_detail(request, spot_id):
    spot = get_object_or_404(Spots, pk=spot_id)
    nearby_restaurants = Restaurants.objects.filter(destination=spot.destination)
    nearby_stays = Stay.objects.filter(destination=spot.destination)

    return render(request, 'spot_detail.html', {
        'spot': spot,
        'nearby_restaurants': nearby_restaurants,
        'nearby_stays': nearby_stays,
    })



# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
	auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


def homepage(request):
	currency = 'INR'
	amount = 100 # Rs. 200

	# Create a Razorpay Order
	razorpay_order = razorpay_client.order.create(dict(amount=amount,
													currency=currency,
													payment_capture='0'))

	# order id of newly created order.
	razorpay_order_id = razorpay_order['id']
	callback_url = 'paymenthandler/'

	# we need to pass these details to frontend.
	context = {}
	context['razorpay_order_id'] = razorpay_order_id
	context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
	context['razorpay_amount'] = amount
	context['currency'] = currency
	context['callback_url'] = callback_url

	return render(request, 'payment.html', context=context)

def paymentsuccess(request):
    return render(request, 'paymentsuccess.html')

def paymentfail(request):
    return render(request, 'paymentfail.html')
# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):

	# only accept POST request.
	if request.method == "POST":
		try:
		
			# get the required parameters from post request.
			payment_id = request.POST.get('razorpay_payment_id', '')
			razorpay_order_id = request.POST.get('razorpay_order_id', '')
			signature = request.POST.get('razorpay_signature', '')
			params_dict = {
				'razorpay_order_id': razorpay_order_id,
				'razorpay_payment_id': payment_id,
				'razorpay_signature': signature
			}

			# verify the payment signature.
			result = razorpay_client.utility.verify_payment_signature(
				params_dict)
			if result is not None:
				amount = 0 # Rs. 200
				try:

					# capture the payemt
					razorpay_client.payment.capture(payment_id, amount)

					# render success page on successful caputre of payment
					return render(request, 'paymentsuccess.html')
				except:

					# if there is an error while capturing payment.
					return render(request, 'paymentfail.html')
			else:

				# if signature verification fails.
				return render(request, 'paymentfail.html')
		except:

			# if we don't find the required parameters in POST data
			return HttpResponseBadRequest()
	else:
	# if other than POST request is made.
		return HttpResponseBadRequest()

