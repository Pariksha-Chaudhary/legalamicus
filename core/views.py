from django.shortcuts import render
from django.http import Http404

def home(request):
    return render(request, 'core/home.html')

def about(request):
    return render(request, 'about.html')

def practice_areas(request):
    return render(request, 'practice_areas.html')
def consultation(request):
    return render(request, 'consultation.html')


from django.shortcuts import render
from django.http import Http404

def practice_detail(request, area_slug):
    practice_data = {
        "criminal-law": {
            "title": "Criminal Law",
            "description": "Criminal law deals with offences against individuals and the state. Our firm provides strategic defense, bail assistance, and strong courtroom representation across all criminal matters.",
            "acts": [
                "Indian Penal Code, 1860 (IPC)",
                "Code of Criminal Procedure, 1973 (CrPC)",
                "Indian Evidence Act, 1872",
                "Information Technology Act, 2000",
                "Negotiable Instruments Act, 1881 (Section 138)"
            ],
            "services": [
                "Bail (Regular & Anticipatory)",
                "FIR Quashing",
                "Cheque Bounce (NI Act 138)",
                "Cyber Crime Cases",
                "Fraud & Cheating",
                "Domestic Violence Defense",
                "Trial Representation"
            ]
        },
        # Add similar data for other practice areas...
    }

    data = practice_data.get(area_slug)

    if not data:
        return render(request, "404.html")

    return render(request, "practice_detail.html", {"data": data})

def sub_practice_detail(request, area_slug, sub_slug):
    # Add sub-areas here, similar to the practice_detail view, to handle sub-practice functionality
    # Example sub-area data:
    practice_data = {
        "criminal-law": {
            "subs": {
                "bail": {
                    "title": "Bail (Regular & Anticipatory)",
                    "description": "We assist clients in securing regular and anticipatory bail under Indian criminal law.",
                    "acts": [
                        "Code of Criminal Procedure, 1973 (Sections 437, 438, 439)"
                    ]
                }
            }
        }
    }

    area = practice_data.get(area_slug)

    if not area:
        raise Http404("Practice area not found")

    sub = area["subs"].get(sub_slug)

    if not sub:
        raise Http404("Sub practice not found")

    context = {
        "area": area_slug,
        "sub": sub
    }

    return render(request, "sub_practice_detail.html", context)
def appointment(request):
    return render(request, 'appointment.html')

def blog(request):
    return render(request,'blog.html')
def casestudy(request):
    return render(request,'casestudy.html')

def faq(request):
    return render(request,'faq.html')
def term_conditions(request):
    return render(request,'term_conditions.html')