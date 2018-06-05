from django.db import models


# 用户管理
class UserManager(models.Manager):

    def register_user(self, username, nickname, password):
        """
        注册用户
        :return:
        """
        self.create(username=username, nickname=nickname, password=password)


    def query_user_count(self, username, password):
        """
        查找用户名密码匹配的用户
        :param username: 用户名
        :param password: 密码
        :return:
        """
        return self.filter(username__exact=username, password__exact=password).count()


    def get_nickname(self, username):
        """
        获取用户昵称
        :param username:
        :return:
        """
        return self.get(username__exact=username).nickname


# 项目管理
class ProjectManager(models.Manager):

    def create_project(self, **kwargs):
        self.create(**kwargs)


    def update_project(self, id, **kwargs):
        obj = self.get(id=id)
        obj.save()


# 模块管理
class ModuleManager(models.Manager):
    pass


# 用例管理
class TestCaseManager(models.Manager):
    pass


# 环境管理
class EnvManager(models.Manager):
    pass