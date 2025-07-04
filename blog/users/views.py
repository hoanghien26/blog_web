from django.shortcuts import render
from users.serializers import RegisterUserSerializer,UserSerializer,UpdateUserSerializer,PasswordChangeSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,serializers,generics,permissions
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework.exceptions import NotFound

# Create your views here.
User=get_user_model()

class RegisterUser(generics.GenericAPIView):
    serializer_class=RegisterUserSerializer
    permission_classes=[permissions.AllowAny]
    def post(self,request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
       
        user=serializer.save()
        
        refresh=RefreshToken.for_user(user)

        return Response({
            "user":UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        },status=status.HTTP_201_CREATED
        )

class UserPofile(generics.RetrieveUpdateAPIView):
    
    permission_classes=[permissions.IsAuthenticated]
    def get_serializer_class(self):
        if self.request.method=="GET":
            return UserSerializer
        return UpdateUserSerializer
    def get_object(self):
        return self.request.user
    
    # trong RetrieveUpdateAPIView các hàm Retrieve, update,partial_update đã tự xử lý các yêu cầu mà không cần chình sửa, chỉ cần chỉ định get_serializer_class,get_objects, get_queryset
    # tuy nhiên vẫn có thể chỉnh sửa để phù hợp với logic của bản thân
    # def retrieve(self,request, *args, **kwargs):
    #     user=self.get_object()
    #     serializers=self.get_serializer(user)
    #     return Response(serializers.data,status=status.HTTP_200_OK)

    # def update(self,request, *args, **kwargs):
    #     user=self.get_object()
    #     serializers= self.get_serializer(user,data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializers.data,status=status.HTTP_200_OK)
    # def partial_update(self, request, *args, **kwargs):
    #     user=self.get_object()
    #     serializers= self.get_serializer(user,data=request.data,partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializers.data,status=status.HTTP_200_OK)

class PasswordCharged(generics.UpdateAPIView):
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=PasswordChangeSerializer

    def get_object(self):
        return self.request.user
    def update(self, request, *args, **kwargs):
        user=self.get_object()
        serializer=self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            if not user.check_password(serializer.data.get("old_password")):
                return Response({"old_password":"Wrong password"},status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializers.data.get("new_password"))
            user.save()
            # try:   hàm này chỉ vô hiệu hoá một phiên của người dùng
            #     refresh_token=request.data["refresh_token"]
            #     token=RefreshToken(refresh_token)
            #     token.blacklist()

            #     response=Response({"messange":"Logout successful"})
            #     response.delete_cookie("acess_token")
            #     response.delete_cookie("refresh_token")
            #     return respone
            # except Exception as e:
            #     return Response({"error": str(e)}, status=400)
            # khi thay đổi mật khẩu cũng như đăng xuất cần vô hiệu hoá tất cả các phiên


            try:
                # Lấy tất cả các OutstandingToken (Refresh Token chưa bị blacklist) của người dùng này
                outstanding_tokens = OutstandingToken.objects.filter(user=user)
                for token in outstanding_tokens:
                    # Kiểm tra xem token này đã bị blacklist chưa để tránh tạo bản ghi trùng lặp
                    if not hasattr(token, 'blacklistedtoken'):
                        BlacklistedToken.objects.create(token=token)
                # 5. Trả về phản hồi thành công
                # Không cần delete_cookie nếu frontend tự quản lý token trong localStorage.
                # Nếu bạn dùng HttpOnly cookie, thì mới cần response.delete_cookie().
                return Response(
                    {"detail": "Mật khẩu đã được thay đổi thành công. Tất cả các phiên đăng nhập của bạn đã bị vô hiệu hóa. Vui lòng đăng nhập lại."},
                    status=status.HTTP_200_OK
                )

            except Exception as e:
                # Ghi log lỗi nếu quá trình blacklist thất bại (ví dụ: lỗi DB)
                # Tuy nhiên, mật khẩu đã được đổi thành công, nên vẫn trả về thành công cho người dùng
                print(f"Lỗi khi blacklist refresh token cho người dùng {user.username}: {e}")
                return Response(
                    {"detail": "Mật khẩu đã được thay đổi thành công. Tuy nhiên, có lỗi xảy ra khi vô hiệu hóa các phiên cũ. Vui lòng đăng nhập lại."},
                    status=status.HTTP_200_OK # Vẫn là 200 vì mật khẩu đã đổi
                )