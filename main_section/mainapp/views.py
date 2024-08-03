from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import redirect,render
from django.core.files.storage import FileSystemStorage
from .models import *
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.http import HttpResponseServerError
import logging
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.core.exceptions import MultipleObjectsReturned
from django.utils import timezone
from django.core.mail import send_mail
import random
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, logout as auth_logout
import string
import time 
from datetime import timedelta
from admin_section.capp.models import *
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import logging
from django.db.models import Count

# Create your views here.                                                


#main front-end page
 # Assuming you have logic to retrieve course and student objects
def main(request):
    instructor=Instructor.objects.exclude(isdelete=1)
    course_categories=course_category.objects.exclude(isdelete=1)
    course_all=courses.objects.exclude(isdelete=1)
    category_counts = courses.objects.filter(isdelete=0).values('category').annotate(total_courses=Count('id'))

    context={
        'inst':instructor,
        'course': course_categories,
        'course_all':course_all,
        'category_counts':category_counts,
    }
    return render(request,'main.html',context)

def first(request):
    return render(request, 'main.html')

def signup(request):
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        qualification = request.POST.get('qualification')
        contact = request.POST.get('contact')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        username = request.POST.get('username')
        if username == 'email':
            username = email
        elif username == 'contact':
            username = contact
        else:
            username = contact
        # Create user object
        user = student(
            firstname=firstname, lastname=lastname, gender=gender, dob=dob,
            qualification=qualification, contact=contact, email=email,
            username=username, password=password, cpassword=cpassword
            )

        # Save the user
        user.save()

        # Assuming 'added_by' should be the ID of the user performing the signup
        user.added_by = request.user.id if request.user.is_authenticated else 1
        user.save()

        # Generate OTP
        otp = ''.join(random.choices(string.digits, k=6))
        # Save OTP to session
        request.session['otp'] = otp
        request.session['otp_expiration'] = time.time() + 45

        # Send OTP email
        subject = 'Your OTP Code'
        message = f'Your OTP code is {otp}. It is valid for 23 seconds.'
        from_email = 'cihsdteam@gmail.com'  # Sender's email address
        recipient_list = [email]  # Recipient's email address
        send_mail(subject, message, from_email, recipient_list)
        return redirect('otp_verify')
    return render(request, 'signup.html')


def signupcomplete(request):
    sid = request.GET.get('sid')
    if sid:
        member = get_object_or_404(student, id=sid)  # Ensure 'student' model is passed correctly
        #return HttpResponse(f'id:{sid}')
        if request.method == "POST":
            # Retrieve form data
            gname = request.POST.get('gname')
            category = request.POST.get('category')
            maritalstatus = request.POST.get('maritalstatus')
            gcontact = request.POST.get('gcontact')
            whatsapp = request.POST.get('whatsapp')
            occupation = request.POST.get('occupation')
            address = request.POST.get('address')
            city = request.POST.get('city')
            place = request.POST.get('place')
            district = request.POST.get('district')
            post = request.POST.get('post')
            pin = request.POST.get('pin')

            # Check if a new image file is uploaded
            if 'image' in request.FILES:
                myfile = request.FILES['image']
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                member.image = filename

            member.gname = gname
            member.category = category
            member.maritalstatus = maritalstatus
            member.gcontact = gcontact
            member.whatsapp = whatsapp
            member.occupation = occupation
            member.address = address
            member.city = city
            member.place = place
            member.district = district
            member.post = post
            member.pin = pin
            member.save()

            member.is_complete = 1
            member.save()
            
            # Redirect or provide a success message
           # return HttpResponse(f'Signup complete for student with ID: {sid}')
        
        return render(request, 'completesignup.html', {'member': member})
    else:
        return HttpResponse('SID parameter is required.')

# def resend_otp(request):
#     try:
#         if 'email' in request.session:
#             email = request.session['email']
#             otp = ''.join(random.choices(string.digits, k=6))
#             request.session['otp'] = otp  # Save new OTP to session
#             request.session['otp_expiration'] = timezone.now() + timedelta(seconds=23)  # Reset expiration time

