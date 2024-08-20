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
from django.db import connection
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import logging
import json

logger = logging.getLogger(__name__)

#index page
def index(request):
    return render(request,'index.html')

#studentform
def reg(request):
    if request.method == 'POST':
            firstname=  request.POST.get('firstname')
            lastname=  request.POST.get('lastname')
            gname =  request.POST.get('gname')
            age = request.POST.get('age')
            maritalstatus=request.POST.get('maritalstatus')
            qualification = request.POST.get('qualification')
            contact = request.POST.get('contact')
            gcontact =request.POST.get('gcontact')
            whatsapp = request.POST.get('whatsapp')
            email =  request.POST.get('email')
            occupation =request.POST.get('occupation')
            address = request.POST.get('address')
            city = request.POST.get('city')
            district =request.POST.get('district')
            post = request.POST.get('post')
            pin =request.POST.get('pin')
            dob =  request.POST.get('dob')
            myfile =request.FILES['image']
            fs = FileSystemStorage()
            f = fs.save(myfile.name, myfile)
            gender =  request.POST.get('gender')  
            category=request.POST.get('category')
            place= request.POST.get('place')
        # Example of rendering the data in a template (adjust as needed)
            r = student(place=place,category=category,firstname=firstname,lastname=lastname,gender=gender,gname=gname,dob=dob,age=age,maritalstatus=maritalstatus, qualification=qualification, contact=contact, gcontact=gcontact, whatsapp=whatsapp, email=email, occupation=occupation, address=address,city=city, district=district, post=post, pin=pin,image=myfile)
            r.save()
           
    duration= course_duration.objects.exclude(isdelete=1)
    course=courses.objects.exclude(isdelete=1)
    batch=course_batch.objects.exclude(isdelete=1)
    return render(request, 'studentform.html',{'add_duration':duration,'course':course,'batch':batch})

def added_by(request,id):
    instance = student()
    instance.added_by = 0
    instance.save() 

@csrf_exempt
def std(request):
    context = {
        'registers': student.objects.exclude(isdelete=1),
    }
    return render(request, 'viewstudent.html', context)

def delete(request,id):
    # Soft delete by marking is_deleted as 1
    student_instance = get_object_or_404(student, id=id)
    student_instance.isdelete = 1
    student_instance.delete()
    student_instance.save()
    return HttpResponseRedirect(reverse(std))

def profileview(request,id):
    std =student.objects.get(id=id)
    # student_with_details = []
    # batch= course_batch.objects.get(id=student.batch).title
    # category= courses.objects.get(id=student.course_category).category
    ## Add all details to a dictionary
    # course_details = {
    #         'batch':batch,
    #         'category':category,
    #     }
        
    #     # Add the course details dictionary to the list
    # student_with_details.append(course_details)
    return render(request, 'studentprofile.html', {'result': std})

def added_by(request,id):
    instance = course_batch()
    instance.added_by = 0
    instance.save()
        
def added_on(request,id):
    instance = student()
    instance.added_on = timezone.now()  # Set added_on field to current date and time
    instance.save()

def update_student(request, id):
    member = student.objects.get(id=id)
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        dob = request.POST.get('dob')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        whatsapp = request.POST.get('whatsapp')
        maritalstatus = request.POST.get('maritalstatus')
        qualification = request.POST.get('qualification')
        category = request.POST.get('category')
        occupation = request.POST.get('occupation')
        address = request.POST.get('address')
        city = request.POST.get('city')
        place = request.POST.get('place')
        district = request.POST.get('district')
        post = request.POST.get('post')
        pin = request.POST.get('pin')
        gname = request.POST.get('gname')
        gcontact = request.POST.get('gcontact')

        # Check if a new image file is uploaded
        if 'image' in request.FILES:
            myfile = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            member.image = filename

        # Update the member's attributes
        member.firstname = firstname
        member.lastname = lastname
        member.dob = dob
        member.age = age
        member.gender = gender
        member.email = email
        member.contact = contact
        member.whatsapp = whatsapp
        member.maritalstatus = maritalstatus
        member.qualification = qualification
        member.category = category
        member.occupation = occupation
        member.address = address
        member.city = city
        member.place = place
        member.district = district
        member.post = post
        member.pin = pin
        member.gname = gname
        member.gcontact = gcontact
        member.save()
        return redirect('update_student', id=id)
    duration = course_duration.objects.exclude(isdelete=1)
    course = courses.objects.exclude(isdelete=1)
    batch=course_batch.objects.exclude(isdelete=1)
    return render(request, 'studentupdate.html', {'member': member, 'add_duration': duration, 'course': course,'batch':batch})

