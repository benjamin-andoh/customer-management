from django.http import HttpResponse
from django.shortcuts import redirect


# logged in user should not access the register or log in page
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            # stay on the homepage
            return redirect('home')
        else:
            # if the user is not authenticated, login
            return view_func(request, *args, **kwargs)
    return wrapper_func


# allowed users on a page: who view what page
# pass in the role
def allowed_users(allowed_roles=[]):
    # pass in the view function
    def decorator(view_func):
        def wrapper_fun(request, *args, **kwargs):

            group = None  # if a list of groups exists
            # check if a user is part of a group
            if request.user.groups.exists():
                # set the group value to the first group in the list
                group = request.user.groups.all()[0].name

            # if the group is the our allowed roles
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page')
        return wrapper_fun
    return decorator


# decorators that takes only the view parameter
def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'customer':
            return redirect('user-page')
        elif group == 'admin':
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("you are neither a customer nor an "
                                "admin yet please contact admin to put you in a group")
    return wrapper_func
