from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

from django.contrib.auth.models import User
from users.models import UserProfile
def register(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email     = request.POST.get("email")
        password  = request.POST.get("password")
        # create user logic here...
        print(full_name)
        print(email)
        print(password)
        
        if User.objects.filter(username=email).exists():
            return redirect(f"/?modal=signup&error=exists")# ← back to home with error flag
        user=User.objects.create_user(
            username=email,
            email=email,
            password=password
        )
        profile=UserProfile.objects.create(user=user)
        print(user)
        print(profile)
        print(profile.plan)
        # we cannot define in model.py because in model.py 
        # we define database structure only not the logic of creating user  
        login(request, user)           # ← log them in immediately after signup
        return redirect("dashboard")   # ← send to dashboard, not login page

    return redirect("home")            # ← GET request → just go home

from django.contrib.auth import authenticate, login
from django.shortcuts import redirect

def login_user(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(
            username=email,
            password=password
        )
        print(user)

        # User does not exist
        if not User.objects.filter(username=email).exists():
            #return HttpResponse("User does not exist. Please sign up first.")
            return redirect("/?modal=login&error=nouser")   # ← back to home with error flag
        
        if user is not None:  #Password is wrong, so Django returns:None Therefore:if user is None:
            login(request, user)
            return redirect("dashboard")
        return redirect("/?modal=login&error=badpass") # back to home with error flag

    return redirect("home")

from django.contrib.auth import logout

def logout_user(request):
    logout(request)
    return redirect("home")

from initial.models import ResumeAnalysis
from django.contrib.auth.decorators import login_required

# @login_required  #request.user.is_authenticated
# def dashboard(request):
#     print(request.user)
#     analyses = ResumeAnalysis.objects.filter(
#         user=request.user  # Django returns only that user's analyses.
#     )
#     return render(request,"dashboard.html",{"analyses":analyses})

from django.utils import timezone

@login_required
def dashboard(request):
    analyses = ResumeAnalysis.objects.filter(user=request.user).order_by('-created_at')
    today_count = ResumeAnalysis.objects.filter(
        user=request.user,
        created_at__date=timezone.now().date()
    ).count()
    return render(request, "dashboard.html", {"analyses": analyses,"today_count": today_count})


# ##  payment
import razorpay
from django.conf import settings
from django.shortcuts import render

def create_order(request):

    client = razorpay.Client(
        auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET
        )
    )

    order = client.order.create({
        "amount": 9900,
        "currency": "INR",
        "payment_capture": 1
    })

    return render(request,"payment.html",{"order": order,"key": settings.RAZORPAY_KEY_ID}
    )

# import razorpay
# from django.conf import settings
# from django.shortcuts import render, redirect
# from django.views.decorators.csrf import csrf_exempt
# from django.http import JsonResponse, HttpResponseBadRequest

# # Initialize Razorpay client
# client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

# @login_required
# def create_order(request):
#     if request.method == "POST":
#         user = request.user
#         amount = int(request.POST.get("amount")) * 100  # Convert to paise

#         # Create Razorpay order
#         order_data = {
#             'amount': amount,
#             'currency': 'INR',
#             'payment_capture': '1',  # Auto-capture payment
#         }

#         order = client.order.create(data=order_data)

#         # Save order locally (optional, but good for tracking)
#         # We link it to user later or in the webhook

#         return JsonResponse({
#             'order_id': order['id'],
#             'amount': order['amount'],
#             'currency': order['currency']
#         })

#     return JsonResponse({'error': 'Invalid request'})


# @csrf_exempt
# def payment_success(request):
#     if request.method == "POST":
#         try:
#             payment_id = request.POST.get('razorpay_payment_id')
#             order_id = request.POST.get('razorpay_order_id')
#             signature = request.POST.get('razorpay_signature')

#             # Verify signature
#             params = {'razorpay_order_id': order_id, 'razorpay_payment_id': payment_id}
#             client.utility.verify_signature(params, signature, settings.RAZORPAY_KEY_SECRET)

#             # Payment successful!
#             # Update user plan
#             user = request.user
#             # Assuming a simple plan update for demonstration
#             # You should implement your UserProfile model update here
#             # For now, just redirect or show success

#             return render(request, "payment_success.html", {
#                 'payment_id': payment_id,
#                 'order_id': order_id
#             })

#         except Exception as e:
#             return HttpResponseBadRequest("Payment verification failed")

#     return JsonResponse({'error': 'Invalid request'})

