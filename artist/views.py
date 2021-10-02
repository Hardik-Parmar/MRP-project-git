from django.http.response import FileResponse, Http404
from accounts.models import Document, Profile
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from accounts.models import FinalProduct
from django.views.generic import TemplateView
from django.db.models import Sum
# for creating user
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
# for authenticating user
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def artistHome(request):
    if(request.user):
        return render(request, "artist1/home.html")

def artistHomeWithOutLogin(request):
    return render(request, "artist1/home2.html")

#Login
def handleLogin(request):
    if (request.method == 'POST'):
        # get the POST parameter
        loginusername = request.POST.get('loginusername', '')
        loginpassword = request.POST.get('loginpassword', '')

        # validating input data
        if (loginusername == ""):
            messages.error(request, "Username can not be empty")
            return redirect('statichome')

        if (loginpassword == ""):
            messages.error(request, "Password can not be empty")
            return redirect('statichome')
        
        try:
            obj1 = User.objects.get(username = loginusername)
        
            if(obj1 != None):
                obj2 = Profile.objects.get(user = obj1)
                user_type = obj2.User_Type
                if(user_type == 'Artist'):
                    # First authenticate the user (CHECK USERNAME AND PASSWORD)
                    user = authenticate(username=loginusername, password=loginpassword)

                    # if authentication fails then USER become "NONE"
                    if (user is not None):
                        # if user is authenticated then and then it will enter inside IF block and then LOGIN allowed
                        if(obj2.admin_approval_status):
                            login(request, user)
                            request.session['name'] = obj1.first_name
                            request.session['username'] = obj1.username
                            request.session['id'] = obj1.id
                            messages.success(request, "Successfully Logged in")
                            return redirect('home/')
                        else:
                            messages.error(request, 'Please wait till Admin approves the your registration request')
                            return redirect('statichome')
                    else:
                        messages.error(request, "Invalid Credentials please try again")
                        return redirect('statichome')
                    
                else:
                    messages.error(request, "Sorry..!! only 'Artist' users are allowed to be Logged-In here.")
                    return redirect('statichome')
            else:
                messages.error(request, "Sorry..!! you are not registered with our System, Contact Admin")
                return redirect('statichome')
                    
        except:
            messages.error(request, "Sorry..!! you are not registered with our System, Contact Admin")
            return redirect('statichome')
    else:
        return HttpResponse("ERROR")

    return HttpResponse("404 Not Found")

#Logout
def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully Logged Out")
    return redirect('statichome')

#View Documents
def viewDocuments(request):
    dict1 = {}
    try:
        obj = Document.objects.filter(artist_name = request.user, admin_approval_status = True)
        # obj = Document.objects.all()
        # print(obj[1].document.url)
    
        dict1 = {'context' : obj}
    except:
        messages.error(request, "Please Log-In")
        return redirect('statichome')
        
    return render(request, "artist1/documents.html", dict1)

# @login_required(login_url='artist/home.html')
class ClubChartView(LoginRequiredMixin, TemplateView):
    template_name='artist1/home.html'
    login_url = 'statichome'
    # print(request)
    # @method_decorator(login_required)
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # if(user.is_authenticated):
                
        # print(user)
        # try:
        context['qs'] = FinalProduct.objects.filter(artist = user.first_name)
        context['total_rbt'] = FinalProduct.objects.filter(artist = user.first_name).aggregate(Sum('rbt_val'))
        context['total_kisom'] = FinalProduct.objects.filter(artist = user.first_name).aggregate(Sum('kisom_val'))
        context['total_altafonte_aoa'] = FinalProduct.objects.filter(artist = user.first_name).aggregate(Sum('altafonte_aoa'))
        context['total_artista'] = FinalProduct.objects.filter(artist = user.first_name).aggregate(Sum('total_artista'))
    
        # print(context['total_artista'])
        return context
        # # except:
        #     #     return render(self.request, 'artist/home2.html')
        # else:
        #     template_name = 'artist/home2.html'
        #     context = super().get_context_data(**kwargs)
        #     return context
