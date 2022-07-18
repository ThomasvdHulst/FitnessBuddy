from email import message
from django.shortcuts import render, redirect
from .forms import RegistrationForm, ProfileForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout, authenticate
from .models import Exercise, UserProfile, Workout
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
@login_required(login_url="/login")
def home(request):
    return render(request, 'main/home.html', {})

def sign_up(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = request.POST.get("email")
            user = form.save()
            login(request, user)
            send_mail(
                subject='Account Created!',
                message='Hello, thank you for creating an account with us!',
                from_email= settings.EMAIL_HOST_USER,
                recipient_list=[email],
            )
            messages.success(request, ('Account created, welcome ' + user.username + '!' ))
            return redirect('/home')
    else:
        form = RegistrationForm()

    return render(request, 'registration/sign_up.html', {"form":form})

@login_required(login_url="/login")
def profile(request):
    userProfile = UserProfile.objects.all()
    for user in userProfile:
        if user.userWithProfile == request.user:
            profile = user
            return render(request, 'main/profile.html', {"profile":profile})

    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            profileUser = form.save(commit=False)
            profileUser.userWithProfile = request.user
            profileUser.save()
            messages.success(request, ('Profile completed, hello ' + profileUser.fullName + '!'))
            return redirect('profile')
    else:
        form = ProfileForm()
    return render(request, 'main/profile.html', {"form":form})

@login_required(login_url="/login")
def exercises(request):
    exercises = Exercise.objects.all()
    return render(request, 'main/exercises.html', {"exercises":exercises})

@login_required(login_url="/login")
def search_exercises(request):
    if request.method == "POST":
        searched = request.POST['searched']
        exercises = Exercise.objects.filter(name__contains=searched)
        if searched != '':
            return render(request, 'main/search_exercises.html', {"searched":searched, "exercises":exercises})
        else: return redirect('/exercises')
    else: 
        return redirect('/exercises')

@login_required(login_url="/login")
def startworkout(request):
    if request.method == 'POST':
        startworkout = request.POST.get("startworkout")
        if startworkout:
            workout = Workout(user=request.user)
            workout.save()
            return redirect('/workout')
    return render(request, 'main/startworkout.html', {})

@login_required(login_url="/login")
def workout(request):
    currentworkout = Workout.objects.last()
    exercises = Exercise.objects.all()
    if request.method == 'POST':
        addexercise = request.POST.get("addexercise")
        cancelworkout = request.POST.get("cancelworkout")
        workoutname = request.POST.get("saveworkoutname")
        exercise_id = request.POST.get("exercise-id")
        if workoutname:
            currentworkout.nameWorkout = request.POST.get("workoutname")
            currentworkout.save()

        if exercise_id:
            exerciseChosen = Exercise.objects.filter(id=exercise_id).first()
            currentworkout.exercises.add(exerciseChosen)
            currentExercises = currentworkout.exercises.all()
            return render(request, 'main/workout.html', {"currentworkout":currentworkout, "exercises":exercises, "currentExercises":currentExercises})
        if cancelworkout:
            currentworkout.delete()
            return redirect('startworkout')
    return render(request, 'main/workout.html', {"currentworkout":currentworkout, "exercises":exercises})