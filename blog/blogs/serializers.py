from rest_framework import serializers
from blogs.models import *
import re
from django.core.exceptions import ValidationError

class SerializerList(serializers.ModelSerializer):
    class Meta:
        model=List
        fields='__all__'

    def validate_List_name(self,value):
        if re.search(r"[^A-Za-z0-9]",value):
            raise ValidationError("Danh mục không chứa ký tự đặc biệt")
        return value
class SerializerCategory(serializers.ModelSerializer):
    list=SerializerList()
    class Meta:
        model=Category
        fields=['name', 'list']

    def validate_List_name(self,value):
        if re.search(r"[^A-Za-z0-9]",value):
            raise ValidationError("Danh mục không chứa ký tự đặc biệt")
        return value
class SerializerBlog(serializers.ModelSerializer):
    category=SerializerCategory(many=True)
    created_at = serializers.DateTimeField(format="%d-%m-%Y", read_only=True)
    
    class Meta:
        model= Blog
        fields=["id","author","title","description","content","created_at","number_of_view","category"]

    def create(self, validated_data):
        categories_data = validated_data.pop('category',[])
        blog = Blog.objects.create(**validated_data)

        for cat_data in categories_data:
           
        # Lấy hoặc tạo Category dựa vào name và list
            category_obj, _ = Category.objects.get_or_create(
                name=cat_data['name'],
                list=cat_data['list']
            )
            blog.category.add(category_obj)  # hàm get_or_create có tác dụng nếu như không tìm thấy đối tượng thì sẽ tạo mới đối tượng

        return blog

    def update(self,instance,validated_data):
        categories_data= validated_data.pop("category",None)


        for atrr, value in validated_data.items():
            setattr(instance,atrr,value)

        instance.save()
        
        if categories_data is not None:
             instance.category.clear()
             for cat_data in categories_data:
           
        # Lấy hoặc tạo Category dựa vào name và list
                category_obj, _ = Category.objects.get_or_create(
                    name=cat_data['name'],
                    list=cat_data['list']
                )
                instance.category.add(category_obj)
        return instance
        
    def to_representation(self, instance):
            rep = super().to_representation(instance)
            rep['category'] = SerializerCategory(instance.category.all(), many=True).data
            return rep
    

class CommentSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d-%m-%Y", read_only=True)
    class Meta:
        model=Comment
        fields="__all__"

    
