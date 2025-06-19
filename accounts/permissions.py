from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'admin')

class IsResearcher(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and (request.user.role == 'researcher' or request.user.role == 'admin'))

class IsViewer(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'viewer')

class ViewerCanUploadAndViewResponse(BasePermission):
    """
    Allow Viewer to upload photo (POST) and view response (GET),
    but restrict other methods.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.role == 'admin':
            return True  # Admins have full access
        if request.user.role == 'viewer':
            return request.method in ['GET', 'POST']
        if request.user.role == 'researcher':
            # Researchers get GET access (for graphics) plus viewer permissions
            return request.method in ['GET', 'POST']
        return False
