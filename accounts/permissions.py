from accounts.models import StaffRole, UserProfile


def get_user_profile(user) -> UserProfile | None:
    if not user.is_authenticated:
        return None
    return UserProfile.objects.filter(user=user).first()


def user_is_director(user) -> bool:
    """Директор: финансы, отчёты, Django admin."""
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    profile = get_user_profile(user)
    return profile is not None and profile.role == StaffRole.DIRECTOR


def user_can_view_finance(user) -> bool:
    """Сводки, отчёты, графики доходов, экспорт."""
    return user_is_director(user)


def user_role_label(user) -> str:
    if not user.is_authenticated:
        return ''
    if user.is_superuser:
        return 'Директор'
    profile = get_user_profile(user)
    if profile:
        return profile.get_role_display()
    return 'Сотрудник'
