def is_author(user,blog):
    return user== blog.user

def get_client_ip(request):
    """Lấy địa chỉ IP của người dùng"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # Lấy IP đầu tiên nếu đi qua proxy
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip