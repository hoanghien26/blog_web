from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAuthorOrAdminCanEditAndDelete(BasePermission):

    def has_object_permission(self, request, view, blog):
        if request.method in SAFE_METHODS:
            return True
        return blog.author == request.user or request.user.is_staff
    
class IsUserCreateComment(BasePermission):
    def has_object_permission(self, request, view, comment):
        if request.method in SAFE_METHODS:
            return True
        return comment.user == request.user or request.user.is_staff