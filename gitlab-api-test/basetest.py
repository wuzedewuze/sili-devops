# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# # @Time : 2019/11/14 9:44
# # @Author : "wuyang"
# # @Email : wuyang_229@126.com
# # @File : basetest.py
# # @Software: PyCharm
#
# import  gitlab
#
#
#
# # 登录project
# gl = gitlab.Gitlab(gitlab_url, token)
#
# # 获取第一页project
# #projects_page1 = gl.projects.list()
# # for p in gl.projects.list(page=1):
# #     print(p.name, p.id)
#
# # 查询project
# # search_projects = gl.projects.list(search='vas')
# # for p in search_projects:
# #     print(p.name, p.id)
#
# # 创建一个项目。 这里不测试
# # 获取指定project
# search_projects = gl.projects.list(search='django_login_manager ')
# for p in search_projects:
#     print(p.id,p.name)
#
# # project = gl.projects.get(384)
# # print(project)
# #print(project.name, project.id)
# # 获取分支
# # branches = project.branches.list()
# # print(branches)
# # # 获取分支属性
# # branch = project.branches.get('master')
# # print(branch)
#
#
#
#
#
#
#
