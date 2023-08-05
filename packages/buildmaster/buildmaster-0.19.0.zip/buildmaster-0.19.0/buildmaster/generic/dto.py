# encoding=utf8

from flask_restplus import fields
from flask_restplus import reqparse
from werkzeug.datastructures import FileStorage
from ..app import api

generic_entity = api.model("Generic entity", {
})

relation = api.model('Relation query', {
    'model': fields.String(description="关联表模型", required=True),
    'fromKey': fields.String(description="关联左键名字", required=True),
    'fromData': fields.List(fields.String, description="关联左键ID数组", required=True),
    'toKey': fields.String(description="关联右键名字", required=True),
    'toData': fields.List(fields.String, description="关联右键ID数组", required=True),
})

relation_update = api.model('Relation update', {
    'model': fields.String(description="关联表模型", required=True),
    'addData': fields.List(fields.Raw, description="增加的关联关系数据[{leftKey:'', rightKey: ''}]"),
    'delData': fields.List(fields.Raw, description="删除的关联关系数据[{leftKey:'', rightKey: ''}]")
})

model_sync = api.model('Model sync', {
    'model': fields.String(description="业务模型", required=True),
})

model_delete = api.model('Model delete', {
    'model': fields.String(description="需要删除的模型")
})

module_delete = api.model('Module delete', {
    'module': fields.String(description="需要删除的业务模块")
})


model_create = api.model('Model create', {
    'model': fields.String(description="业务模型", required=True),
    'table': fields.String(description="数据库表", required=True),
    'displayName': fields.String(description="业务名称", required=False),
    'module': fields.String(description="业务模块", required=False),
    'roleId': fields.String(description="默认赋权的角色Id，不提供则不赋权给任何角色", required=False)
})

model_copy = api.model('Model copy', {
    'copyModel': fields.String(description="拷贝的业务模型", required=True),
    'model': fields.String(description="新的业务模型", required=True),
    'displayName': fields.String(description="业务名称", required=False)
})

model_pattern_create = api.model('Model pattern create', {
    'tablePrefix': fields.String(description="匹配的表前缀"),
    'module': fields.String(description="业务模块", required=False),
    'roleId': fields.String(description="默认赋权的角色Id，不提供则不赋权给任何角色", required=False)
})

resource_create = api.model('Resource create', {
    'type': fields.String(description="资源类型", required=True),
    'resource': fields.String(description="资源", required=True),
    'name': fields.String(description="资源名称", required=True)
})

model_func_create = api.model('Model function create', {
    'model': fields.String(description="模型名称", required=True),
    'funcKey': fields.String(description="功能（funcKey）", required=True)
})

menu_func_create = api.model('Menu function create', {
    'url': fields.String(description="菜单URL", required=True),
    'name': fields.String(description="菜单名字", required=True),
    'module': fields.String(description="菜单所属模块", required=False)
})

menu_func = api.model('Menu function', {
    'url': fields.String(description="菜单URL", required=True)
})

search_by_key = api.model('Generic full search', {
    'key': fields.String(description="查询关键词"),
    'page': fields.Integer(description="指定从返回结果中的第几页开始显示。默认值是1。", default=1),
    'limit': fields.Integer(description="指定返回结果中每页显示的记录数量", default=10),
    'doCount': fields.Integer(description="统计总数, 0--仅数据, 1/None--数据+总数, 2--仅总数"),
    'columns': fields.List(fields.String, description="指定需要的列[prop]"),
    'where': fields.Raw(description="JSON条件表达式 { 'name': 'rushmore', 'age': {'>': 10 } }"),
    'joinCond': fields.Raw(description="关联表的条件表达式 { '_user.id': 1 }"),
    'order': fields.List(fields.String, description="排序, 示例[\"id desc\"]"),
})

search_data = api.model('Generic search', {
    'columns': fields.List(fields.String, description="指定需要的列[prop]"),
    'where': fields.Raw(description="JSON条件表达式 { 'name': 'rushmore', 'age': {'>': 10 } }"),
    'joinCond': fields.Raw(description="关联表的条件表达式 { '_user.id': 1 }"),
    'order': fields.List(fields.String, description="排序, 示例[\"id desc\"]"),
})


