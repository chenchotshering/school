import datetime

from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from StdMgtApp.models import Subjects, AttendanceReport, Students, Courses, CustomUser, Attendance, LeaveReportStudent, \
    FeedbackStudent


def student_home(request):
    return render(request, "student_template/student_home_template.html")


def student_view_attendance(request):
    student = Students.objects.get(admin=request.user.id)
    # course = Courses.objects.get(id=student.course_id.id)
    course = student.course_id
    subjects = Subjects.objects.filter(course_id=course)
    return render(request, "student_template/student_view_attendance.html", {"subjects": subjects})


def student_view_attendance_post(request):
    subject_id = request.POST.get('subject')
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')

    start_date_parse = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date_parse = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
    subject_obj = Subjects.objects.get(id=subject_id)
    user_obj = CustomUser.objects.get(id=request.user.id)
    std_obj = Students.objects.get(admin=user_obj)

    attendance = Attendance.objects.filter(attendance_date__range=(start_date_parse, end_date_parse),
                                           subject_id=subject_obj)
    attendance_reports = AttendanceReport.objects.filter(attendance_id__in=attendance, student_id=std_obj)

    #for attendance_report in attendance_reports:
    #    print("Date :" + str(attendance_report.attendance_id.attendance_date),"Status :" + str(attendance_report.status))
    #return HttpResponse("OKie")
    return  render(request,"student_template/student_attendance_data.html",{"attendance_reports":attendance_reports})


def student_apply_leave(request):
    student_obj = Students.objects.get(admin=request.user.id)
    leave_data = LeaveReportStudent.objects.filter(student_id=student_obj)
    return render(request, "student_template/student_apply_leave.html",{"leave_data":leave_data})


def student_apply_leave_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("student_apply_leave"))
    else:
        leave_date = request.POST.get("leave_date")
        leave_msg = request.POST.get("leave_msg")

        student = Students.objects.get(admin=request.user.id)
        try:
            leave_report = LeaveReportStudent(student_id=student,leave_date=leave_date,leave_message=leave_msg, leave_status=0)
            leave_report.save()

            messages.success(request, "Leave Applied Successfully")
            return HttpResponseRedirect(reverse("student_apply_leave"))
        except:
            messages.error(request, "Failed to Apply for Leave")
            return HttpResponseRedirect(reverse("student_apply_leave"))


def student_feedback(request):
    student_obj = Students.objects.get(admin=request.user.id)
    feedback_data = FeedbackStudent.objects.filter(student_id=student_obj)
    return render(request,"student_template/student_feedback.html", {"feedback_data":feedback_data})


def student_feedback_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("student_feedback_save"))
    else:
        feedback_msg = request.POST.get("feedback_msg")

        student = Students.objects.get(admin=request.user.id)
        try:
            feedback_report = FeedbackStudent(student_id=student, feedback=feedback_msg)
            feedback_report.save()

            messages.success(request, "Your Feedback is Successfully Sent")
            return HttpResponseRedirect(reverse("student_feedback"))
        except:
            messages.error(request, "Couldn't submit the Feedback")
            return HttpResponseRedirect(reverse("student_feedback"))


def student_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    student = Students.objects.get(admin=user.id)
    return render(request, "student_template/student_profile.html", {"user": user, "students": student})


def student_profile_save(request):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse("staff_profile"))
    else:
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        password = request.POST.get('password')
        address = request.POST.get('address')

        try:
            profile = CustomUser.objects.get(id=request.user.id)
            profile.first_name = first_name
            profile.last_name = last_name
            if password != None and password != "":
                profile.set_password(password)
            profile.save()

            students = Students.objects.get(admin=profile.id)
            students.address = address
            students.save()

            messages.success(request, "Profile Updated")
            return HttpResponseRedirect(reverse('student_profile'))
        except:
            messages.error(request, "Failed to Edit Profile")
        return HttpResponseRedirect(reverse("student_profile"))

