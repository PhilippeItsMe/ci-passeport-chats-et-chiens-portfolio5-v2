from django.contrib.auth.models import Group
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import PetBusiness, Comment, Like
from .forms import CommentForm, UserRegistrationForm
from .forms import CustomSignupForm, PetBusinessForm
from pet_businesses.utils import group_required
from django.core.exceptions import PermissionDenied


def custom_signup(request):
    """
    Custom signup view combining user registration and group assignment.
    """
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        group_form = CustomSignupForm(request.POST)

        if user_form.is_valid() and group_form.is_valid():
            user = user_form.save(commit=False)
            user.email = user_form.cleaned_data['email']
            user.save()
            group_name = group_form.cleaned_data['group']
            try:
                group = Group.objects.get(name=group_name)
                user.groups.add(group)
                messages.success(request, "Votre compte a été créé.")
                return redirect('login')
            except Group.DoesNotExist:
                messages.error(request,
                               f"Le groupe '{group_name}' n'existe pas.")
        else:
            messages.error(request,
                           "Il y a eu une erreur avec votre inscription.")
    else:
        user_form = UserRegistrationForm()
        group_form = CustomSignupForm()

    return render(request, 'registration/signup.html', {
        'user_form': user_form,
        'group_form': group_form,
    })


class BusinessList(generic.ListView):
    """
    View to render businesses list.
    """
    queryset = PetBusiness.objects.filter(approved=True)
    template_name = "pet_businesses/pet_business_list.html"
    context_object_name = "pet_business_list"
    paginate_by = 3


def pet_business_detail(request, slug):
    """
    View to render business details and create comments.
    """
    post = get_object_or_404(PetBusiness.objects.filter(approved=True),
                             slug=slug)
    comments = post.comments.all().order_by("-date_created")
    comment_count = post.comments.filter(approved=True).count()

    likes_count = post.likes.count()
    has_liked = post.likes.filter(
        author=request.user
        ).exists() if request.user.is_authenticated else False

    if request.method == "POST":
        if not request.user.groups.filter(name="Pet Owners").exists():
            raise PermissionDenied("Vous n'avez pas la permission de faire des commentaires.")
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.pet_businesse = post
            comment.save()
            messages.success(
                request, "Commentaire soumis en attente d'approbation."
            )
            return HttpResponseRedirect(reverse('pet_business_detail',
                                                args=[slug]))
        else:
            messages.error(request, "Il y a eu une erreur.")
    else:
        comment_form = CommentForm()

    return render(
        request,
        "pet_businesses/pet_business_detail.html",
        {
            "pet_business_detail": post,
            "comment_form": comment_form,
            "comments": comments,
            "comment_count": comment_count,
            "likes_count": likes_count,
            "has_liked": has_liked,
        },
    )


@group_required("Pet Owners")
def comment_edit(request, slug, comment_id):
    """
    View to edit comments.
    """
    if request.method == "POST":

        queryset = PetBusiness.objects.filter(approved=True)
        post = get_object_or_404(queryset, slug=slug)
        comment = get_object_or_404(Comment, pk=comment_id)
        comment_form = CommentForm(data=request.POST, instance=comment)

        if comment_form.is_valid() and comment.author == request.user:
            comment = comment_form.save(commit=False)
            comment.pet_business = post
            comment.approved = False
            comment.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Commentaire mis à jour.')
        else:
            messages.add_message(request,
                                 messages.ERROR,
                                 'Il y a eu une erreur.')

    return HttpResponseRedirect(reverse('pet_business_detail', args=[slug]))


@group_required("Pet Owners")
def comment_delete(request, slug, comment_id):
    """
    View to delete comment.
    """
    queryset = PetBusiness.objects.filter(approved=True)
    post = get_object_or_404(queryset, slug=slug)
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.author == request.user:
        comment.delete()
        messages.add_message(request, messages.SUCCESS,
                             'Commentaire effacé!')
    else:
        messages.add_message(request, messages.ERROR,
                             'Vous ne pouvez effacer que vos commentaires!')

    return HttpResponseRedirect(reverse('pet_business_detail', args=[slug]))


@group_required("Pet Owners")
def like_post(request, pet_business_id):
    pet_business = get_object_or_404(PetBusiness, id=pet_business_id)
    like, created = Like.objects.get_or_create(pet_business=pet_business,
                                               author=request.user)
    if not created:
        like.delete()
    return redirect('pet_business_detail', slug=pet_business.slug)


@group_required("Business Owners")
def pet_business_form(request):

    """
    View to list pet businesses created
    by the logged-in user and create new one.
    """
    pet_businesses = PetBusiness.objects.filter(
        author=request.user, approved=True)

    if request.method == "POST":
        form = PetBusinessForm(request.POST)

        if form.is_valid():
            pet_business = form.save(commit=False)
            pet_business.author = request.user
            pet_business.save()
            form.save_m2m()
            messages.success(request,
                             "Entreprise soumise en attente d'approbation.")
            return redirect('pet_business_form')
        else:
            messages.error(request, "Il y a eu une erreur.")
    else:
        form = PetBusinessForm()

    return render(request, 'pet_businesses/pet_business_form.html', {
        'pet_businesses': pet_businesses, 'form': form,
    })


@group_required("Business Owners")
def pet_business_edit(request, slug, pet_business_id):
    """
    View to edit pet businesses created by the logged-in user.
    """
    pet_business = get_object_or_404(
        PetBusiness,
        id=pet_business_id, slug=slug, author=request.user)

    if request.method == "POST":
        form = PetBusinessForm(data=request.POST, instance=pet_business)

        if form.is_valid():
            pet_business = form.save(commit=False)
            pet_business.author = request.user
            pet_business.save()
            form.save_m2m()
            messages.success(request, "Mise à jour réussie.")
            return redirect('pet_business_form')
        else:
            messages.error(request, "Il y a eu une erreur.")
    else:
        form = PetBusinessForm(instance=pet_business)

    return render(request, 'pet_businesses/pet_business_form.html', {
        'form': form,
        'pet_businesses': PetBusiness.objects.filter(author=request.user,
                                                     approved=True),
    })


@group_required("Business Owners")
def pet_business_delete(request, slug, pet_business_id):
    """
    View to delete pet businesses created by the logged-in user.
    """
    pet_business = get_object_or_404(PetBusiness, id=pet_business_id,
                                     slug=slug, author=request.user)

    if request.method == "POST":
        pet_business.delete()
        messages.success(request, "Entreprise effacée.")
        return redirect('pet_business_form')
    else:
        messages.error(request, "Il y a eu une erreur.")
    return redirect('pet_business_form')
