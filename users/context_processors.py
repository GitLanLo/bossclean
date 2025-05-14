from places.views import menu

def get_main_menu(request):
    return {'mainmenu': menu}