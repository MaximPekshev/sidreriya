from authapp.models import Buyer 
def buyer(request):
    buyer = None
    if request.user.is_authenticated: 
        buyer = Buyer.objects.filter(user=request.user).first()
    return {
        'buyer': buyer
    }