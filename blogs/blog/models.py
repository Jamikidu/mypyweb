from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100)    #블로그제목
    content = models.TextField()                #내용
    pub_date = models.DateTimeField()           #작성일
    modify_date = models.DateTimeField(null=True, blank=True)   #입력 폼이 비어도 됨 - 수정일
    photo = models.ImageField(upload_to='blog/images/%Y/%m/%d/',
                              null=True, blank=True)    #null 허용, 파일을 첨부하지 않을때도 OK

    def __str__(self):
        return self.title