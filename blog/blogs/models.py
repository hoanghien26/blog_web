from django.db import models
from users.models import CustomUser
# Create your models here.

# model danh mục
class List(models.Model):
    List_name=models.CharField(max_length=500)

    def __str__(self):
        return f"{self.List_name}"

# model thể loại
class Category(models.Model):
    name=models.CharField(max_length=500)
    list=models.ForeignKey(List,on_delete=models.CASCADE,related_name="categogies")
    
    def __str__(self):
        return f"{self.name}"


# model blog
class Blog(models.Model):
    author=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    title=models.CharField(max_length=5000)
    description=models.TextField()
    content=models.TextField()
    created_at=models.DateTimeField(  auto_now_add=True)
    number_of_view=models.IntegerField(default=0)
    category=models.ManyToManyField(Category,related_name="blogs")

    class Meta:
        ordering=['-created_at']
        permissions=[
            ("can_edit_delete","can edit and delete for blog")
        ]

    def __str__(self):
        return f"{self.title}:{self.author.username}"

class BlogViewBlog(models.Model):
    blog= models.ForeignKey(Blog, on_delete=models.CASCADE)
    ip_address=models.GenericIPAddressField()
    viewed_at= models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('blog', 'ip_address')

class Comment(models.Model):
    content=models.TextField()
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    blog=models.ForeignKey(Blog,on_delete=models.CASCADE)
    created_at=models.DateTimeField(  auto_now_add=True)

    class Meta:
        # Sắp xếp bình luận theo thời gian mới nhất lên đầu
        ordering = ['-created_at'] 
        verbose_name = "Bình luận"
        verbose_name_plural = "Các bình luận"   

    def __str__(self):
        return f"Bình luận của {self.user.username} về '{self.blog.title}': {self.context[:50]}..."


    
    