def stdcourse(request):
    if request.method == 'POST':
        # Extract form data
        course = request.POST.get('course')
        code = request.POST.get('code')
        certificate = request.POST.get('certificate')
        coursetype = request.POST.get('coursetype')
        duration = request.POST.get('duration')
        hours = request.POST.get('hours')
        affiliation = request.POST.get('affiliation')
        center = request.POST.get('center')
        other = request.POST.get('other')
        total = request.POST.get('total')
        qualification = request.POST.get('qualification')
        admission = request.POST.get('admission')
        durationdigit = request.POST.get('durationdigit')
        installment_no = request.POST.get('installment_no')
        course_desc = request.POST.get('course_desc')
        category=request.POST.get('category')
        myfile =request.FILES['image']
        fs = FileSystemStorage()
        f = fs.save(myfile.name, myfile)

        # Save course data
        course_object = courses(
            course=course, code=code, installment_no=installment_no, certificate=certificate,
            coursetype=coursetype, duration=duration, hours=hours, affiliation=affiliation,
            center=center, other=other, total=total, qualification=qualification,
            admission=admission, durationdigit=durationdigit, course_desc=course_desc,category=category,image=myfile
        )
        course_object.save()
        # Save installment data
        number_of_installments = int(installment_no) if installment_no else 0
        for i in range(1, number_of_installments + 1):
            amount = request.POST.get(f'installmentAmount_{i}')
            if amount:
                installments.objects.create(
                    courseid=course_object.id,   # Use course_object.id to get the auto-incremented ID
                    order=i,
                    amount=amount
                )    
        return HttpResponseRedirect(reverse(stdcourse))

    # If it's a GET request, render the form with certificate and course type options
    addcertificates =course_certification.objects.exclude(isdelete=1)
    addcoursetypes = course_type.objects.exclude(isdelete=1)
    duration = course_duration.objects.exclude(isdelete=1)
    category = course_category.objects.exclude(isdelete=1)
    return render(request, 'studentcourse.html',{'addcertificates': addcertificates,'addcoursetypes': addcoursetypes,'add_duration': duration,'category':category})

def courseview(request):
    # Fetch all non-deleted courses
    try:
        non_deleted_courses = courses.objects.exclude(isdelete=1)
        # Create a list to hold course details with related names
        courses_with_details = []
        
        for course in non_deleted_courses:
            # Fetch related names using IDs
            certificate_name = course_certification.objects.get(id=course.certificate).certificateadd
            coursetype_name = course_type.objects.get(id=course.coursetype).coursetypeadd
            duration_name = course_duration.objects.get(id=course.duration).durationadd
            #category_name = course_category.objects.get(id=course.category).categoryadd
            
            # Add all details to a dictionary
            course_details = {
                'id':course.id,
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
                #'category': category_name
            }
            
            # Add the course details dictionary to the list
            courses_with_details.append(course_details)
    except Exception as e:
        return HttpResponse(f'An error occured as : {e}')
    return render(request, 'viewcourse.html', {'courses': courses_with_details})

def dele(request, id):
 # Soft delete by marking is_deleted as 1
    course_instance = get_object_or_404(courses, id=id)
    course_instance.isdelete = 1
    course_instance.delete()
    course_instance.save()
    return HttpResponseRedirect(reverse(courseview))

def added_on(request,id):
    instance = courses()
    instance.added_on = timezone.now()  # Set added_on field to current date and time
    instance.save()

def added_by(request,id):
    instance = courses()
    instance.added_by = 0
    instance.save()

def deleteduration(request, id):
    # Soft delete by marking is_deleted as 1
    duration_instance = get_object_or_404(installments, id=id)
    duration_instance.isdelete = 1
    duration_instance.delete()
    duration_instance.save()
    return HttpResponseRedirect(reverse(show_duration))

def added_on(request,id):
    instance = installments()
    instance.added_on = timezone.now()  # Set added_on field to current date and time
    instance.save()

