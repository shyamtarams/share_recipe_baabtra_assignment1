from django.db import models


class Login(models.Model):
    username=models.CharField(max_length=150)
    password=models.CharField(max_length=200)
    user_image=models.ImageField(upload_to='user_image/')
    def __str__(self):
        return '{} {} {}'.format(self.username, self.password,self.user_image)

class Signup(models.Model):
    username=models.CharField(max_length=150, unique=True)
    # gender=models.CharField(max_length=10)
    email=models.CharField(max_length=254)
    # phone=models.BigIntegerField()
    password=models.CharField(max_length=200)
    user_image=models.ImageField(upload_to='user_image/')
    login=models.ForeignKey(Login,on_delete=models.CASCADE)
    def __str__(self):
        return '{} {} {}'.format(self.username, self.email, self.password)


class Category(models.Model):
    name=models.CharField(max_length=50)
    description=models.TextField()
    # category_image_image=models.ImageField(upload_to='category_img')
    def __str__(self):
        return '{} '.format(self.name)



class Post(models.Model):
    name=models.CharField(max_length=50)
    description=models.TextField()
    post_image=models.ImageField(upload_to='post_img/')
    date=models.DateTimeField(auto_now_add=True)
    category=models.CharField(max_length=100)
    login=models.ForeignKey(Login,on_delete=models.CASCADE)
    # category=models.ForeignKey(Category,on_delete=models.CASCADE)
    # author=models.ForeignKey(Signup,null=False)
    def __str__(self):
        return '{} {} {} {}'.format(self.name, self.description,self.login,self.category)

# class Interaction(models.Model):
#     likes=models.IntegerField(null=True)
#     comment=models.TextField(null=True)
#     date=models.DateTimeField(auto_now_add=True)
#     user=models.ForeignKey(Login,on_delete=models.CASCADE)
#     post=models.ForeignKey(Post,on_delete=models.CASCADE)
#     def __str__(self):
#         return '{} {} {} {} {}'.format(self.likes, self.comment,self.date,self.user,self.post)

class Postlike(models.Model):
    likes=models.IntegerField(null=True)
    date=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(Login,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    def __str__(self):
        return '{} {} {} {}'.format(self.likes,self.date,self.user,self.post)

class Postcomment(models.Model):
    comment=models.TextField(null=True)
    date=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(Login,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    def __str__(self):
        return '{} {} {} {}'.format(self.comment,self.date,self.user,self.post)