#             # Send OTP via email
#             subject = 'Your OTP Code'
#             message = f'Your OTP code is {otp}. It is valid for 23 seconds.'
#             from_email = 'cihsdteam@gmail.com'
#             recipient_list = [email]
#             send_mail(subject, message, from_email, recipient_list)

#             # Redirect back to OTP verification page
#             return redirect('resend_otp')
#     except Exception as e:
#         # Log the error (consider using a logging framework)
#         print(f'An error occurred: {e}')
#         # Return a generic error message to the user
#         return HttpResponse('An internal error occurred. Please try again later.', status=500)


# Configure logging


def loginmain(request):
    try:
        message = ""  # Initialize message
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            # Check if student with given username and password exists
            if student.objects.filter(username=username, password=password).exists():
                student_obj = student.objects.get(username=username, password=password)
                request.session['sid'] = student_obj.id  # Store student ID in session
                studentid = student_obj.id  # Set student_id for context
                course = get_object_or_404(courses, id=1)
                print(f"Session ID set: {request.session['sid']}")  # Debug statement
                return redirect('course_detail', studentid=studentid, courseid=course.id)
            else:
                # Handle invalid credentials here (for example, show an error message)
                message = "Invalid username or password"
    except Exception as e:
        return HttpResponse(f'An error occured:{e}')
    return render(request, 'mainlogin.html', {'message': message})




def otp_verify(request):
    if request.method == 'POST':
         entered_otp = ''.join([
             request.POST.get(f'otp{i}') for i in range(1,7)
         ])
         session_otp = request.session.get('otp')
         otp_expiration = request.session.get('otp_expiration')
         if session_otp and otp_expiration:
             if time.time() < otp_expiration:
                 if entered_otp == session_otp:
                    del request.session['otp']
                    del request.session['otp_expiration']
                    return redirect('success_msg')
                 else:
                     error = 'OTP not matched.'
             else:
                   error = 'OTP expired.'
         else:
              error = 'OTP not found.'
        
         return render(request, 'otp_verification.html', {'error': error})

    return render(request, 'otp_verification.html')

def success_msg(request):
    return render(request,'success.html')
    
#sample alert box passing message.
def ajax_message(request):
    data = {
        'message': "Hello from the server!"
        }
    return JsonResponse(data)


# logger = logging.getLogger(__name__)

def validate_username(request):
    # Extracting data from the request
    username = request.POST.get('username')
    email = request.POST.get('email', None)
    contact = request.POST.get('contact', None)
    data = {}

    # Determine the actual username to validate
    if username == 'email':
        username = email
    elif username == 'contact':
        username = contact
    else:
        username = contact  # No specific type matched, default to None
    # logger.debug(f"Determined username: {username}")

    # Check if the determined username is valid (not None or empty)
    if not username:
       data['message'] = "Invalid username"
       return JsonResponse(data)

    # Query the database to check if the username exists
    try:
        user_exists = student.objects.filter(username=username).exists()
        if user_exists:
            data['message'] = "Username already taken"
        else:
            data['message'] = ""
    except Exception as e:
        data['message'] = "Error checking username"
        logger.error(f"Error querying database: {e}")

    logger.debug(f"Response data: {data}")
    return JsonResponse(data)
logger = logging.getLogger(__name__)


