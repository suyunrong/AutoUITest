from django.contrib import admin

# Register your models here.

from DataServer.models import UserInfo, Projectinfo, ModuleInfo, TestCaseInfo, TestCaseScriptInfo, EnvInfo


@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'password', 'status', 'create_time', 'update_time')
    list_per_page = 10
    ordering = ('-create_time',)
    list_display_links = ('username',)
    # 筛选器
    list_filter = ('username',)  # 过滤器
    search_fields = ('username',)  # 搜索字段
    date_hierarchy = 'update_time'  # 详细时间分层筛选


@admin.register(Projectinfo)
class ProjectinfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'project_name', 'dev_leader', 'test_leader', 'simple_desc', 'other_desc', 'create_time',
                    'update_time')
    list_per_page = 10
    ordering = ('-create_time',)
    list_display_links = ('project_name',)
    # 筛选器
    list_filter = ('project_name', 'test_leader')  # 过滤器
    search_fields = ('project_name', 'test_leader')  # 搜索字段
    date_hierarchy = 'update_time'  # 详细时间分层筛选


@admin.register(ModuleInfo)
class ModuleInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'module_name', 'test_user', 'simple_desc', 'create_time', 'update_time')
    list_per_page = 10
    ordering = ('-create_time',)
    list_display_links = ('module_name',)
    # 筛选器
    list_filter = ('module_name', 'test_user')  # 过滤器
    search_fields = ('module_name', 'test_user')  # 搜索字段
    date_hierarchy = 'update_time'  # 详细时间分层筛选


@admin.register(TestCaseInfo)
class TestCaseInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'case_name', 'case_desc', 'author', 'is_execute', 'create_time', 'update_time')
    list_per_page = 10
    ordering = ('-create_time',)
    list_display_links = ('case_name',)
    # 筛选器
    list_filter = ('case_name', 'author', 'is_execute')  # 过滤器
    search_fields = ('case_name', 'author')  # 搜索字段
    date_hierarchy = 'update_time'  # 详细时间分层筛选


@admin.register(TestCaseScriptInfo)
class TestCaseScriptInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'script_desc', 'script_step', 'operate_type', 'element_pos', 'operate_val',
                    'expect_val', 'sleep_time', 'create_time', 'update_time')
    list_per_page = 10
    ordering = ('-create_time',)
    list_display_links = ('script_desc',)
    # 筛选器
    list_filter = ('script_name', )  # 过滤器
    search_fields = ('script_desc', 'operate_type')  # 搜索字段
    date_hierarchy = 'update_time'  # 详细时间分层筛选


@admin.register(EnvInfo)
class EnvInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'env_name', 'base_url', 'explorer_name', 'explorer_version', 'simple_desc', 'create_time',
                    'update_time')
    list_per_page = 10
    ordering = ('-create_time',)
    list_display_links = ('env_name',)
    # 筛选器
    list_filter = ('env_name', 'explorer_name')  # 过滤器
    search_fields = ('env_name', 'explorer_name')  # 搜索字段
    date_hierarchy = 'update_time'  # 详细时间分层筛选


admin.site.site_header = 'AutoUITest后台系统'

admin.site.site_title = 'AutoUITest'
