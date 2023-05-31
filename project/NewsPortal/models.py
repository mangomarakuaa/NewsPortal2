from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

class Author(models.Model):
    user_author = models.OneToOneField(User, on_delete=models.CASCADE)
    rating_author = models.IntegerField(default=0)

    def update_rating(self):
        rating_post = Post.objects.filter(author_id=self.pk).aggregate(rating_post=Sum('rating_post'))['rating_post']
        rating_comments_author = Comment.objects.filter(user_post_id=self.user_author).aggregate(rating_comment=Sum('rating_comment'))['rating_comment']
        rating_comments_posts = Comment.objects.filter(comment_post__author__user_post=self.user_author).aggregate(rating_comment=Sum('rating'))['rating_comment']
        self.rating_author = rating_post * 3 + rating_comments_author + rating_comments_posts
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    ManyToManyCategory = models.ManyToManyField(Category, through="PostCategory")
    article = 'AR'
    news = 'NE'
    POSITIONS = [
        (article, 'Статья'),
        (news, 'Новость')
    ]

    field_choice = models.CharField(max_length=20, choices=POSITIONS, default=news)
    auto_data = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating_post = models.IntegerField(default=0)

    def like(self):
        self.rating_post += 1
        self.save()

    def dislike(self):
        self.rating_post -= 1
        self.save()

    def preview(self):
        return self.text[0:124] + '...'


    def __str__(self):
        return f'{self.title.title()}: {self.text[:128]}'

class PostCategory(models.Model):
    post_through = models.ForeignKey(Post, on_delete=models.CASCADE)
    category_through = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_post = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    auto_data = models.DateTimeField(auto_now_add=True)
    rating_comment = models.IntegerField(default=0)
    def like(self):

        self.rating_comment += 1
        self.save()

    def dislike(self):

        self.rating_comment -= 1
        self.save()

