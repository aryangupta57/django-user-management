from django.http import JsonResponse
from django.views import View
from .forms import CreateUserForm
from .models import User

class UserView(View):
    def post(self, request):
        form = CreateUserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            token = user.generate_jwt_token()
            user.save()
            return JsonResponse({'token': token, 'email': user.email, 'full_name': user.full_name})
        else:
            return JsonResponse({'error': form.errors}, status=400)

    def patch(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[-1]
        payload = User.decode_jwt_token(token)
        if not payload:
            return JsonResponse({'error': 'Invalid token'}, status=400)

        email = payload.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        if request.POST.get('password'):
            user.set_password(request.POST.get('password'))

        if request.POST.get('full_name'):
            user.full_name = request.POST.get('full_name')

        if request.POST.get('bio'):
            user.bio = request.POST.get('bio')

        if request.FILES.get('profile_picture'):
            user.profile_picture = request.FILES.get('profile_picture')

        user.save()
        
        return JsonResponse({'message': 'User updated successfully'})
