from .models import Lawyer

def user_role(request):
    if request.user.is_authenticated:
        is_lawyer = Lawyer.objects.filter(user=request.user).exists()
        return {
            "is_lawyer": is_lawyer
        }
    return {
        "is_lawyer": False
    }