def added_by(request,id):
    instance = installments()
    instance.added_by = 0
    instance.save()

def edit_course(request, id):
    member = courses.objects.get(id=id)
    installment_objs = installments.objects.filter(courseid=id)  # Renamed to avoid conflict
    
    if request.method == 'POST':
        # Update course details
        course = request.POST.get('course')
        code = request.POST.get('code')
        course_desc = request.POST.get('course_desc')
        certificate = request.POST.get('certificate')
        coursetype = request.POST.get('coursetype')
        duration = request.POST.get('duration')
        hours = request.POST.get('hours')
        affiliation = request.POST.get('affiliation')
        center = request.POST.get('center')
        qualification = request.POST.get('qualification')
        other = request.POST.get('other')
        total = request.POST.get('total')
        admission = request.POST.get('admission')
        category= request.POST.get('category')
        durationdigit = request.POST.get('durationdigit')
        installment_no = request.POST.get('installment_no')  # Renamed variable
    
        
        # Handle image upload
        if 'image' in request.FILES:
            myfile = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            member.image = filename 
       
        member.certificate = certificate
        member.course = course
        member.code = code
        member.course_desc = course_desc
        member.coursetype = coursetype
        member.duration = duration
        member.hours = hours
        member.affiliation = affiliation
        member.center = center
        member.qualification = qualification
        member.other = other
        member.total = total
        member.admission = admission
        member.durationdigit = durationdigit
        member.category = category
        member.installment_no = installment_no
        member.save()
        
        # # Update or create installment amounts
        # for installment in installment_objs:
        #     amount_key = f'installmentAmount_{installment.id}'
        #     if amount_key in request.POST:
        #         installment_amount = request.POST.get(amount_key)
        #         installment.amount = installment_amount
        #         installment.save()

        #  #Create new installments for added rows
        # new_installment_count = int(request.POST.get('installment_no', 0)) - installment_objs.count()
        # for i in range(1, new_installment_count + 1):
        #     amount_key = f'installmentAmount_{installment_objs.count() + i}'
        #     amount = request.POST.get(amount_key)
        # if amount:
        #     installments.objects.create(
        #         courseid=member.id,  # Use member.id instead of member
        #         order=installment_objs.count() + i,
        #         amount=amount
        #     )
        for installment in installment_objs:
            amount_key = f'installmentAmount_{installment.id}'
        if amount_key in request.POST:
            installment_amount = request.POST.get(amount_key)
            if installment_amount:  # Ensure the amount is not None or empty
                installment.amount = installment_amount
                installment.save()
    
    # Create new installments for added rows
    new_installment_count = int(request.POST.get('installment_no', 0)) - installment_objs.count()
    for i in range(1, new_installment_count + 1):
        amount_key = f'installmentAmount_{installment_objs.count() + i}'
        amount = request.POST.get(amount_key)
        if amount:  # Ensure the amount is not None or empty
            installments.objects.create(
                courseid=course.id,  # Use course.id instead of member
                order=installment_objs.count() + i,
                amount=amount
            )
    for inst in installment_objs:
            order_key = f'order_{inst.id}'
            amount_key = f'amount_{inst.id}'
            if order_key in request.POST and amount_key in request.POST:
                inst.order = request.POST[order_key]
                inst.amount = request.POST[amount_key]
                inst.save()

    addcertificates =course_certification.objects.exclude(isdelete=1)
    addcoursetypes = course_type.objects.exclude(isdelete=1)
    duration = course_duration.objects.exclude(isdelete=1)
    category=course_category.objects.exclude(isdelete=1)
    return render(request, 'courseupdate.html', {'installment': installment_objs, 'members': member, 'certificates': addcertificates, 'coursetype': addcoursetypes, 'duration': duration,'category':category})

def tablejoin(request, id):
    # Retrieve the course with the provided id
    course = get_object_or_404(courses, id=id)
    # Retrieve all installments related to the course
    installments_for_course = installments.objects.filter(courseid=id)
    # Retrieve certification, coursetype, and duration details for the course
    courses_with_details = []
    certification= course_certification.objects.get(id=course.certificate).certificateadd
    coursetype = course_type.objects.get(id=course.coursetype).coursetypeadd
    duration = course_duration.objects.get(id=course.duration).durationadd
    category = course_category.objects.get(id=course.category).categoryadd
     # Add all details to a dictionary
    course_details = {
            'id':course.id,
            'course': course.course,
            'certificate': certification,
            'coursetype': coursetype,
            'duration': duration,
            'category': category,
        }
        
        # Add the course details dictionary to the list
    courses_with_details.append(course_details)
    return render(request, 'courseprofile.html', {'course': course, 'installment': installments_for_course, 'courses':courses_with_details})

def option_view(request):
    certificates =course_certification.objects.exclude(isdelete=1)
    return render(request, 'studentcourse.html', { 'certificates': certificates})

#certification
def certification(request):
    non_deleted_certificate =course_certification.objects.exclude(isdelete=1)
    return render(request, 'certification.html', { 'certificates': non_deleted_certificate}) 

def add_certification(request, id=None):
    if id:
        member = get_object_or_404(course_certification, id=id)
    else:
        member = None

    if request.method == 'POST':
        certificateadd = request.POST.get('certificateadd')
        if member:
            # Update existing record
            member.certificateadd = certificateadd
            member.save()
        else:
            course_certification.objects.create(certificateadd=certificateadd)
            # Create new record
        return redirect('certification')

    return render(request, 'certification.html', {'member': member})

def deleaddcourse(request,id):
   # Soft delete by marking is_deleted as 1
    certificate_instance = get_object_or_404(course_certification, id=id)
    certificate_instance.isdelete = 1
    certificate_instance.delete()
    certificate_instance.save()
    return HttpResponseRedirect(reverse(certification))
   
def added_on(request,id):
    instance = course_certification()
    instance.added_on = timezone.now()  # Set added_on field to current date and time
    instance.save()

def added_by(request,id):
    instance = course_certification()
    instance.added_by = 0
    instance.save()

def add_coursetype(request, id=None):
    if id:
        member = get_object_or_404(course_type, id=id)
    else:
        member = None

    if request.method == 'POST':
        coursetypeadd = request.POST.get('coursetypeadd')
        if member:
            # Update existing record
            member.coursetypeadd = coursetypeadd
            member.save()
        else:
            course_type.objects.create(coursetypeadd=coursetypeadd)
            # Create new record
        return redirect('show_course')

    return render(request, 'coursetype.html', {'member': member})

def show_course(request):
    # Exclude deleted course types
    non_deleted_registers = course_type.objects.exclude(isdelete=1)  # Assuming `isdelete` is a BooleanField
    return render(request, 'coursetype.html',{'coursetypes': non_deleted_registers})

def deletetype(request, id):
    # Soft delete by marking is_deleted as 1
    coursetype_instance = get_object_or_404(course_type, id=id)
    coursetype_instance.isdelete = 1
    coursetype_instance.delete()
    coursetype_instance.save()
    return HttpResponseRedirect(reverse(show_course))

def added_on(request,id):
    instance = course_type()
    instance.added_on = timezone.now()  # Set added_on field to current date and time
    instance.save()

def added_by(request,id):
    instance = course_type()
    instance.added_by = 0
    instance.save()

#course duration
def show_duration(request):
    non_deleted_duration =course_duration.objects.exclude(isdelete=1)
    return render(request,'courseduration.html',{'duration': non_deleted_duration})


def add_duration(request, id=None):
    if id:
        member = get_object_or_404(course_duration, id=id)
    else:
        member = None

    if request.method == 'POST':
        durationadd = request.POST.get('durationadd')
        if member:
            # Update existing record
            member.durationadd = durationadd
            member.save()
        else:
            course_duration.objects.create(durationadd=durationadd)
            # Create new record
        return redirect('show_duration')

    return render(request, 'courseduration.html', {'member': member})

def deleteduration(request, id):
    # Soft delete by marking is_deleted as 1
    duration_instance = get_object_or_404(course_duration, id=id)
    duration_instance.isdelete = 1
    duration_instance.delete()
    duration_instance.save()
    return HttpResponseRedirect(reverse(show_duration))

def added_on(request,id):
    instance = course_duration()
    instance.added_on = timezone.now()  # Set added_on field to current date and time
    instance.save()

