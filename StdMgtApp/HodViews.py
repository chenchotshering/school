import json
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from StdMgtApp.forms import AddStudentForm, EditStudentForm
from StdMgtApp.models import CustomUser, Courses, Subjects, Staffs, Students, SessionYearModel, FeedbackStudent, \
    FeedbackStaffs, LeaveReportStudent, LeaveReportStaff, Attendance, AttendanceReport


def admin_home(request):
    return render(request, "hod_template/home_content.html")


def add_staff(request):
    return render(request, "hod_template/add_staff_template.html")


def add_staff_save(request):
    if request.method != 'POST':
        return HttpResponse("Methond Not Allowed")
    else:
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        email = request.POST.get('email')

        try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email,
                                                  last_name=lastname,
                                                  first_name=firstname, user_type=2)
            user.staffs.address = address
            user.save()
            messages.success(request, "Successfully Added Staff")
            return HttpResponseRedirect(reverse("add_staff"))
        except:
            messages.error(request, "Failed to Add Staff")
            return HttpResponseRedirect(reverse("add_staff"))


def add_course(request):
    return render(request, "hod_template/add_course_template.html")


def add_course_save(request):
    if request.method != 'POST':
        return HttpResponse("Methond Not Allowed")
    else:
        course = request.POST.get('coursename')
        try:
            courses_model = Courses(name=course)
            courses_model.save()
            messages.success(request, "Successfully Added Course")
            return HttpResponseRedirect(reverse("add_course"))
        except:
            messages.error(request, "Failed to Add Course")
            return HttpResponseRedirect(reverse("add_course"))


def add_session_save(request):
    if request.method != "POST":
        return HttpResponse(reverse("manage_session"))
    else:
        start_session = request.POST.get('session_start_year')
        end_session = request.POST.get('session_end_year')
        try:
            session = SessionYearModel(session_start_year=start_session, session_end_year=end_session)
            session.save()
            messages.success(request, "Successfully Added Session")
            return HttpResponseRedirect(reverse("manage_session"))
        except:
            messages.error(request, "Failed to Add Session")
            return HttpResponseRedirect(reverse("session_Session"))


def add_student(request):
    form = AddStudentForm()
    return render(request, "hod_template/add_student_template.html", {"form": form})


def add_student_save(request):
    if request.method != 'POST':
        return HttpResponse("Method Not Allowed")
    else:
        form = AddStudentForm(request.POST, request.FILES)
        if form.is_valid():
            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            address = form.cleaned_data['address']
            email = form.cleaned_data['email']
            session_year_id = form.cleaned_data['session_year_id']
            course_id = form.cleaned_data['course']
            sex = form.cleaned_data['sex']

            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)

            try:
                user = CustomUser.objects.create_user(username=username, password=password, email=email,
                                                      last_name=lastname,
                                                      first_name=firstname, user_type=3)
                user.students.address = address
                course_obj = Courses.objects.get(id=course_id)
                user.students.course_id = course_obj

                session_year = SessionYearModel.objects.get(id=session_year_id)
                user.students.session_year_id = session_year
                user.students.profile_pic = profile_pic_url
                user.students.sex = sex
                user.save()
                messages.success(request, "Successfully Added Student")
                return HttpResponseRedirect(reverse("add_student"))
            except:
                messages.error(request, "Failed to Add Student")
                return HttpResponseRedirect(reverse("add_student"))
        else:
            form = AddStudentForm(request.POST)
            return render(request, "hod_template/add_student_template.html", {"form": form})


def add_subject(request):
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type=2)
    return render(request, "hod_template/add_subject_template.html", {"courses": courses, "staffs": staffs})


def add_subject_save(request):
    if request.method != "POST":
        return HttpResponse("<h3>Method not Allowed</h3>")
    else:
        subject = request.POST.get('subjectname')
        course_id = request.POST.get('course')
        course = Courses.objects.get(id=course_id)
        staff_id = request.POST.get('staff')
        staff = CustomUser.objects.get(id=staff_id)

        try:
            subject = Subjects(name=subject, course_id=course, staff_id=staff)
            subject.save()
            messages.success(request, "Successfully Added Subject")
            return HttpResponseRedirect(reverse("add_subject"))
        except:
            messages.error(request, "Failed to Add Subject")
            return HttpResponseRedirect(reverse("add_subject"))


def manage_staff(request):
    staffs = Staffs.objects.all()
    return render(request, "hod_template/manage_staff.html", {"staffs": staffs})


def manage_student(request):
    students = Students.objects.all()
    return render(request, "hod_template/manage_student_template.html", {"students": students})


def manage_course(request):
    courses = Courses.objects.all()
    return render(request, "hod_template/manage_course_template.html", {"courses": courses})


def manage_subject(request):
    subjects = Subjects.objects.all()
    return render(request, "hod_template/manage_subject_template.html", {"subjects": subjects})


def manage_session(request):
    sessions = SessionYearModel.objects.all()
    return render(request, "hod_template/manage_session_template.html", {"session": sessions})


def edit_staff(request, staff_id):
    staff = Staffs.objects.get(admin=staff_id)
    return render(request, "hod_template/edit_staff_template.html", {"staff": staff, "id": staff_id})


def edit_staff_save(request):
    if request.method != 'POST':
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        staff_id = request.POST.get("staff_id")
        first_name = request.POST.get("firstname")
        last_name = request.POST.get("lastname")
        email = request.POST.get("email")
        username = request.POST.get("username")
        address = request.POST.get("address")

        try:
            user = CustomUser.objects.get(id=staff_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()

            staff_model = Staffs.objects.get(admin=staff_id)
            staff_model.address = address
            staff_model.save()

            messages.success(request, "Successfully Edited Staff")
            return HttpResponseRedirect(reverse("edit_staff", kwargs={"staff_id": staff_id}))
        except:
            messages.error(request, "Failed to edit Staff Details")
            return HttpResponseRedirect(reverse("edit_staff", kwargs={"staff_id": staff_id}))


def edit_student(request, student_id):
    request.session['student_id'] = student_id
    student = Students.objects.get(admin=student_id)
    form = EditStudentForm()
    form.fields['email'].initial = student.admin.email
    form.fields['firstname'].initial = student.admin.first_name
    form.fields['lastname'].initial = student.admin.last_name
    form.fields['username'].initial = student.admin.username
    form.fields['address'].initial = student.address
    form.fields['course'].initial = student.course_id.id
    form.fields['sex'].initial = student.gender
    form.fields['session_year_id'].initial = student.session_year_id.id

    return render(request, "hod_template/edit_student_template.html",
                  {"form": form, "id": student_id, "username": student.admin.username})


def edit_student_save(request):
    if request.method != 'POST':
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        std_id = request.session.get('student_id')
        if std_id is None:
            return HttpResponseRedirect(reverse("manage_student"))

        form = EditStudentForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data['firstname']
            last_name = form.cleaned_data['lastname']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            address = form.cleaned_data['address']
            course_id = form.cleaned_data['course']
            sex = form.cleaned_data['sex']
            session_year_id = form.cleaned_data['session_year_id']

            if request.FILES.get('profile_pic', False):
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None

            try:
                user = CustomUser.objects.get(id=std_id)
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.username = username
                user.save()

                std_model = Students.objects.get(admin=std_id)
                std_model.address = address
                std_model.course_id.course = course_id
                std_model.gender = sex

                session_year = SessionYearModel.objects.get(id=session_year_id)
                std_model.session_year_id = session_year

                courses = Courses.objects.get(id=course_id)
                std_model.course_id = courses

                if profile_pic_url != None:
                    std_model.profile_pic = profile_pic_url
                std_model.save()

                del request.session['student_id']

                messages.success(request, "Successfully Edited Student")
                return HttpResponseRedirect(reverse("edit_student", kwargs={"student_id": std_id}))
            except:
                messages.error(request, "Failed to edit Student Details")
                return HttpResponseRedirect(reverse("edit_student", kwargs={"student_id": std_id}))
        else:
            form = EditStudentForm(request.POST)
            student = Students.objects.get(admin=std_id)
            return render(request, "hod_template/edit_student_template.html",
                          {"form": form, "id": std_id, "username": student.admin.username})


def edit_course(request, course_id):
    course = Courses.objects.get(id=course_id)
    return render(request, "hod_template/edit_course_template.html", {"courses": course, "id": course_id})


def edit_course_save(request):
    if request.method != 'POST':
        return HttpResponse(" Method Not Allowed!")
    else:
        course_name = request.POST.get('coursename')
        course_id = request.POST.get('course_id')
        try:
            courses = Courses.objects.get(id=course_id)
            courses.name = course_name
            courses.save()

            messages.success(request, "Successfully Edited Course")
            return HttpResponseRedirect(reverse("edit_course", kwargs={"course_id": course_id}))
        except:
            messages.error(request, "Couldn't Edit the Course")
            return HttpResponseRedirect(reverse("edit_course", kwargs={"course_id": course_id}))


def edit_subject(request, subject_id):
    subject = Subjects.objects.get(id=subject_id)
    course = Courses.objects.all()
    staff = CustomUser.objects.all()
    return render(request, "hod_template/edit_subject_template.html",
                  {"subjects": subject, "courses": course, "staffs": staff, "id": subject_id})


def edit_subject_save(request):
    if request.method != 'POST':
        return HttpResponse("Method not Allowed!")
    else:
        subject_id = request.POST.get('subject_id')
        subject_name = request.POST.get('subjectname')
        staff_id = request.POST.get('staff')
        course_id = request.POST.get('course')

        try:
            subjects = Subjects.objects.get(id=subject_id)
            subjects.name = subject_name
            staff = CustomUser.objects.get(id=staff_id)
            subjects.staff_id = staff
            courses = Courses.objects.get(id=course_id)
            subjects.course_id = courses
            subjects.save()

            messages.success(request, "Successfully Edited Subjects")
            return HttpResponseRedirect("edit_subject/" + subject_id)
            return HttpResponseRedirect(reverse("edit_subject", kwargs={"subject_id": subject_id}))
        except:
            messages.error(request, "Failed to Edit the Subject")
            return HttpResponseRedirect(reverse("edit_subject", kwargs={"subject_id": subject_id}))


@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    user_obj = CustomUser.objects.filter(email=email).exists()

    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_username_exist(request):
    username = request.POST.get("username")
    user_obj = CustomUser.objects.filter(username=username).exists()

    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


def staff_feedback_msg(request):
    feedbacks = FeedbackStaffs.objects.all()
    return render(request, "hod_template/staff_feedback_reply.html", {"feedbacks": feedbacks})


def student_feedback_msg(request):
    feedbacks = FeedbackStudent.objects.all()
    return render(request, "hod_template/student_feedback_reply.html", {"feedbacks": feedbacks})


@csrf_exempt
def staff_feedback_msg_replied(request):
    feedback_id = request.POST.get("id")
    feedback_msg = request.POST.get("message")

    try:
        feedback = FeedbackStaffs.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_msg
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")


@csrf_exempt
def student_feedback_msg_replied(request):
    feedback_id = request.POST.get("id")
    feedback_msg = request.POST.get("message")

    try:
        feedback = FeedbackStudent.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_msg
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")


def student_leave_view(request):
    leaves = LeaveReportStudent.objects.all()
    return render(request, "hod_template/student_leave_view.html", {"leaves": leaves})


def student_leave_approve(request, leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return HttpResponseRedirect(reverse("student_leave_view"))


def student_leave_disapprove(request, leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return HttpResponseRedirect(reverse("student_leave_view"))


def staff_leave_view(request):
    leaves = LeaveReportStaff.objects.all()
    return render(request, "hod_template/staff_leave_view.html", {"leaves": leaves})


def staff_leave_approve(request, leave_id):
    leave = LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return HttpResponseRedirect(reverse("staff_leave_view"))


def staff_leave_disapprove(request, leave_id):
    leave = LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return HttpResponseRedirect(reverse("staff_leave_view"))


def admin_view_attendance(request):
    subjects = Subjects.objects.all()
    session_year_id = SessionYearModel.objects.all()
    return render(request, "hod_template/admin_view_attendance.html",
                  {"subjects": subjects, "session_year_id": session_year_id})


@csrf_exempt
def admin_get_attendance_dates(request):
    subject = request.POST.get("subject")
    session_year_id = request.POST.get("session_year_id")
    subject_obj = Subjects.objects.get(id=subject)
    session_obj = SessionYearModel.objects.get(id=session_year_id)
    attendance = Attendance.objects.filter(subject_id=subject_obj, session_year_id=session_obj)
    attendance_obj = []
    for attendance_single in attendance:
        data = {"id": attendance_single.id, "attendance_date": str(attendance_single.attendance_date),
                "session_year_id": attendance_single.session_year_id.id}
        attendance_obj.append(data)
    return JsonResponse(json.dumps(attendance_obj), safe=False)


@csrf_exempt
def admin_get_attendance_student(request):
    attendance_date = request.POST.get("attendance_date")
    attendance = Attendance.objects.get(id=attendance_date)

    attendance_data = AttendanceReport.objects.filter(attendance_id=attendance)
    list_data = []

    for student in attendance_data:
        data_small = {"id": student.student_id.admin.id,
                      "name": student.student_id.admin.first_name + " " + student.student_id.admin.last_name,
                      "status": student.status}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


def admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    return render(request, "hod_template/admin_profile.html", {"user": user})


def edit_profile_save(request):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse("admin_profile"))
    else:
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        password = request.POST.get('password')

        try:
            profile = CustomUser.objects.get(id=request.user.id)
            profile.first_name = first_name
            profile.last_name = last_name
            if password != None and password != "":
                profile.set_password(password)
            profile.save()

            messages.success(request, "Profile Updated")
            return HttpResponseRedirect(reverse('admin_profile'))
        except:
            messages.error(request, "Failed to Edit Profile")
        return HttpResponseRedirect(reverse("admin_profile"))
