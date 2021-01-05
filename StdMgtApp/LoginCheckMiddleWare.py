from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class LoginCheckMiddleWare(MiddlewareMixin):

    def process_view(self,request,view_func,view_args,view_kwargs):
        modulename=view_func.__module__
        #print(modulename)
        #print(request.path)
        user = request.user
        if user.is_authenticated:
            if user.user_type=="1":
                if modulename == "StdMgtApp.HodViews":
                    pass
                elif modulename == "StdMgtApp.views" or modulename == "django.views.static":
                    pass
                else:
                    return HttpResponseRedirect(reverse("admin_home"))
            elif user.user_type=="2":
                if modulename == "StdMgtApp.StaffViews":
                    pass
                elif modulename == "StdMgtApp.views" or modulename == "django.views.static":
                    pass
                else:
                    return HttpResponseRedirect(reverse("staff_home"))
            elif user.user_type=="3":
                if modulename == "StdMgtApp.StudentViews":
                    pass
                elif modulename == "StdMgtApp.views" or modulename == "django.views.static":
                    pass
                else:
                    return HttpResponseRedirect(reverse("student_home"))
            else:
                    return HttpResponseRedirect(reverse("show_login"))
        else:
            if request.path == reverse("show_login") or request.path == reverse("dologin") or modulename == "django.contrib.auth.views":
                pass

            else:
                return HttpResponseRedirect(reverse("show_login"))