def added_by(request,id):
    instance = course_duration()
    instance.added_by = 0
    instance.save()

#course batch
def batch(request):
    if request.method == 'POST':
        course = request.POST.get('course')
        duration = request.POST.get('duration')
        hours = request.POST.get('hours')
        title = request.POST.get('title')
        days = request.POST.getlist('days')  # Use getlist to retrieve all selected days
        daily_hours = request.POST.get('daily_hours')

        # Process the days into a format suitable for storage
        days_str = ','.join(days)

        # Create and save the course_batch object
        k = course_batch(course=course, hours=hours, title=title, days=days_str, daily_hours=daily_hours, duration=duration)
        k.save()

        return HttpResponseRedirect(reverse('batch'))

    course_list = courses.objects.exclude(isdelete=1)
    return render(request, 'batch.html', {'course': course_list})

def added_on(request,id):
    instance = course_batch()
    instance.added_on = timezone.now()  # Set added_on field to current date and time
    instance.save()

def added_by(request,id):
    instance = course_batch()
    instance.added_by = 0
    instance.save()

def viewbatch(request):
    batch = course_batch.objects.exclude(isdelete=1)
    courses_list = courses.objects.exclude(isdelete=1)
    batch_with_course_names = []

    for batch in batch:
        course = get_object_or_404(courses, id=batch.course)
        batch_with_course_names.append({
            'id': batch.id,
            'course_name': course.course,
            'duration': batch.duration,
            'hours': batch.hours,
            'title': batch.title,
            'days': batch.days,
            'daily_hours': batch.daily_hours,
        })

    return render(request, 'batchview.html', {'batch': batch_with_course_names, 'courses': courses_list})

def update_batch(request, id):
    member = get_object_or_404(course_batch, id=id)
    
    if request.method == 'POST':
        course = request.POST.get('course')
        duration = request.POST.get('duration')
        hours = request.POST.get('hours')
        title = request.POST.get('title')
        days = request.POST.getlist('days')  # Retrieve all selected days as a list
        daily_hours = request.POST.get('daily_hours')

        if course:
            member.course = course
        member.duration = duration
        member.hours = hours
        member.title = title
        member.days = ','.join(days)  # Convert the list to a comma-separated string
        member.daily_hours = daily_hours
        member.save()

    courses_list = courses.objects.exclude(isdelete=1)
    current_course_obj = get_object_or_404(courses, id=member.course)
    current_course_name = current_course_obj.course

    return render(request, 'batch_update.html', {'member': member, 'current_course_name': current_course_name, 'course': courses_list})

def delebatch(request, id):
 # Soft delete by marking is_deleted as 1
    batch_instance = get_object_or_404(course_batch, id=id)
    batch_instance.isdelete = 1
    batch_instance.delete()
    batch_instance.save()
    return HttpResponseRedirect(reverse(viewbatch))

#login
def log(request):
    email=request.POST.get('email')
    password=request.POST.get('password')
    if email== 'admin@gmail.com' and password == 'admin':
        request.session['logindetails'] = email
        request.session['admin'] = 'admin'
        return render(request,'index.html')
    else:
        return render(request,'login.html',{'success':'User login successfully'})   
    
#logout
def logout(request):
    # Clear session data
    request.session.flush()
    # Redirect to a success page.
    return redirect('log')  

#Syllabus
def managesyllabus(request):
    if request.method == 'POST':
        # Get the form data
        course= request.POST.get('course')
        title = request.POST.get('title')
        syllabus_desc = request.POST.get('syllabus_desc')
       
        # Create a new course_syllabus instance and save it
        syllabus_entry = course_syllabus(course=course, title=title, syllabus_desc=syllabus_desc)
        syllabus_entry.save()

    courses_all =courses.objects.exclude(isdelete=1)
    return render(request, 'syllabus.html', {'courses': courses_all})


def added_on(request,id):
    instance = course_syllabus()
    instance.added_on = timezone.now()  # Set added_on field to current date and time
    instance.save()

def added_by(request,id):
    instance = course_syllabus()
    instance.added_by = 0
    instance.save()
    
