from django.shortcuts import render
from rest_framework import status,serializers,generics,permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from blogs.serializers import SerializerBlog,CommentSerializer
from blogs.models import *
from blogs.permissions.blog import *
from rest_framework.pagination import PageNumberPagination
from blogs.utils.permissions import is_author, get_client_ip
from django.shortcuts import get_object_or_404

# Create your views here.

class CustomPagenigation(PageNumberPagination):
    page_size=10
    page_query_param="p"
    page_size_query_param = 'per_page'

class View_blog(generics.ListAPIView):
    serializer_class=SerializerBlog
    permission_classes=[permissions.AllowAny]
    pagination_class=CustomPagenigation

    def get_queryset(self):
        return Blog.objects.all().order_by("-created_at")
    

class viewDetail_edit_delete_blog(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=SerializerBlog
    queryset=Blog.objects.all()
    
    
    def get_permissions(self):
        if self.request.method in ["PUT","PATCH","DELETE"]:
            return [IsAuthorOrAdminCanEditAndDelete()]
        return [permissions.AllowAny()]
    def retrieve(self,request,*args, **kwargs):
        blog=self.get_object()
        ip=get_client_ip(request)

        if not BlogViewBlog.objects.filter(blog=blog,ip_address=ip).exists():
            blog.number_of_view += 1
            blog.save(update_fields=["number_of_view"])
        serializer=self.get_serializer(blog)

        comment=blog.comment_set.all()
        serializerComment=CommentSerializer(comment,many=True)

        return Response({"blog":serializer.data,
                         "comment":serializerComment.data})

class CreateNewBlog(APIView):
    def post(self,request):
        permission_classes = [permissions.IsAuthenticated]
        
        blog=SerializerBlog(data=request.data)
        if blog.is_valid():
            blog.save(author=request.user) # luôn gán để tránh giả mạo
            return Response({"blog":blog.data},status=status.HTTP_201_CREATED)
        return Response(blog.errors,status=status.HTTP_400_BAD_REQUEST)
        

class CreateComment(APIView):
    permissions_classes=[permissions.IsAuthenticated]

    def post(self,request,pk):
        Comment= CommentSerializer(data=request.data)
        if Comment.is_valid():
            Comment.save(author=request.user)
            return Response(Comment.data,status=status.HTTP_201_CREATED)
        return Response(Comment.errors,status=status.HTTP_400_BAD_REQUEST)     
    
class DeleteComment(generics.DestroyAPIView):
    permission_classes=[IsUserCreateComment]
    queryset=Comment.objects.all()

    