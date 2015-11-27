from django.apps import apps
from apps.sa.models import AppDataLastUpdate


def vars(request):

    path_items = request.path.split('/')
    app_label = path_items[1]
    page_label = path_items[2] if len(path_items)>2 else ''
    item_label = path_items[3] if len(path_items)>3 else ''

    if app_label[-3:] == '-sa':
        app_label = app_label[:-3]
        sa_flag = True
    else:
        sa_flag = False

    appslist = []
    for app in apps.get_app_configs():
        if app.name[:5] == 'apps.':
            appslist.append(app)

    try:
        app = apps.get_app_config(app_label)
        if app in appslist:
            if sa_flag:
                sa_app = apps.get_app_config('sa')
                if app_label == 'sa':
                    app_pages = sa_app.pages
                else:
                    app_pages = sa_app.admin_pages
            else:
                if app_label == 'sa':
                    app_pages = []
                else:
                    app_pages = app.pages
        else:
            app_pages = []
    except LookupError:
        app = None
        app_pages = []

    try:
        last_update = AppDataLastUpdate.objects.get(appname=app_label).datetime
    except:
        last_update = None

    return {
        'sa': sa_flag,
        'app_label': app_label,
        'page_label': page_label,
        'item_label': item_label,
        'appslist': appslist,
        'app': app,
        'app_pages': app_pages,
        'last_update': last_update,
    }

