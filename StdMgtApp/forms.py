from django import forms

from StdMgtApp.models import Courses, SessionYearModel


class DateInput(forms.DateInput):
    input_type = "date"


class AddStudentForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50,
                             widget=forms.EmailInput(attrs={"class": "form-control", "autocomplete": "off"}))
    firstname = forms.CharField(label="First Name", max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
    lastname = forms.CharField(label="Last Name", max_length=50,
                               widget=forms.TextInput(attrs={"class": "form-control"}))
    username = forms.CharField(label="Username", max_length=50,
                               widget=forms.TextInput(attrs={"class": "form-control", "autocomplete": "off"}))
    password = forms.CharField(label="Password", max_length=50,
                               widget=forms.PasswordInput(attrs={"class": "form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))

    course_list = []

    courses = Courses.objects.all()
    for course in courses:
        small_course = (course.id, course.name)
        course_list.append(small_course)
        #print(course_list)
        # course_list = []
    course = forms.ChoiceField(label="Course", choices=course_list,
                               widget=forms.Select(attrs={"class": "form-control"}))

    session_list = []
    try:
        sessions = SessionYearModel.objects.all()
        for session in sessions:
            small_sess = (session.id, str(session.session_start_year) + " To " + str(session.session_end_year))
            session_list.append(small_sess)
    except:
        session_list = []

    gender_choice = (
        ("Male", "Male"),
        ("Female", "Female")
    )
    sex = forms.ChoiceField(label="Gender", choices=gender_choice, widget=forms.Select(attrs={"class": "form-control"}))
    session_year_id = forms.ChoiceField(label="Session Year", choices=session_list,
                                        widget=forms.Select(attrs={"class": "form-control"}))
    profile_pic = forms.FileField(label="Profile Picture", max_length=50,
                                  widget=forms.FileInput(attrs={"class": "form-control"}))


class EditStudentForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class": "form-control"}))
    firstname = forms.CharField(label="First Name", max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
    lastname = forms.CharField(label="Last Name", max_length=50,
                               widget=forms.TextInput(attrs={"class": "form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))

    course_list = []
    try:
        courses = Courses.objects.all()
        for course in courses:
            small_course = (course.id, course.name)
            course_list.append(small_course)
    except:
        course_list = []
    course = forms.ChoiceField(label="Course", choices=course_list,
                               widget=forms.Select(attrs={"class": "form-control"}))

    session_list = []
    try:
        sessions = SessionYearModel.objects.all()
        for session in sessions:
            small_sess = (session.id, str(session.session_start_year) + " To " + str(session.session_end_year))
            session_list.append(small_sess)
    except:
        session_list = []

    gender_choice = (
        ("Male", "Male"),
        ("Female", "Female")
    )
    sex = forms.ChoiceField(label="Gender", choices=gender_choice, widget=forms.Select(attrs={"class": "form-control"}))
    session_year_id = forms.ChoiceField(label="Session Year", choices=session_list,
                                        widget=forms.Select(attrs={"class": "form-control"}))
    profile_pic = forms.FileField(label="Profile Picture", max_length=50,
                                  widget=forms.FileInput(attrs={"class": "form-control"}), required=False)
