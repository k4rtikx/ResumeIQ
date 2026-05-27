from django.contrib.auth import base_user
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect


# Create your views here.
def home(request):
    return render(request, "main.html")

import fitz
from .resume_analysis import gemini_resume_analyzer
from .models import ResumeAnalysis
from django.utils import timezone
from users.models import UserProfile
def analyzer(request):
    if request.method == "POST":
        resume = request.FILES.get("resume")
        job_description = request.POST.get("job_description")
        job_title = request.POST.get("job_title")
        #job_title=request.POST.get("job_title")
        print(f"receiving the file {resume}")
        print(f"receiving the job_description {job_description}")
        print(f"receiving the job_title {job_title}")
        # your Gemini analysis logic here...
        # result = analyze_resume(resume_text, job_description)

        """check three times that user upload resume or not"""
        if request.user.is_authenticated:
            print("USER:, request.user")
            print("USER ID:, request.user.id")
            print("AUTH:, request.user.is_authenticated")
            
            # Use get_or_create — safe whether signal creates it or not
            profile, created = UserProfile.objects.get_or_create(
                user=request.user,
                defaults={"plan": "free"}
            )
            print("Profile plan:, profile.plan")
            print("Profile plan:, profile")
            
            if profile.plan == "free":
                today_count = ResumeAnalysis.objects.filter(
                    user=request.user,
                    created_at__date=timezone.now().date()
                ).count()  #Count today's analyses for this user

                if today_count >= 3:  #free user can upload 3 resumes
                    return redirect("pricing")

        try: 
            result= gemini_resume_analyzer(resume,job_description,job_title)

            """check that user is logged in and save his analysis"""
            if request.user.is_authenticated:
                ResumeAnalysis.objects.create(
                    user=request.user,
                    resume_file=resume,
                    job_title=job_title,
                    match_score=result["match_score"]
                ) # to save this in database 
            
            return render(request, "analyzer.html", {"result": result})
        
        except Exception as e:
            # Store the error in session so it survives the redirect
            request.session["ai_error"] = str(e)
            return redirect("mistake")

    # If someone visits /analyzer directly without POST, send them home
    return redirect("home")

def works(request):
    return render(request,'works.html',{})

def feature(request):
    return render(request,'feature.html',{})

def pricing(request):
    return render(request,'pricing.html',{})

def mistake(request):
    # Pop the error from session (one-time read — clears after display)
    error_message = request.session.pop("ai_error", None)
    return render(request, "mistake.html", {"error_message": error_message})
