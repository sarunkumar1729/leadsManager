from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from functools import wraps
from app.models import Counsellor,Lead,login_details
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from user_agents import parse



def home(request):
      return render(request,'index.html')

def check_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)

def create_user(request):
      if request.method=='POST':
            name=request.POST['name']
            email=request.POST['email']
            center=request.POST['center']
            username=request.POST['username']
            password=request.POST['password']
            user_type=request.POST['user_type']
            if not User.objects.filter(username=username):

                  user=User.objects.create_user(first_name=name,username=username,email=email,password=password)
                  if user_type == "counsellor":
                        user.save()
                        counsellor=Counsellor(user=user,center=center)
                        counsellor.save()
                  else:
                        user.is_superuser=True
                        user.is_staff=True
                        user.save()
                  print('user created') # use alert
                  return render(request,'admin/create_user.html')
            else:
                  print('username already exist') # use ajax here
                  return render(request,'admin/create_user.html')
      else:
            return render(request,'admin/create_user.html')
      
def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return redirect('admin_login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def user_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.is_staff:
            return redirect('user_login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# def admin_login(request):
#       if request.method=='POST':
#             username=request.POST['username']
#             password=request.POST['password']
#             user=authenticate(username=username,password=password)
#             if user is not None:
#                   login(request,user)
#                   return redirect('admin_home')
#             else:
#                   return render(request,'admin/login.html')
#       else:
#             return render(request,'admin/login.html')

def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)

            # Capture device details
            user_agent_string = request.META.get('HTTP_USER_AGENT', '')
            user_agent = parse(user_agent_string)
            device_details = {
                'browser': user_agent.browser.family,
                'browser_version': user_agent.browser.version_string,
                'os': user_agent.os.family,
                'os_version': user_agent.os.version_string,
                'device': user_agent.device.family,
                'is_mobile': user_agent.is_mobile,
                'is_tablet': user_agent.is_tablet,
                'is_pc': user_agent.is_pc,
                'is_bot': user_agent.is_bot,
            }

            # Optionally, log the device details or store them in the user profile
            print(f"User logged in from: {device_details}")
            new_login = login_details(
                 user=user,
                 browser=user_agent.browser.family,
                 browser_version=user_agent.browser.version_string,
                 os=user_agent.os.family,
                 os_version=user_agent.os.version_string,
                 device=user_agent.device.family,
                 is_mobile=user_agent.is_mobile,
                 is_tablet=user_agent.is_tablet,
                 is_pc=user_agent.is_pc,
                 is_bot=user_agent.is_bot
            )
            new_login.save()
            return redirect('admin_home')
        else:
            return render(request, 'admin/login.html', {'error': 'Invalid credentials'})
    else:
        return render(request, 'admin/login.html')

# def user_login(request):
#       if request.method=='POST':
#             username=request.POST['username']
#             password=request.POST['password']
#             user=authenticate(username=username,password=password)
#             if user is not None:
#                   login(request,user)
#                   return redirect('user_home')
#             else:
#                   return render(request,'user/login.html')
#       else:
#             return render(request,'user/login.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            counsellor = Counsellor.objects.get(user=user)
            if counsellor.status:
                  login(request, user)
                  # Capture device details
                  user_agent_string = request.META.get('HTTP_USER_AGENT', '')
                  user_agent = parse(user_agent_string)
                  device_details = {
                  'browser': user_agent.browser.family,
                  'browser_version': user_agent.browser.version_string,
                  'os': user_agent.os.family,
                  'os_version': user_agent.os.version_string,
                  'device': user_agent.device.family,
                  'is_mobile': user_agent.is_mobile,
                  'is_tablet': user_agent.is_tablet,
                  'is_pc': user_agent.is_pc,
                  'is_bot': user_agent.is_bot,
                  }

                  # Optionally, log the device details or store them in the user profile
                  print(f"User logged in from: {device_details}")
                  new_login = login_details(
                  user=user,
                  browser=user_agent.browser.family,
                  browser_version=user_agent.browser.version_string,
                  os=user_agent.os.family,
                  os_version=user_agent.os.version_string,
                  device=user_agent.device.family,
                  is_mobile=user_agent.is_mobile,
                  is_tablet=user_agent.is_tablet,
                  is_pc=user_agent.is_pc,
                  is_bot=user_agent.is_bot
                  )
                  new_login.save()
                  return redirect('user_home')
            else:
                 return render(request,'user/login.html')
        else:
            return render(request, 'user/login.html', {'error': 'Invalid credentials'})
    else:
        return render(request, 'user/login.html')


def user_logout(request):
      logout(request)
      return redirect('home')
      
@admin_required
def admin_home(request):
      counsellors=Counsellor.objects.all()
      kochi_leads = Lead.objects.filter(joining_centre = 'kochi').count()
      converted_kochi_leads = Lead.objects.filter(Q(joining_centre='kochi') & Q(status='batch confirmed')).count()
      calicut_leads = Lead.objects.filter(joining_centre = 'calicut').count()
      converted_calicut_leads = Lead.objects.filter(Q(joining_centre='calicut') & Q(status='batch confirmed')).count()
      palakkad_leads = Lead.objects.filter(joining_centre = 'palakkad').count()
      converted_palakkad_leads = Lead.objects.filter(Q(joining_centre='palakkad') & Q(status='batch confirmed')).count()
      total_leads = kochi_leads+calicut_leads+palakkad_leads
      total_converted_leads = converted_kochi_leads+converted_calicut_leads+converted_palakkad_leads
      # login times
      superusers = User.objects.filter(is_superuser=True).order_by('-last_login')
      users = Counsellor.objects.all() 
      # leads cound
      warm_count=Lead.objects.filter(status='warm').count()
      cold_count=Lead.objects.filter(status='cold').count()
      confirmed_count=Lead.objects.filter(status='batch confirmed').count()
      not_intrested_count=Lead.objects.filter(status='not intrested').count()
      registration_fee_paid_count=Lead.objects.filter(status='registration fee paid').count()
      demo_requested_count=Lead.objects.filter(status='demo requested').count()
      demo_provided_count=Lead.objects.filter(status='demo provided').count()
      
      data_science=Lead.objects.filter(Q(status='batch confirmed') & Q(course='data science')).count()
      data_analytics=Lead.objects.filter(Q(status='batch confirmed') & Q(course='data analytics')).count()
      business_analytics=Lead.objects.filter(Q(status='batch confirmed') & Q(course='business analytics')).count()
      python_fullstack =Lead.objects.filter(Q(status='batch confirmed') & Q(course='python fullstack')).count()
      software_testing=Lead.objects.filter(Q(status='batch confirmed') & Q(course='software testing')).count()
      MERN_stack=Lead.objects.filter(Q(status='batch confirmed') & Q(course='MERN stack')).count()
      
      january = Lead.objects.filter(Q(status='batch confirmed') & Q(joining_month='2024-01')).count()
      february = Lead.objects.filter(Q(status='batch confirmed') & Q(joining_month='2024-02')).count()
      march = Lead.objects.filter(Q(status='batch confirmed') & Q(joining_month='2024-03')).count()
      april = Lead.objects.filter(Q(status='batch confirmed') & Q(joining_month='2024-04')).count()
      may = Lead.objects.filter(Q(status='batch confirmed') & Q(joining_month='2024-05')).count()
      june = Lead.objects.filter(Q(status='batch confirmed') & Q(joining_month='2024-06')).count()
      july = Lead.objects.filter(Q(status='batch confirmed') & Q(joining_month='2024-07')).count()
      august = Lead.objects.filter(Q(status='batch confirmed') & Q(joining_month='2024-08')).count()
      september = Lead.objects.filter(Q(status='batch confirmed') & Q(joining_month='2024-09')).count()
      october = Lead.objects.filter(Q(status='batch confirmed') & Q(joining_month='2024-10')).count()
      november = Lead.objects.filter(Q(status='batch confirmed') & Q(joining_month='2024-11')).count()
      december = Lead.objects.filter(Q(status='batch confirmed') & Q(joining_month='2024-12')).count()

      context={
           'ds':data_science,'da':data_analytics,'ba':business_analytics,'pf':python_fullstack,'st':software_testing,'ms':MERN_stack,
                  'counsellors':counsellors,
                  'kochi_leads':kochi_leads,
                  'converted_kochi_leads':converted_kochi_leads,
                  'calicut_leads':calicut_leads,
                  'converted_calicut_leads':converted_calicut_leads,
                  'palakkad_leads':palakkad_leads,
                  'converted_palakkad_leads':converted_palakkad_leads,
                  'total_leads':total_leads,
                  'total_converted_leads':total_converted_leads,
                  'superusers':superusers,
                  'users':users,
                  'warm':warm_count,
                  'cold':cold_count,
                  'confirmed':confirmed_count,
                  'not_intrested':not_intrested_count,
                  'registration_fee_paid':registration_fee_paid_count,
                  'demo_requested':demo_requested_count,
                  'demo_provided':demo_provided_count,
                  'january':january,'february':february,'march':march,'april':april,'may':may,'june':june,'july':july,'august':august,
            'september':september,'october':october,'november':november,'december':december
            }
      return render(request,'admin/home.html',context)

@user_required
def user_home(request):
      leads=Lead.objects.filter(counsellor=request.user)
      warm_count=Lead.objects.filter(Q(counsellor=request.user) & Q(status='warm')).count()
      cold_count=Lead.objects.filter(Q(counsellor=request.user) & Q(status='cold')).count()
      confirmed_count=Lead.objects.filter(Q(counsellor=request.user) & Q(status='batch confirmed')).count()
      not_intrested_count=Lead.objects.filter(Q(counsellor=request.user) & Q(status='not intrested')).count()
      registration_fee_paid_count=Lead.objects.filter(Q(counsellor=request.user) & Q(status='registration fee paid')).count()
      demo_requested_count=Lead.objects.filter(Q(counsellor=request.user) & Q(status='demo requested')).count()
      demo_provided_count=Lead.objects.filter(Q(counsellor=request.user) & Q(status='demo provided')).count()
      next_year=Lead.objects.filter(Q(counsellor=request.user) & Q(status='next year')).count()
      context={
            'leads':leads,'warm':warm_count,'cold':cold_count,'confirmed':confirmed_count,'not_intrested':not_intrested_count,'registration_fee_paid':registration_fee_paid_count,'demo_requested':demo_requested_count,'demo_provided':demo_provided_count,'next_year':next_year
            }
      return render(request,'user/home.html',context)

# def leads(request):
#       leads=Lead.objects.filter(counsellor=request.user)
#       context={'leads':leads}
#       return render(request,'user/leads.html',context)

def add_lead(request):
      if request.method=='POST':
            name=request.POST['name']
            phone=request.POST['phone']
            date=request.POST['date']
            source_of_lead=request.POST['source']
            # counsellor=request.POST['counsellor']
            mode=request.POST['mode']
            status=request.POST['status']
            joining_center=request.POST['joining_center']
            course=request.POST['course']
            education=request.POST['education']
            stream=request.POST['stream']
            cs_background=request.POST['cs_background']
            if cs_background=='yes':
                  cs_background=True
            else:
                  cs_background=False
            employed=request.POST['employed']
            if employed=='yes':
                  employed=True
            else:
                  employed=False
            joining_month=request.POST['joining_month']
            additional_notes=request.POST['additional_notes']
            initial_response=request.POST['initial_response']
            first_follow_up=request.POST['first_follow_up']
            first_follow_up_date=request.POST['first_follow_up_date']
            second_follow_up=request.POST['second_follow_up']
            second_follow_up_date=request.POST['second_follow_up_date']
            third_follow_up=request.POST['third_follow_up']
            third_follow_up_date=request.POST['third_follow_up_date']
            print(
                  name,
                  phone,date,source_of_lead,
                  mode,
                  source_of_lead,
                  status,
                  joining_center,
                  course,
                  education,
                  stream,
                  cs_background,
                  employed,
                  joining_month,
                  additional_notes,
                  initial_response,
                  first_follow_up,
                  first_follow_up_date,
                  second_follow_up,
                  second_follow_up_date,
                  third_follow_up,
                  third_follow_up_date,
                  sep='~'
            )
            new_lead=Lead(
                  name=name,
                  phone_number=phone,
                  date=date,
                  source_of_lead=source_of_lead,
                  counsellor=request.user,
                  mode=mode,
                  status=status,
                  joining_centre=joining_center,
                  course=course,
                  education_background=education,
                  main=stream,
                  cs_background=cs_background,
                  employed=employed,
                  joining_month=joining_month,
                  additional_notes=additional_notes,
                  initial_response=initial_response,
                  first_follow_up=first_follow_up,
                  first_follow_up_date=first_follow_up_date,
                  second_follow_up=second_follow_up,
                  second_follow_up_date=second_follow_up_date,
                  third_follow_up=third_follow_up,
                  third_follow_up_date=third_follow_up_date
            )
            new_lead.save()
            print('lead added')
            return render(request,'user/add_lead.html')
      else:
            counsellors = Counsellor.objects.all()
            context={'counsellors':counsellors}
            return render(request,'user/add_lead.html',context)
      
def edit_lead(request,i):
      global lead
      lead=Lead.objects.get(id=i)
      context={'lead':lead}
      return render(request,'user/edit_lead.html',context)

def save_edited(request):
      name=request.POST['name']
      phone=request.POST['phone']
      date=request.POST['date']
      source_of_lead=request.POST['source']
      mode=request.POST['mode']
      status=request.POST['status']
      joining_center=request.POST['joining_center']
      course=request.POST['course']
      education=request.POST['education']
      stream=request.POST['stream']
      cs_background=request.POST['cs_background']
      if cs_background=='yes':
            cs_background=True
      else:
            cs_background=False
      employed=request.POST['employed']
      if employed=='yes':
            employed=True
      else:
            employed=False
      joining_month=request.POST['joining_month']
      additional_notes=request.POST['additional_notes']
      initial_response=request.POST['initial_response']
      first_follow_up=request.POST['first_follow_up']
      first_follow_up_date=request.POST['first_follow_up_date']
      second_follow_up=request.POST['second_follow_up']
      second_follow_up_date=request.POST['second_follow_up_date']
      third_follow_up=request.POST['third_follow_up']
      third_follow_up_date=request.POST['third_follow_up_date']
      lead.name=name
      lead.phone_number=phone
      if date:
            lead.date=date
      lead.source_of_lead=source_of_lead
      lead.mode=mode
      lead.status=status
      lead.joining_centre=joining_center
      lead.course=course
      lead.education_background=education
      lead.main=stream
      lead.cs_background=cs_background
      lead.employed=employed
      lead.joining_month=joining_month
      lead.additional_notes=additional_notes
      lead.initial_response=initial_response
      lead.first_follow_up=first_follow_up
      if first_follow_up_date:
            lead.first_follow_up_date=first_follow_up_date
      lead.second_follow_up=second_follow_up
      if second_follow_up_date:
            lead.second_follow_up_date=second_follow_up_date
      lead.third_follow_up=third_follow_up
      if third_follow_up_date:
            lead.third_follow_up_date=third_follow_up_date
      lead.last_modified=timezone.now()
      lead.save()
      print('edited')
      return redirect('leads')
      
def user_report(request,i):
      user=User.objects.get(id=i)
      leads=Lead.objects.filter(counsellor=user)
      warm_count=Lead.objects.filter(Q(counsellor=user) & Q(status='warm')).count()
      cold_count=Lead.objects.filter(Q(counsellor=user) & Q(status='cold')).count()
      confirmed_count=Lead.objects.filter(Q(counsellor=user) & Q(status='batch confirmed')).count()
      not_intrested_count=Lead.objects.filter(Q(counsellor=user) & Q(status='not intrested')).count()
      registration_fee_paid_count=Lead.objects.filter(Q(counsellor=user) & Q(status='registration fee paid')).count()
      demo_requested_count=Lead.objects.filter(Q(counsellor=user) & Q(status='demo requested')).count()
      demo_provided_count=Lead.objects.filter(Q(counsellor=user) & Q(status='demo provided')).count()

      january = Lead.objects.filter(Q(counsellor=user) & Q(status='batch confirmed') & Q(joining_month='2024-01')).count()
      february = Lead.objects.filter(Q(counsellor=user) & Q(status='batch confirmed') & Q(joining_month='2024-02')).count()
      march = Lead.objects.filter(Q(counsellor=user) & Q(status='batch confirmed') & Q(joining_month='2024-03')).count()
      april = Lead.objects.filter(Q(counsellor=user) & Q(status='batch confirmed') & Q(joining_month='2024-04')).count()
      may = Lead.objects.filter(Q(counsellor=user) & Q(status='batch confirmed') & Q(joining_month='2024-05')).count()
      june = Lead.objects.filter(Q(counsellor=user) & Q(status='batch confirmed') & Q(joining_month='2024-06')).count()
      july = Lead.objects.filter(Q(counsellor=user) & Q(status='batch confirmed') & Q(joining_month='2024-07')).count()
      august = Lead.objects.filter(Q(counsellor=user) & Q(status='batch confirmed') & Q(joining_month='2024-08')).count()
      september = Lead.objects.filter(Q(counsellor=user) & Q(status='batch confirmed') & Q(joining_month='2024-09')).count()
      october = Lead.objects.filter(Q(counsellor=user) & Q(status='batch confirmed') & Q(joining_month='2024-10')).count()
      november = Lead.objects.filter(Q(counsellor=user) & Q(status='batch confirmed') & Q(joining_month='2024-11')).count()
      december = Lead.objects.filter(Q(counsellor=user) & Q(status='batch confirmed') & Q(joining_month='2024-12')).count()

      context={
            'user':user,'leads':leads,'warm':warm_count,'cold':cold_count,'confirmed':confirmed_count,'not_intrested':not_intrested_count,'registration_fee_paid':registration_fee_paid_count,'demo_requested':demo_requested_count,'demo_provided':demo_provided_count,
            'january':january,'february':february,'march':march,'april':april,'may':may,'june':june,'july':july,'august':august,
            'september':september,'october':october,'november':november,'december':december
            }
      return render(request,'admin/user_report.html',context)

def course_wise_report(request):
     data_science=Lead.objects.filter(Q(status='batch confirmed') & Q(course='data science')).count()
     data_analytics=Lead.objects.filter(Q(status='batch confirmed') & Q(course='data analytics')).count()
     business_analytics=Lead.objects.filter(Q(status='batch confirmed') & Q(course='business analytics')).count()
     python_fullstack =Lead.objects.filter(Q(status='batch confirmed') & Q(course='python fullstack')).count()
     software_testing=Lead.objects.filter(Q(status='batch confirmed') & Q(course='software testing')).count()
     MERN_stack=Lead.objects.filter(Q(status='batch confirmed') & Q(course='MERN stack')).count()
     context1={'ds':data_science,'da':data_analytics,'ba':business_analytics,'pf':python_fullstack,'st':software_testing,'ms':MERN_stack}
     return render(request,'admin/course_wise_report.html',context)

# def delete_lead(request,i):
#       lead=Lead.objects.get(id=i)
#       lead.delete()
#       return redirect('leads')

@csrf_exempt
def delete_lead(request, i):
    if request.method == 'POST':
        lead = get_object_or_404(Lead, id=i)
        lead.delete()
        return JsonResponse({'status': 'success', 'message': 'Lead deleted successfully'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

def change_password(request):
      if request.method == 'POST':
            old_password = request.POST.get('old_password')
            new_password1 = request.POST.get('new_password1')
            new_password2 = request.POST.get('new_password2')

            user = authenticate(username=request.user.username, password=old_password)
            if user is not None:
                  if new_password1 == new_password2:
                        user.set_password(new_password1)
                        user.save()
                        login(request, user)
                        return redirect('user_logout')
      else:
            return render(request, 'change_password.html')
      
# def suspend_user(request,i):
#       counsellor=Counsellor.objects.get(id=i)
#       counsellor.status = False
#       counsellor.save()
#       return redirect('admin_home')

# @csrf_exempt
# def suspend_user(request, i):
#     if request.method == 'POST':
#         counsellor = get_object_or_404(Counsellor, id=i)
#         counsellor.status = False
#         counsellor.save()
#         return JsonResponse({'status': 'success', 'message': 'Account suspended successfully'})
#     return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

def suspend_user(request,i):
      counsellor=Counsellor.objects.get(id=i)
      counsellor.status = False
      counsellor.save()
      return redirect('users_page')


def activate_user(request,i):
      counsellor=Counsellor.objects.get(id=i)
      counsellor.status = True
      counsellor.save()
      return redirect('users_page')

def users_page(request):
      superusers = User.objects.filter(is_superuser=True).order_by('-last_login')
      users = Counsellor.objects.all() 
      logins = login_details.objects.all()
      context={'users':users,'superusers':superusers,'login_details':logins}
      return render(request,'admin/users.html',context)

def lead_profile(request,i):
      lead=Lead.objects.get(id=i)
      context={'lead':lead}
      return render(request,'user/lead_profile.html',context)