from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Category(models.Model):  # 创建分类
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    name = models.CharField(max_length=50, verbose_name='名称')
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    is_nav = models.BooleanField(default=False, verbose_name="是否为导航栏")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="作者")

    # 展示名字
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = "分类"


class Tag(models.Model):  # 标签
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    name = models.CharField(max_length=50, verbose_name='名称')
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="作者")

    # 展示名字
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = "标签"


class Post(models.Model):  # 文章
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
        (STATUS_DRAFT, "草稿"),
    )

    title = models.CharField(max_length=255, verbose_name="标题")
    desc = models.CharField(max_length=1024, blank=True, verbose_name="摘要")
    content = models.TextField(verbose_name="正文", help_text="正文必须是MarkDonw格式")
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="分类")
    tag = models.ManyToManyField(Tag, verbose_name="标签")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="作者")

    # 展示名字
    def __str__(self):
        return self.title

    # 标签处理
    @staticmethod
    def get_by_tag(tag_id):
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            tag = None
            post_list = []
        else:
            post_list = tag.post_set.filter(status=Post.STATUS_NORMAL) \
                .select_related('owner', 'category')

        return post_list, tag

    # 分类处理
    @staticmethod
    def get_by_category(category_id):
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            category = None
            post_list = []
        else:
            post_list = category.post_set.filter(status=Post.STATUS_NORMAL) \
                .select_related('owner', 'category')

        return post_list, category

    # 最近文章
    @classmethod
    def latest_posts(cls):
        queryset = cls.objects.filter(status=cls.STATUS_NORMAL)
        return queryset

    class Meta:
        verbose_name = verbose_name_plural = "文章"
        ordering = ['-id']  # 根据 id 降序排序
