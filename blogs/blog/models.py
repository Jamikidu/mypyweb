import os.path

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# 카테고리 모델
class Category(models.Model):
    # unique=True 중복 불허
    name = models.CharField(max_length=50, unique=True)
    # url주소 - 문자, allow_unicode = 한글허용
    slug = models.SlugField(max_length=200, unique=True,
                            allow_unicode=True)

    def __str__(self):
        return self.name

    # 카테고리 url 주소
    def get_absolute_url(self):
        # return f'/blog/category/{self.slug}'  #절대 경로
        # reverse() - redirect와 유사: app-name으로 경로 이동
        return reverse('blog:category_page', args=[self.slug])

    # 관리자 페이지에서 적용
    class Meta:
        ordering = ['name'] # 이름순 정렬
        verbose_name = 'category'
        verbose_name_plural = 'categories'  # 복수일때 categorys 는 맞지 않으니 변경해줌



# 포스트 모델
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)  #글쓴이
    title = models.CharField(max_length=100)    #블로그제목
    content = models.TextField()                #내용
    pub_date = models.DateTimeField()           #작성일
    modify_date = models.DateTimeField(null=True, blank=True)   #입력 폼이 비어도 됨 - 수정일
    photo = models.ImageField(upload_to='blog/images/%Y/%m/%d/',
                              null=True, blank=True)    #null 허용, 파일을 첨부하지 않을때도 OK
    file = models.FileField(upload_to='blog/files/%Y/%m/%d/',
                            null=True, blank=True)
    # 카테고리가 삭제되어도 카테고리가 없는 포스트는 유지
    category = models.ForeignKey(Category, null=True, blank=True,
                                 on_delete=models.SET_NULL)

    def __str__(self):
        return self.title

    # 파일의 이름을 출력하는 메서드
    def get_file_name(self):
        return os.path.basename(self.file.name)

    # 파일의 확장자 구분
    def get_file_ext(self):
        # seoul.csv ->split() -> [seoul, csv]
        return self.get_file_name().split('.')[-1]

