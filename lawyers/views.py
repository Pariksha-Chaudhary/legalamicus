from django.shortcuts import render, get_object_or_404, redirect
from .models import Lawyer, State, City, LegalCategory, SubCategory, LawyerCategory
from django.db.models import Q
from django.http import JsonResponse



def lawyer_list(request):
    lawyers = Lawyer.objects.filter(is_active=True).prefetch_related(
        'lawyercategory_set__category'
    )

    state = request.GET.get('state')
    city = request.GET.get('city')
    category = request.GET.get('category')
    sub_category = request.GET.get('sub_category')
    experience = request.GET.get('experience')

    if state:
        lawyers = lawyers.filter(state_id=state)

    if city:
        lawyers = lawyers.filter(city_id=city)

    if category:
        lawyers = lawyers.filter(lawyercategory__category_id=category)

    if sub_category:
        lawyers = lawyers.filter(lawyercategory__sub_category_id=sub_category)

    if experience:
        lawyers = lawyers.filter(experience__gte=experience)

    lawyers = lawyers.distinct()

    # ✅ ADD THIS BLOCK (VERY IMPORTANT)
    for lawyer in lawyers:
        categories = lawyer.lawyercategory_set.all()

        paid_categories = categories.filter(is_free_consultation=False)
        free_categories = categories.filter(is_free_consultation=True)

        lawyer.has_paid = paid_categories.exists()
        lawyer.first_paid = paid_categories.first()
        lawyer.first_free = free_categories.first()

    # FILTERED cities based on state
    if state:
        cities = City.objects.filter(state_id=state)
    else:
        cities = City.objects.all()

    context = {
        'lawyers': lawyers,
        'states': State.objects.all(),
        'cities': cities,
        'categories': LegalCategory.objects.all(),
        'sub_categories': SubCategory.objects.all(),
        'selected_state': state,
        'selected_city': city,
        'selected_category': category,
        'selected_sub_category': sub_category,
        'selected_experience': experience,
    }

    return render(request, 'lawyers/lawyer_list.html', context)

def book_consultation(request, lawyer_id, category_id):
    lawyer = get_object_or_404(Lawyer, id=lawyer_id)

    lawyer_category = get_object_or_404(
        LawyerCategory,
        lawyer=lawyer,
        category_id=category_id
    )

    # If FREE → Direct WhatsApp
    if lawyer_category.is_free_consultation:
        whatsapp_url = f"https://wa.me/{lawyer.whatsapp_number}"
        return redirect(whatsapp_url)

    # If Paid → redirect to payment page
    return redirect('payment_page', lawyer_id=lawyer.id, category_id=category_id)


def payment_page(request, lawyer_id, category_id):
    return HttpResponse("Payment Page Working")

def load_cities(request):
    state_id = request.GET.get('state_id')
    cities = City.objects.filter(state_id=state_id).values('id', 'name')
    return JsonResponse(list(cities), safe=False)


def load_subcategories(request):
    category_id = request.GET.get('category_id')
    subs = SubCategory.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse(list(subs), safe=False)