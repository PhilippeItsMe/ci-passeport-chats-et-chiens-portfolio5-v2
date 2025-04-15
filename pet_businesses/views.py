from django.contrib.auth.models import Group
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views.generic import ListView
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import PetBusiness, Comment, Like, PetType, ServiceType
from .forms import CommentForm, UserRegistrationForm
from .forms import CustomSignupForm, PetBusinessForm
from pet_businesses.utils import group_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from checkout.models import ActivationCode
from django.utils import timezone
from datetime import timedelta


#------------  Authentificaiton view ------------#

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


#------------  Pet Businesses view ------------#

class BusinessList(ListView):
    """
    View to render businesses list and manage search queries and filters.
    """
    model = PetBusiness
    template_name = "pet_businesses/pet_business_list.html"
    context_object_name = "pet_business_list"
    paginate_by = 3

    def get_queryset(self):
        queryset = PetBusiness.objects.filter(approved=True)

        # Search functionality
        query = self.request.GET.get('q')
        if query:
            if query.strip() == "":
                messages.error(self.request, "Vous n'avez pas entré de recherche.")
            else:
                queryset = queryset.filter(
                    Q(firm__icontains=query) | Q(description__icontains=query)
                )

        # Filtering by Pet Type or Service Type ID
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(
                Q(business_pet_type__id=category_id) | Q(business_service_type__id=category_id)
            ).distinct()

        # Filtering by Canton
        canton = self.request.GET.get('canton')
        if canton:
            queryset = queryset.filter(canton=canton)

        # Filtering by Locality
        locality = self.request.GET.get('locality')
        if locality:
            queryset = queryset.filter(locality__iexact=locality)

        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_canton = self.request.GET.get('canton', '')

        # If canton is selected, filter localities by that canton
        if selected_canton:
                localities = PetBusiness.objects.filter(canton=selected_canton).values_list('locality', flat=True).distinct()
        else:
                localities = PetBusiness.objects.values_list('locality', flat=True).distinct()

        context['search_term'] = self.request.GET.get('q', '')
        context['selected_category'] = self.request.GET.get('category', '')
        context['selected_canton'] = selected_canton
        context['selected_locality'] = self.request.GET.get('locality', '')
        context['pet_types'] = PetType.objects.all()
        context['service_types'] = ServiceType.objects.all()
        context['canton_choices'] = PetBusiness.CANTON_CHOICES
        context['localities'] = sorted(localities)

        return context

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
            raise PermissionDenied(
                "Vous n'avez pas la permission de faire des commentaires.")
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

    has_active_code = False
    if request.user.is_authenticated:
        has_active_code = ActivationCode.objects.filter(
            activated_by=request.user,
            is_active=True,
            activation_date__isnull=False
        ).exclude(
            activation_date__lt=timezone.now() - timedelta(days=365)
        ).exists()

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
            "has_active_code": has_active_code,
        },
        )


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


#------------  Comments views ------------#

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


#------------  Likes views ------------#

@require_POST
@group_required("Pet Owners")
def ajax_like_toggle(request):
    pet_business_id = request.POST.get('pet_business_id')
    pet_business = get_object_or_404(PetBusiness, id=pet_business_id)

    like, created = Like.objects.get_or_create(
        pet_business=pet_business,
        author=request.user
    )

    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({
        'liked': liked,
        'like_count': pet_business.likes.count()
    })