def view_syllabus(request):
    syllabus= course_syllabus.objects.exclude(isdelete=1)
    courses_list = courses.objects.exclude(isdelete=1)
    syllabus_with_course_names = []

    for syllabus in syllabus:
        course = get_object_or_404(courses, id=syllabus.course)
        syllabus_with_course_names.append({
            'id': syllabus.id,
            'course_name': course.course,  # Accessing the 'course' attribute of the 'course' object
            'title': syllabus.title,
            'syllabus_desc': syllabus.syllabus_desc,
            })
    return render(request,'syllabusview.html', {'syllabus': syllabus_with_course_names,'course':courses_list})

def update_syllabus(request,id):
    member = course_syllabus.objects.get(id=id)
    if request.method == 'POST':
        course = request.POST.get('course') # Update course details
        syllabus_desc = request.POST.get('syllabus_desc')
        title = request.POST.get('title')

        if course:# Save the course ID in the member.course field
            member.course = course    
        member.syllabus_desc= syllabus_desc
        member.title = title
        member.save()
    # Fetch all courses from the database
    coursename = courses.objects.exclude(isdelete=1)

    # Fetch the current course object to display its name
    current_course_obj = get_object_or_404(courses, id=member.course)
    current_course_name = current_course_obj.course
    return render(request,'syllabus_update.html',{'member':member,'course':coursename,'current_course_name': current_course_name})

def delesyllabus(request, id):
 # Soft delete by marking is_deleted as 1
    syllabus_instance = get_object_or_404(course_syllabus, id=id)
    syllabus_instance.isdelete = 1
    syllabus_instance.delete()
    syllabus_instance.save()
    return HttpResponseRedirect(reverse('view_syllabus'))


def application(request, id):
     # Fetch the Course_Application objects that match the course ID
    course_applications = Course_Application.objects.filter(course_id=id)

    # Fetch the related student objects
    student_ids = course_applications.values_list('student_id', flat=True)
    students = student.objects.filter(id__in=student_ids)

    # Fetch the course details
    course = get_object_or_404(courses, id=id)

    # Prepare the data for display
    context = {
        'courses': course,
        'students': students,
    }

    return render(request, 'course_application.html', context)

#category
def add_category(request):
    if request.method == 'POST':
        categoryadd = request.POST.get('categoryadd')
        myfile =request.FILES['image']
        fs = FileSystemStorage()
        f = fs.save(myfile.name, myfile)
        k = course_category(categoryadd=categoryadd, image=myfile)
        k.save()
        return redirect('show_category')
    return render(request, 'category.html')


def show_category(request):
    non_deleted_category = course_category.objects.exclude(isdelete=1)
    return render(request, 'category.html',{'category': non_deleted_category})

def deletecategory(request, id):
    # Soft delete by marking is_deleted as 1
    category_instance = get_object_or_404(course_category, id=id)
    category_instance.isdelete = 1
    category_instance.delete()
    category_instance.save()
    return HttpResponseRedirect(reverse(show_category))

def added_on(request,id):
    instance = course_category()
    instance.added_on = timezone.now()  # Set added_on field to current date and time
    instance.save()

def added_by(request,id):
    instance = course_category()
    instance.added_by = 0
    instance.save()

def update_category(request, id):
    member =course_category.objects.get(id=id)
    if request.method == 'POST':
        categoryadd = request.POST.get('categoryadd')
        member.categoryadd= categoryadd
        member.save()
        return HttpResponseRedirect(reverse('show_category'))
    return render(request,'category.html', {'members': member})

def application_course(request, id):
    # Fetch all Course_Application instances related to the student_id
    course_applications = Course_Application.objects.filter(student_id=id)
    
    # Extract course IDs from Course_Application instances
    course_ids = [course_app.course_id for course_app in course_applications]
    
    # Fetch all courses that match these IDs
    # Assuming you have a Course model defined
    course = courses.objects.filter(id__in=course_ids)
    
    context = {
        'student_id': id,
        'course': course,
    }
    return render(request, 'student_application.html', context)

#instructor
def add_instructor(request):
    if request.method == 'POST':
        name= request.POST.get('name')
        myfile =request.FILES['img']
        fs = FileSystemStorage()
        f = fs.save(myfile.name, myfile)
        course= request.POST.get('course')
        qualification= request.POST.get('qualification')
        experience= request.POST.get('experience')
        designation=request.POST.get('designation')
        k=Instructor(name=name,img=myfile,designation=designation,course=course,qualification=qualification,experience=experience)
        k.save()
        #return HttpResponseRedirect(reverse(show_instructor))
    course_inst=courses.objects.exclude(isdelete=1)
    return render(request,'instructor.html',{'course':course_inst})

