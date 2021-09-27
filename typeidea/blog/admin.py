from django.contrib import admin
from django.urls import reverse

from .models import Post, Category, Tag
from django.utils.html import format_html
from .adminforms import PostAdminForm
from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnerAdmin
from django.contrib.admin.models import LogEntry


# Register your models here.

# 同一页面编辑关联数据 -》 分类页面直接编辑文章
class PostInline(admin.TabularInline):  # StackedInline
    fields = ('title', 'desc')
    extra = 1  # 控制额外多几个
    model = Post


# @admin.register(Category)
@admin.register(Category, site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    # 关联文章
    inlines = [PostInline, ]

    list_display = ('name', 'status', 'is_nav', 'create_time', 'post_count')

    fields = ('name', 'status', 'is_nav', 'owner')

    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(CategoryAdmin, self).save_model(request, obj, form, change)

    # 统计文章数量
    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_descrition = "文章数量"


@admin.register(Tag, site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'create_time')
    fields = ('name', 'status')

    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(TagAdmin, self).save_model(request, obj, form, change)


class CategoryOwnerFilter(admin.SimpleListFilter):
    '''自定义过滤器只展示当前用户的分类'''
    title = '分类过滤器'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=category_id)
        return queryset


@admin.register(Post, site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    # 添加 form
    form = PostAdminForm

    list_display = [
        'title', 'category', 'status', 'create_time', 'owner', 'operator'
    ]
    list_display_links = []

    # list_filter = ['category']
    list_filter = [CategoryOwnerFilter]
    search_fields = ['title', 'category__name']

    actions_on_top = True
    # actions_on_bottom = True

    # 编辑页面
    save_on_top = True

    # 不展示内容
    exclude = ('owner',)

    # fields =(
    #     ('category', 'title'),
    #     'desc',
    #     'status',
    #     'content',
    #     'tag',
    # )

    # 使用 fieldsets
    fieldsets = (
        ('基础配置', {
            'description': '基础配置描述',
            'fields': (
                ('title', 'category'),
                'status',
            ),
        }),
        ('内容', {
            'fields': (
                'desc',
                'content',
            ),
        }),
        ('额外信息', {
            'classes': ('collapse',),
            'fields': ('tag',),
        })
    )

    def operator(self, obj):
        return format_html(
            # '<a href="{}">编辑</a>',reverse('admin:blog_post_change', args=(obj.id,))
            '<a href="{}">编辑</a>', reverse('cus_admin:blog_post_change', args=(obj.id,))
        )

    operator.short_description = '操作'

    def owner(self, obj):
        return obj.user

    owner.short_descrition = '作者'

    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(PostAdmin, self).save_model(request, obj, form, change)
    #
    # # 作者文章过滤
    # def get_queryset(self, request):
    #     qs = super(PostAdmin, self).get_queryset(request)
    #     return qs.filter(owner=request.user)

    # 自定义静态资源
    class Media:
        css = {
            'all': ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css",),

        }
        js = ('https://cds.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundles.js',)


# log out
@admin.register(LogEntry, site=admin.site)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['object_repr', 'object_id', 'action_flag', 'user', 'change_message']
