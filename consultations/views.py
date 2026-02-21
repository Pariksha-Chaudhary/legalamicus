from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
import razorpay

from lawyers.models import Lawyer
from .models import Consultation

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum


from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
import razorpay
import logging

logger = logging.getLogger(__name__)


@login_required
@login_required
def book_lawyer(request, lawyer_id):
    lawyer = get_object_or_404(Lawyer, id=lawyer_id)

    # If FREE → WhatsApp
    if not lawyer.fee or lawyer.fee == Decimal("0.00"):
        whatsapp_url = f"https://wa.me/{lawyer.whatsapp_number}"
        return redirect(whatsapp_url)

    # 🔥 DELETE OLD UNPAID CONSULTATIONS (IMPORTANT)
    Consultation.objects.filter(
        lawyer=lawyer,
        client=request.user,
        is_paid=False
    ).delete()

    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

    order = client.order.create({
        "amount": int(lawyer.fee * 100),
        "currency": "INR",
        "payment_capture": 1
    })

    Consultation.objects.create(
        lawyer=lawyer,
        client=request.user,
        amount=lawyer.fee,
        razorpay_order_id=order["id"]
    )

    return render(request, "payment.html", {
        "lawyer": lawyer,
        "order_id": order["id"],
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "amount": lawyer.fee
    })

@login_required
def payment_success(request, lawyer_id):

    razorpay_payment_id = request.GET.get("payment_id")
    razorpay_order_id = request.GET.get("order_id")
    razorpay_signature = request.GET.get("signature")

    consultation = Consultation.objects.filter(
        razorpay_order_id=razorpay_order_id,
        client=request.user
    ).first()

    if not consultation:
        return redirect("/")

    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

    try:
        client.utility.verify_payment_signature({
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        })

        consultation.is_paid = True
        consultation.razorpay_payment_id = razorpay_payment_id
        consultation.razorpay_signature = razorpay_signature
        consultation.save()

    except:
        return redirect("/")

    lawyer = get_object_or_404(Lawyer, id=lawyer_id)

    whatsapp_url = f"https://wa.me/{lawyer.whatsapp_number}?text=Hello, I have completed payment."

    return redirect(whatsapp_url)


@login_required
def my_consultations(request):
    consultations = Consultation.objects.filter(
        client=request.user
    ).order_by("-created_at")

    return render(request, "consultations/my_consultations.html", {
        "consultations": consultations
    })


    
@staff_member_required
def admin_revenue(request):

    paid_consultations = Consultation.objects.filter(is_paid=True)

    total_revenue = paid_consultations.aggregate(
        Sum("amount")
    )["amount__sum"] or 0

    total_consultations = paid_consultations.count()

    return render(request, "admin/revenue.html", {
        "total_revenue": total_revenue,
        "total_consultations": total_consultations
    })