def show_instructor(request):
    instructor= Instructor.objects.exclude(isdelete=1)  # Assuming `isdelete` is a BooleanField
    courses_list = courses.objects.exclude(isdelete=1)
    instructors_course_names = []

    for instructor in instructor:
        course = get_object_or_404(courses,id=instructor.course)
        instructors_course_names.append({
            'id': instructor.id,
            'course': course.course,
            'name': instructor.name,
            'img': instructor.img,
            'qualification': instructor.qualification,
            'experience': instructor.experience,
            'designation': instructor.designation,
        })
    return render(request, 'view_instructor.html',{'inst':instructors_course_names})

def delete_instructor(request, id):
    # Soft delete by marking is_deleted as 1
    instructor = get_object_or_404(Instructor, id=id)
    instructor.isdelete = 1
    instructor.delete()
    instructor.save()
    return HttpResponseRedirect(reverse(show_instructor))

def added_on(request,id):
    instance =Instructor()
    instance.added_on = timezone.now()  # Set added_on field to current date and time
    instance.save()

def added_by(request,id):
    instance = ()
    instance.added_by = 0
    instance.save()

def update_instructor(request, id):
    member = get_object_or_404(Instructor, id=id)
    if request.method == 'POST':
        name = request.POST.get('name')
        course = request.POST.get('course')
        qualification = request.POST.get('qualification')
        experience = request.POST.get('experience')
        designation = request.POST.get('designation')
        
        if 'img' in request.FILES:
            myfile = request.FILES['img']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            member.img = filename
        if course:# Save the course ID in the member.course field
            member.course = course    
        member.name = name    
        member.qualification = qualification
        member.experience = experience
        member.designation=designation
        member.save()

    # Fetch all courses from the database
    courses_list = courses.objects.exclude(isdelete=1)
    # Fetch the current course object to display its name
    current_course_obj = get_object_or_404(courses, id=member.course)
    current_course_name = current_course_obj.course
    
    return render(request, 'update_instruct.html', {
        'member': member,
        'current_course_name': current_course_name,
        'courses': courses_list
    })


def popularadd(request, id):
    item = get_object_or_404(courses, id=id)
    # Retrieve the is_popular parameter from the URL
    is_popular = request.GET.get('is_popular', '1')
    # Update the item based on the is_popular value
    item.is_popular = (is_popular == '0')
    item.save()
    return HttpResponseRedirect(reverse(courseview))


def apply(request):
    student_id = request.GET.get('student_id')
    
    if student_id:
        # Fetch all courses that are not deleted
        courses_not_deleted = courses.objects.exclude(isdelete=1)
        
        # Fetch IDs of courses applied by the student
        applied_courses_ids = Course_Application.objects.filter(student_id=student_id).values_list('course_id', flat=True)
        
        # Filter out courses that the student has already applied for
        courses_not_applied = courses_not_deleted.exclude(id__in=applied_courses_ids)
        
        # Prepare data in the desired format
        courses_data = [{'id': course.id, 'name': course.course} for course in courses_not_applied]
        
        if courses_data:
            return JsonResponse({'courses': courses_data}, status=200)
        else:
            return JsonResponse({'message': 'No courses available'}, status=204)

    elif request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        student_id = request.POST.get('student_id')
        course_id = request.POST.get('course_id')
        course_status = request.POST.get('course_status')
        payment_id = request.POST.get('payment_id')
        applied_on = request.POST.get('applied_on')
        applied_by = request.POST.get('applied_by')

        # Perform validation, save data to Course_Application
        application = Course_Application(
            student_id=student_id,
            course_id=course_id,
            course_status=course_status,
            payment_id=payment_id,
            applied_on=applied_on,
            applied_by=applied_by
        )
        application.save()

        # Return JSON response indicating success
        return JsonResponse({'message': 'Course Applied Successfully'})
    context = {
        'registers': student.objects.exclude(isdelete=1),
        'course': courses.objects.exclude(isdelete=1),
    }
    return render(request, 'applycourse.html', context)





