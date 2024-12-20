from goodapp.models import In_Barrels

def cider_in_barrels(request):
	return {
		'in_bar': In_Barrels.objects.all()[:8]
    }