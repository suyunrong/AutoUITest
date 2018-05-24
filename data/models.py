from django.db import models

# Create your models here.


# 基础模型
class BaseModel(models.Model):
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        abstract = True
        verbose_name = '公共字段'


# 用户模型
class UserInfo(BaseModel):
    class Meta:
        verbose_name = '用户信息'
        db_table = 'UserInfo'
    username = models.CharField('用户名', max_length=20)
    password = models.CharField('密码', max_length=20)
    status = models.IntegerField('可用/不可用', default=1)


# 项目模型
class ProjectInfo(BaseModel):
    class Meta:
        verbose_name = '项目信息'
        db_table = 'Projectinfo'
    project_name = models.CharField('项目名称', max_length=64)
    dev_leader = models.CharField('开发负责人', max_length=32)
    test_leader = models.CharField('测试负责人', max_length=32)
    simple_desc = models.CharField('简要描述', max_length=120, null=True)
    other_desc = models.CharField('其他描述', max_length=120, null=True)

    def __str__(self):
        return self.project_name


# 模块模型，与项目多对一
class ModuleInfo(BaseModel):
    class Meta:
        verbose_name = '模块信息'
        db_table = 'ModuleInfo'
    module_name = models.CharField('模块名称', max_length=64)
    belong_project = models.ForeignKey(ProjectInfo, on_delete=models.CASCADE)
    test_user = models.CharField('测试人员', max_length=120)
    simple_desc = models.CharField('简要描述', max_length=120, null=True)

    def __str__(self):
        return self.module_name


# 测试用例模型
class TestCaseInfo(BaseModel):
    class Meta:
        verbose_name = '测试用例信息'
        db_table = 'TestCaseInfo'
    case_name = models.CharField('用例名称', max_length=200)
    belong_module = models.ForeignKey(ModuleInfo, on_delete=models.CASCADE)
    case_desc = models.TextField('用例描述')
    author = models.CharField('所有者', max_length=32)
    is_execute = models.BooleanField('是否执行', default=True)

    def __str__(self):
        return self.case_name


# 测试脚本模型
class TestCaseScriptInfo(BaseModel):
    class Meta:
        verbose_name = '测试脚本信息'
        db_table = 'TestCaseScriptInfo'
    belong_module = models.ForeignKey(TestCaseInfo, on_delete=models.CASCADE)
    script_desc = models.TextField('脚本描述')
    script_step = models.IntegerField('操作步骤', default=1)
    operate_type = models.CharField('操作类型', max_length=32)
    element_pos = models.TextField('元素定位')
    operate_val = models.TextField('操作值', null=True)
    expect_val = models.TextField('预期结果', null=True)
    sleep_time = models.IntegerField('睡眠时间', default=0)


# 测试环境模型
class EnvInfo(BaseModel):
    class Meta:
        verbose_name = '测试环境信息'
        db_table = 'EnvInfo'
    env_name = models.CharField('环境名称', max_length=32)
    base_url = models.CharField('环境URL', max_length=120)
    explorer_name = models.CharField('浏览器名称', max_length=32)
    explorer_version = models.CharField('浏览器版本', max_length=32)
    simple_desc = models.CharField('简要描述', max_length=120, null=True)
