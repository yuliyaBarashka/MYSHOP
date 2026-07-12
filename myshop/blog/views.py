from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from .models import BlogPost


class BlogListView(ListView):
    model = BlogPost
    template_name = 'blog/blog_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        # Выводим только опубликованные статьи
        return BlogPost.objects.filter(is_published=True).order_by('-created_at')


class BlogDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/blog_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        old_views = obj.views_count
        obj.views_count += 1
        obj.save()

        # Если статья достигла 100 просмотров, отправляем поздравление
        if old_views < 100 and obj.views_count >= 100:
            self.send_congratulation_email(obj)

        return obj

    def send_congratulation_email(self, post):
        subject = f'🎉 Поздравление! Статья "{post.title}" набрала 100 просмотров!'
        message = f'''
        Поздравляем!

        Ваша статья "{post.title}" набрала {post.views_count} просмотров!

        Продолжайте в том же духе!

        Ссылка на статью: http://localhost:8000/blogs/{post.pk}/

        ---
        С уважением, команда интернет-магазина
        '''

        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.ADMIN_EMAIL],
                fail_silently=False,
            )
        except Exception as e:
            print(f'Ошибка отправки email: {e}')

class BlogCreateView(CreateView):
    model = BlogPost
    template_name = 'blog/blog_form.html'
    fields = ['title', 'content', 'preview', 'is_published']
    success_url = reverse_lazy('blog:list')

class BlogUpdateView(UpdateView):
    model = BlogPost
    template_name = 'blog/blog_form.html'
    fields = ['title', 'content', 'preview', 'is_published']

    def get_success_url(self):
        # Перенаправляем на страницу отредактированной статьи
        return reverse_lazy('blog:detail', kwargs={'pk': self.object.pk})

class BlogDeleteView(DeleteView):
    model = BlogPost
    template_name = 'blog/blog_confirm_delete.html'
    success_url = reverse_lazy('blog:list')