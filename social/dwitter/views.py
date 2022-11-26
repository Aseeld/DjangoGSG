from django.shortcuts import render,redirect
from .forms import DweetForm
from .models import Profile,Dweet 
from django.http import HttpResponseRedirect
# def dashboard(request):
#     form = DweetForm()
#     if request.method == 'POST':
#         form = DweetForm(request.POST)
#         if form.is_valid():            
#             dweet=Dweet(body=form.cleaned_data["body"],
#             user=request.user
#             )
#         dweet.save()
#     form = DweetForm()
#     return render(request, "dwitter/dashboard.html", {"form": form})
def dashboard(request):
    form = DweetForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            dweet = form.save(commit=False)
            dweet.user = request.user
            dweet.save()
            return redirect("dwitter:dashboard")
        #return redirect(request.path_info)
        # return HttpResponseRedirect(request.path_info)
    # else:
    #     form = DweetForm()
    return render(request, "dwitter/dashboard.html", {"form": form})

def profile_list(request):
    profiles = Profile.objects.exclude(user=request.user)
    return render(request, "dwitter/profile_list.html", {"profiles": profiles})

def profile(request, pk):
    if not hasattr(request.user, 'profile'):
        missing_profile = Profile(user=request.user)
        missing_profile.save()

    profile = Profile.objects.get(pk=pk)
    if request.method == "POST":
        current_user_profile = request.user.profile
        data = request.POST
        action = data.get("follow")
        if action == "follow":
            current_user_profile.follows.add(profile)
        elif action == "unfollow":
            current_user_profile.follows.remove(profile)
        current_user_profile.save()
    return render(request, "dwitter/profile.html", {"profile": profile})

