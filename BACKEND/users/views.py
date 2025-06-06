from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import logout

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if not username or not password:
            messages.error(request, 'Tous les champs sont obligatoires.')
        else:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenue {user.username} !')
                return redirect('home')  # à adapter selon le nom de ta vue d'accueil
            else:
                messages.error(request, 'Nom d’utilisateur ou mot de passe invalide.')

    return render(request, 'users/login.html')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if not username or not password:
            messages.error(request, 'Tous les champs sont obligatoires.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Ce nom d’utilisateur est déjà pris.')
        else:
            User.objects.create_user(username=username, password=password)
            messages.success(request, 'Compte créé avec succès ! Vous pouvez maintenant vous connecter.')
            return redirect(reverse('login'))

    return render(request, 'users/register.html')

@login_required
def profile_view(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        profile.bio = request.POST.get('bio')

        user.save()
        profile.save()

        messages.success(request, "Profil mis à jour avec succès.")
        return redirect('profile')

    return render(request, 'users/profile.html', {'user': user, 'profile': profile})

from django.contrib.auth import update_session_auth_hash
from .forms import CustomPasswordChangeForm

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # évite de déconnecter l'utilisateur
            messages.success(request, 'Mot de passe modifié avec succès.')
            return redirect('profile')
        else:
            messages.error(request, 'Erreur lors du changement de mot de passe.')
    else:
        form = CustomPasswordChangeForm(user=request.user)
    
    return render(request, 'users/change_password.html', {'form': form})

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, "Votre compte a été supprimé.")
        return redirect('home')
    
def logout_view(request):
    logout(request)
    return redirect('home')