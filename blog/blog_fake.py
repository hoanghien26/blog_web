import os
import django
import random
from faker import Faker

# Khởi động Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')  # Sửa lại đúng tên project của bạn
django.setup()

from blogs.models import Blog, Category, List
from users.models import CustomUser

fake = Faker("vi_VN")


def fake_users(n=10):
    print(f"⏳ Đang tạo {n} người dùng...")
    for _ in range(n):
        username = fake.user_name()
        email = fake.email()
        password = fake.password()
        CustomUser.objects.create_user(username=username, email=email, password=password)
    print(f"✅ Tạo {n} user thành công!\n")


def fake_categories(n=10):
    print(f"⏳ Đang tạo {n} category...")
    try:
        list_instance = List.objects.get(pk=1)
    except List.DoesNotExist:
        list_instance = List.objects.create(name="Danh sách mặc định")

    for _ in range(n):
        name = fake.sentence(nb_words=5)
        Category.objects.create(name=name, list=list_instance)
    print(f"✅ Tạo {n} category thành công!\n")


def fake_blogs(n=20):
    print(f"⏳ Đang tạo {n} blog...")
    users = list(CustomUser.objects.all())
    categories = list(Category.objects.all())

    if not users or not categories:
        print("❌ Lỗi: Cần có user và category trước khi tạo blog.")
        return

    for _ in range(n):
        author = random.choice(users)
        title = fake.sentence(nb_words=6)
        description = fake.text(max_nb_chars=200)
        content = "\n\n".join([fake.paragraph(nb_sentences=5) for _ in range(5)])
        created_at = fake.date_between(start_date="-2y", end_date="today")

        blog = Blog.objects.create(
            author=author,
            title=title,
            description=description,
            content=content,
            created_at=created_at,
            number_of_view=random.randint(0, 1000),
        )

        selected_categories = random.sample(categories, k=min(2, len(categories)))
        blog.category.set(selected_categories)

    print(f"✅ Tạo {n} blog thành công!\n")


if __name__ == '__main__':
    fake_users(10)
    fake_categories(10)
    fake_blogs(20)