generic_import = reqparse.RequestParser()
generic_import.add_argument('file', location='files', type=FileStorage, help="导入EXCEL文件", required=True)
generic_import.add_argument('model', location='form', help="业务模型", required=True)
generic_import.add_argument('overwrite', location='form', type=str, help="是否存在覆盖", default='1', required=False)
generic_import.add_argument('column', location='form', help="文件、图片关联字段", required=False)
generic_import.add_argument('zip', location='files', type=FileStorage, help="文件、图片ZIP文件", required=False)
generic_import.add_argument('tag', location='form', help="上传的zip文件的Tag，用于提示后台存储路径更新", required=False)

module_import = reqparse.RequestParser()
module_import.add_argument('file', location='files', type=FileStorage, help="模块JSON文件", required=True)
module_import.add_argument('roleId', location='form', help="默认关联的角色Id", required=False)
module_import.add_argument('overwrite', location='form', help="是否覆盖已有，0-否，1-是", required=False)

dict_domain = reqparse.RequestParser()
dict_domain.add_argument('domain', type=str, location='args', help="字典领域，多领域用逗号分隔", required=False)

acl_func = reqparse.RequestParser()
acl_func.add_argument('userId', type=str, location='args', help="用户Id，默认为当前登录用户", required=False)
acl_func.add_argument('resource_type', type=str, location='args', help="功能分类诸如model,url,func", required=False)
acl_func.add_argument('resource', type=str, location='args', help="资源标识，默认所有", required=False)

acl_func_role = reqparse.RequestParser()
acl_func_role.add_argument('roleId', type=str, location='args', help="角色Id", required=True)
acl_func_role.add_argument('resource_type', type=str, location='args', help="功能分类诸如model,url,func", required=False)
acl_func_role.add_argument('resource', type=str, location='args', help="资源标识，默认所有", required=False)

acl_data = reqparse.RequestParser()
acl_data.add_argument('userId', type=str, location='args', help="用户Id，默认为当前登录用户", required=False)
acl_data.add_argument('model', type=str, location='args', help="业务模型，默认所有", required=False)

acl_data_role = reqparse.RequestParser()
acl_data_role.add_argument('roleId', type=str, location='args', help="角色Id", required=True)
acl_data_role.add_argument('model', type=str, location='args', help="业务模型，默认所有", required=False)

link = reqparse.RequestParser()
link.add_argument('link_table', type=str, location='args', help="关联关系表", required=True)

sys_config = reqparse.RequestParser()
sys_config.add_argument('orgId', type=str, location='args', help='组织id')

menu = reqparse.RequestParser()
menu.add_argument('orgId', type=str, location='args', help='组织id')

create_org = api.model('Create org', {
    'desc': fields.String(description=r"描述", required=True),
    'name': fields.String(description="组织名称"),
    'defaultPage': fields.String(description="默认页面"),
    'copyOrgId': fields.String(description="复制的组织ID"),
    'parentId': fields.String(description="上级组织ID")
})

delete_org = api.model("delete_org", {
    'id': fields.String(description="orgId")
})

create_role = api.model('Create role', {
    'name': fields.String(description="角色名", required=True),
    'code': fields.String(description=r"角色编码"),
    'parentId': fields.String(description="上级角色ID")
})

copy_role = api.model('Copy role', {
    'fromId': fields.String(description="来源角色ID"),
    'toId': fields.String(description="目标角色ID")
})

role_op = api.model('Operation on role', {
    'op': fields.String(description="操作动作，加/减(plus/minus)"),
    'changeRoleId': fields.String(description="需要改变的角色ID"),
    'roleId': fields.String(description="角色ID")
})


logger_control = api.model('Logger level control', {
    'level': fields.String(description="日志等级 [DEBUG,DEFAULT,INFO,WARNING,ERROR,OFF]", required=True),
    'entry': fields.String(description='控制的日志的影响范围，由entry决定，默认不填控制所有', required=False)
})