def course_detail(request, studentid, courseid):
    # Log the received IDs
    #logger.info(f"Received studentid: {studentid}, courseid: {courseid}")
    
    # Example logic to retrieve course details
    non_deleted_courses = courses.objects.exclude(isdelete=1)
    course = get_object_or_404(courses, id=courseid)
    students = get_object_or_404(student, id=studentid)
    add= students.is_complete
   
    courses_with_details = []
    coursetype = course_type.objects.get(id=course.coursetype).coursetypeadd
    duration = course_duration.objects.get(id=course.duration).durationadd
     # Add all details to a dictionary
    course_details = {
            'id':course.id,
            'coursetype': coursetype,
            'duration': duration,
        }
        
        # Add the course details dictionary to the list
    courses_with_details.append(course_details)
    context = {
        'courses':non_deleted_courses ,
        'course_detail': courses_with_details,
        'course': course,   # Passing course object to context
        'student': students, # Passing student object to context
        'is_complete':add,  # Pass the iscomplete value
    }
    
    if request.method == 'POST':
        applied_by = 1
        payment_id = 1
        course_status = 'applied'
        applied_on = timezone.now()

        # Create and save the Course_Application object
        application = Course_Application.objects.create(
            student_id=students.id,
            course_id=course.id,
            applied_on=applied_on,
            applied_by=applied_by,
            course_status=course_status,
            payment_id=payment_id
        )

        response = {
            'status': 'success',
            'message': 'Course Applied successfully.',
            'application_id': application.id
        }
        return JsonResponse(response, status=201)

    return render(request, 'coursegrid.html', context)


def course_pro(request, courseid, studentid):
    course = get_object_or_404(courses, id=courseid)
    syllabus =course_syllabus.objects.filter(course=courseid)
    students = get_object_or_404(student, id=studentid)
    #return HttpResponse(f'id:{studentid},course:{courseid}')
    # Add all details to a dictionary
    if request.method == 'POST':
        applied_by = 1  # Example: Set applied_by to the actual user or admin ID
        payment_id = 1  # Example: Set payment_id to the actual payment ID
        course_status = 'applied'
        applied_on = timezone.now()
        # Create and save the Course_Application object
        application = Course_Application.objects.create(
            student_id=students.id,
            course_id=course.id,
            applied_on=applied_on,
            applied_by=applied_by,
            course_status=course_status,
            payment_id=payment_id
        )
        response = {
            'status': 'success',
            'message': 'Course Applied successfully.',
            'application_id': application.id
        }
        return JsonResponse(response, status=201)
    # Fetch related names using IDs for the course details
 
 
    certificate_name =course_certification.objects.get(id=course.certificate).certificateadd
    coursetype_name = course_type.objects.get(id=course.coursetype).coursetypeadd
    duration_name = course_duration.objects.get(id=course.duration).durationadd
    category_name = course_category.objects.get(id=course.category).categoryadd
        
        # Create a dictionary with course details
    course_details = {
        'id': course.id,
        'course': course.course,
        'code': course.code,
        'certificate': certificate_name,
        'coursetype': coursetype_name,
        'duration': duration_name,
        'hours': course.hours,
        'affiliation': course.affiliation,
        'center': course.center,
        'other': course.other,
        'total': course.total,
        'qualification': course.qualification,
        'installment_no': course.installment_no,
        'admission': course.admission,
        'durationdigit': course.durationdigit,
        'image': course.image,
        'course_desc': course.course_desc,
        'category': category_name,
    }
        
    #Prepare the context dictionary with the course details
    context = {
        'courses': course_details,
        'course': course,
        'syllabus':syllabus,
        'student':students,
    }
    return render(request, 'profilecourse.html', context)


def user_pro(request):
    sid = request.GET.get('sid')
    if sid:
        students = get_object_or_404(student, id=sid)
    context = {
        'student': students,
    }
    return render(request, 'profilestudent.html', context)

def signout(request):
    # Clear session data
    request.session.flush()
    return redirect('main')  # Redirect to a success page.

def check_profile_status(request, student_id):
    try:
        students = student.objects.get(pk=student_id)
        return JsonResponse({'is_complete': students.is_complete})
    except student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)
    
def contact(request): 
    return render(request,'contact.html')

def maincourse(request):
    non_deleted_courses = courses.objects.exclude(isdelete=1)
    context={
        'course': non_deleted_courses,
    }
    return render(request,'public_course.html',context)

