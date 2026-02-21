from .models import PracticeArea

def practice_areas(request):
    return {
        "practice_areas": PracticeArea.objects.prefetch_related("sub_areas").all()
    }
