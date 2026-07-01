from accounts.permissions import user_can_view_finance, user_role_label


def site_settings(request):
    return {
        'site_name': 'Дарование — CRM',
    }


def navigation(request):
    match = getattr(request, 'resolver_match', None)
    user = getattr(request, 'user', None)
    is_admin = user_can_view_finance(user) if user else False
    return {
        'current_page': match.url_name if match else '',
        'current_namespace': match.namespace if match else '',
        'is_admin': is_admin,
        'user_role_label': user_role_label(user) if user and user.is_authenticated else '',
    }
