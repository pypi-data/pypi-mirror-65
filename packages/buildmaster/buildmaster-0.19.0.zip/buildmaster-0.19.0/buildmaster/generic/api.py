# encoding=utf8
import json
from flask_restplus import Resource
from flask import request, make_response, send_file, after_this_request
from ..db import Dict
from datetime import datetime
from ..app import (
    api, db, dbplus,
    auth_required, auth_user,
    settings
)
from ..log import log_action
from . import dto
from ..utils import upload_zip
from functools import wraps
import logging
import base64
import hashlib
import pandas as pd
import re


ns = api.namespace(name='generic', description="业务模型通用操作")

_t = db.escape


def clear_cache(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        finally:
            dbplus.clear_cache()
    return wrapper


@ns.route('/search/<model>')
class GenericSearch(Resource):
    @auth_required
    @api.expect(dto.search_by_key)
    def post(self, model):
        """条件查询"""
        u = auth_user()
        args = Dict(request.json or {})
        if not model:
            return {'message': 'model required'}, 400
        return dbplus.search(u, model, args)


@ns.route('/model_copy')
class GenericModelCopy(Resource):

    @auth_required
    @log_action()
    @api.expect(dto.model_copy)
    def post(self):
        """复制模型"""
        u = auth_user()
        args = Dict(request.json or {})
        model = args.model
        copy_model = args.copyModel
        display_name = args.displayName
        if not model:
            return {'message': 'model required'}, 400
        if not copy_model:
            return {'message': 'copyModel required'}, 400

        with dbplus.session() as s:
            return dbplus.copy_model(u, copy_model, model,
                                     display_name=display_name, copy_acl=True, session=s)


@ns.route('/search_one/<model>')
class GenericSearchOne(Resource):
    @auth_required
    @api.expect(dto.search_data)
    def post(self, model):
        """条件查询"""
        u = auth_user()
        args = Dict(request.json or {})
        if not model:
            return {'message': 'model required'}, 400
        return dbplus.search_one(u, model, args)


@ns.route('/search_all/<model>')
class GenericSearchAll(Resource):
    @auth_required
    @api.expect(dto.search_data)
    def post(self, model):
        """条件查询"""
        u = auth_user()
        args = Dict(request.json or {})
        if not model:
            return {'message': 'model required'}, 400
        return dbplus.search_all(u, model, args)


@ns.route('/export/<model>')
class GenericExport(Resource):
    @auth_required
    @api.expect(dto.search_by_key)
    def post(self, model):
        """查询导出Excel"""
        u = auth_user()
        args = Dict(request.json or {})
        if not model:
            return {'message': 'model required'}, 400
        f, status = dbplus.export(u, model, args)
        if status != 200:
            return f, status
        full_path = f"{f.path}/{f.filename}"
        response = make_response(send_file(full_path))
        response.headers["Content-Type"] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response.headers["Content-Disposition"] = f"attachment; filename={f.filename}"
        return response


@ns.route('/one/<model>/<id>')
class GenericOne(Resource):
    @auth_required
    def get(self, model, id):
        """查询单条记录"""
        u = auth_user()
        return dbplus.query_one(u, model, id)


@ns.route('/one/<model>')
class GenericOne(Resource):
    @auth_required
    @api.expect(dto.search_data)
    def post(self, model):
        """条件查询单条记录"""
        u = auth_user()
        args = Dict(request.json or {})
        if not model:
            return {'message': 'model required'}, 400
        return dbplus.search_one(u, model, args)


@ns.route('/create/<model>')
class GenericCreate(Resource):
    @auth_required
    @log_action()
    @api.expect(dto.generic_entity)
    def post(self, model):
        """创建表单"""
        u = auth_user()
        data = Dict(request.json)
        try:
            return dbplus.create(u, model, data)
        finally:
            dbplus.evict_cache(model)


@ns.route('/update/<model>')
class GenericUpdate(Resource):
    @auth_required
    @log_action()
    @api.expect(dto.generic_entity)
    def post(self, model):
        """更新表单"""
        user = auth_user()
        data = Dict(request.json)
        try:
            return dbplus.update(user, model, data)
        finally:
            dbplus.evict_cache(model)


@ns.route('/delete/<model>/<id>')
class GenericDelete(Resource):

    @auth_required
    @log_action(action="delete")
    def delete(self, model, id):
        """删除表单"""
        if not model:
            return {'message': f'{model} required'}, 400
        if not id:
            return {'message': f'{id} required'}, 400

        u = auth_user()
        try:
            return dbplus.delete(u, model, id)
        finally:
            dbplus.evict_cache(model)


@ns.route('/info/<model>')
class GenericInfo(Resource):
    @auth_required
    def get(self, model):
        """表单元信息"""
        # TODO 数据权限控制用户只能查询授权的实体信息
        u = auth_user()

        info = dbplus.model_info(model, u)
        if not info or len(info.props) == 0:
            return {'message': f'{model}不存在'}, 404

        dict_domains = [info.props[c].get('transDict') for c in info.props if info.props[c].get('transDict')]
        domains = {}
        if len(dict_domains):
            domains = dbplus.find_dict_domains(dict_domains)

        link_domains = dbplus.find_link_domains(u, info)
        domains.update(link_domains)

        acl = dbplus.acl_model(u.id, model)
        return {
            'model': info.model,
            'props': info.props,
            'dict': domains,
            'acl': acl
        }


@ns.route('/model_relation/<model>')
class ModelRelation(Resource):
    @auth_required
    def get(self, model):
        """联动模型属性"""
        u = auth_user()

        link_models = db.query('select * from _model_relation where model=:model order by displayOrder', model=model)
        for m in link_models:
            m['acl'] = dbplus.acl_model(u.id, m.linkModel)
        return link_models


@ns.route('/info/save')
class GenericInfoSave(Resource):

    @clear_cache
    @auth_required
    @log_action()
    @api.expect(dto.generic_entity)
    def post(self):
        """更新列元数据"""

        u = auth_user()
        data = Dict(request.json)
        if not data.id:     # 没有ID则，必须有model + name来确定
            if not data.model:
                return {'message': 'model required'}, 400
            if not data.name:
                return {'message': 'name required'}, 400
            sql = f"select * from _prop where model=:model and name=:name"
            prop = db.query_one(sql, model=data.model, name=data.name)
        else:
            sql = f"select * from _prop where id=:id"
            prop = db.query_one(sql, id=data.id)

        if not prop:
            if not data.model:
                return {'message': 'model required'}, 400
            if not data.name:
                return {'message': 'name required'}, 400
            return dbplus.create(u, '_prop', data)
        else:
            if data.model and prop['model'] != data.model:
                return {'message': 'Model can not change'}, 400
            data['id'] = prop['id']
            return dbplus.update(u, '_prop', data)


@ns.route('/dict')
class DictInfo(Resource):
    @auth_required
    @api.expect(dto.dict_domain)
    def get(self):
        """根据领域读取字典信息"""

        args = dto.dict_domain.parse_args()
        domain = args.domain
        domains = []
        if domain:
            domains = domain.split(',')

        return dbplus.find_dict_domains(domains)


@ns.route('/relation_update')
class RelationSet(Resource):

    @auth_required
    @log_action()
    @api.expect(dto.relation_update)
    def post(self):
        """关联关系更新"""
        u = auth_user()
        rel = Dict(request.json)
        if not rel.model:
            return {'message': f'model required'}, 400
        if not rel.addData and not rel.delData:
            return {'message': f'addData or delData at least one required'}, 400
        try:
            return dbplus.relation_update(u, relation_model=rel.model,
                                          add_data=rel.addData or [],
                                          del_data=rel.delData or [])
        finally:
            dbplus.evict_cache(rel.model)


default_func = {
    'queryEnabled': '搜索',
    'viewEnabled': '详情',
    'createEnabled': '创建',
    'updateEnabled': '更新',
    'deleteEnabled': '删除'
}

default_menu_func = {
    'viewEnabled': '详情'
}


@ns.route('/model_create')
class ModelCreate(Resource):
    @clear_cache
    @auth_required
    @log_action()
    @api.expect(dto.model_create)
    def post(self):
        """增加模型"""

        user = auth_user()
        args = Dict(request.json)
        return generate_model(user, args)


@ns.route('/model_pattern_create')
class ModelPatternCreate(Resource):

    @clear_cache
    @auth_required
    @log_action()
    @api.expect(dto.model_pattern_create)
    def post(self):
        """表前缀匹配批量增加模型"""

        user = auth_user()
        data = Dict(request.json)
        pattern = data.tablePrefix
        module = data.module
        roleId = data.roleId
        res = []
        for name in db.tables:
            t = db.tables[name]
            if not name.startswith(pattern):
                continue
            args = Dict({
                'model': name,
                'displayName': t.comment or name,
                'table': name,
                'module': module,
                'roleId': roleId
            })
            res.append(generate_model(user, args))
        return res


def generate_model_acl(user, args, session=None):
    model = args.model
    r = db.query_one(f"select * from _resource where resource=:model and type='model'", model=model)
    if not r:
        resource = {
            'name': args.displayName,
            'resource': args.model,
            'type': 'model',
            'module': args.module
        }
        r, status = dbplus.create(user, '_resource', resource, session=session)
        if status != 200:
            return r, status

        acl_func_list = []
        for key in default_func:
            acl_func = {
                'resourceId': r['id'],
                'funcKey': key,
                'funcName': default_func[key]
            }
            acl_func_list.append(acl_func)
        db.add_many('_acl_func', acl_func_list, session=session)

    if args.roleId:
        if session is None:
            with db.session() as s:
                auth_role_func_list(s, args.roleId, r['id'])
        else:
            auth_role_func_list(session, args.roleId, r['id'])

    return None, 200


def generate_model(user, args):
    with db.session() as s:
        res, status = dbplus.create(user, '_model', args, session=s)
        if status != 200:
            return res, status
        res, status = dbplus.sync_model(args.model, session=s)
        if status != 200:
            return res, status

    generate_model_acl(user, args)

    return res, status


def auth_role_func_list(sess, roleId, resourceId):
    """
    把资源的所有功能赋权给角色
    :param sess:
    :param roleId:
    :param resourceId:
    :return:
    """
    role = sess.query_one('select * from _role where id=:id', id=roleId)
    if not role:
        return
    func_list = sess.query('select * from _acl_func where resourceId=:id', id=resourceId)
    if not func_list:
        return

    sql = f"""
    select * from _role_acl_func where roleId=:roleId and aclFuncId in :funcIds
    """
    exist_role_func_list = db.query(sql, roleId=roleId, funcIds=[f['id'] for f in func_list])
    exist_func_set = set([rf['aclFuncId'] for rf in exist_role_func_list])
    role_func_list = []
    for f in func_list:
        if f['id'] in exist_func_set:
            continue
        role_func_list.append({
            'roleId': roleId,
            'aclFuncId': f['id']
        })
    if len(role_func_list) > 0:
        sess.add_many('_role_acl_func', role_func_list)


@ns.route('/resource_create')
class ResourceCreate(Resource):

    @clear_cache
    @auth_required
    @log_action()
    @api.expect(dto.resource_create)
    def post(self):
        """增加权限资源"""

        user = auth_user()
        args = Dict(request.json)
        res, status = dbplus.create(user, '_resource', args)
        if status != 200:
            return res, status

        acl_func_list = []
        func_table = default_func
        if args.type == 'menu':
            func_table = default_menu_func
        for key in func_table:
            acl_func = {
                'resourceId': res['id'],
                'funcKey': key,
                'funcName': func_table[key]
            }
            acl_func_list.append(acl_func)
        db.add_many('_acl_func', acl_func_list)

        return res, status


@ns.route('/resource_delete/<id>')
class ResourceDelete(Resource):

    @clear_cache
    @auth_required
    @log_action(action='delete')
    def delete(self, id):
        """根据ID删除资源（级联删除对应资源的功能权限定义，授权数据）"""
        u = auth_user()
        with db.session() as s:
            res = dbplus.check_perm(u, '_resource', 'deleteEnabled', '删除资源', session=s)
            if res.status != 200:
                return res.message, res.status

            sql = f"""delete rf from _role_acl_func rf
            join _acl_func f on rf.aclFuncId=f.id
            where f.resourceId=:id"""
            s.execute(sql, id=id)

            sql = f"""
            delete from _acl_func where resourceId=:id
            """
            s.execute(sql, id=id)
            sql = f"""
            delete from _resource where id=:id
            """
            s.execute(sql, id=id)


@ns.route('/acl_func_delete/<id>')
class FuncDelete(Resource):

    @clear_cache
    @auth_required
    @log_action(action='delete')
    def delete(self, id):
        """根据ID删除功能（级联删除对应的授权数据）"""
        u = auth_user()
        try:
            with db.session() as s:
                sql = f"""delete from _role_acl_func where aclFuncId=:id"""
                s.execute(sql, id=id)
                res, status = dbplus.delete(u, '_acl_func', id, s)
                if status != 200:
                    raise Exception()  # rollback
        finally:
            return res, status


@ns.route('/acl_prop_delete/<id>')
class AclPropDelete(Resource):

    @clear_cache
    @auth_required
    @log_action(action='delete')
    def delete(self, id):
        """根据ID删除属性（级联删除对应的列权限授权数据）"""
        u = auth_user()
        try:
            with db.session() as s:
                sql = f"""delete from _role_prop where propId=:id"""
                s.execute(sql, id=id)
                res, status = dbplus.delete(u, '_prop', id, s)
                if status != 200:
                    raise Exception()  # rollback
        finally:
            return res, status


@ns.route('/acl_data_delete/<id>')
class AclDataDelete(Resource):

    @clear_cache
    @auth_required
    @log_action(action='delete')
    def delete(self, id):
        """根据ID删除数据权限（级联删除对应的授权数据）"""
        u = auth_user()
        try:
            with db.session() as s:
                sql = f"""delete from _role_acl_data where aclDataId=:id"""
                s.execute(sql, id=id)
                res, status = dbplus.delete(u, '_acl_data', id, s)
                if status != 200:
                    raise Exception()  # rollback
        finally:
            return res, status


@ns.route('/seq_delete/<id>')
class SeqDelete(Resource):

    @clear_cache
    @auth_required
    @log_action(action='delete')
    def delete(self, id):
        """删除模型"""

        user = auth_user()
        res, status = None, 200
        try:
            with db.session() as s:
                res = dbplus.check_perm(user, '_seq', 'deleteEnabled', '删除序列发生器', session=s)
                if res.status != 200:
                    return res.message, res.status
                sql = "delete sv from _seq_value sv join _seq s on sv.seqId=s.id where s.id=:id"
                db.execute(sql, id=id, session=s)
                res, status = dbplus.delete(user, '_seq', id, session=s)
                if status != 200:
                    raise Exception(res.message)
        except:
            return res, status


@ns.route('/model_func_create')
class ModelFuncCreate(Resource):

    @clear_cache
    @auth_required
    @log_action()
    @api.expect(dto.model_func_create)
    def post(self):
        """增加模型的功能定义"""

        user = auth_user()
        args = Dict(request.json)
        if not args.model:
            return {'message': 'model required'}, 400
        if not args.funcKey:
            return {'message': 'funcKey required'}, 400

        resource = db.query_one(f"select * from _resource where type='model' and resource=:model",
                                model=args.model)
        if not resource:
            model = db.query_one(f"select displayName, module from _model where model=:model",
                                 model=args.model)
            if not model:
                return {'message': f'Model({args.model} Not Found)'}, 404

            resource = {
                'name': model.displayName,
                'resource': args.model,
                'module': model.module,
                'type': 'model',
            }
            res, status = dbplus.create(user, '_resource', resource)
            if status != 200:
                return res, status
            resource['id'] = res['id']

        acl_func = {
            'resourceId': resource['id'],
            'funcKey': args.funcKey
        }
        return db.add('_acl_func', acl_func)


@ns.route('/menu_func_create')
class MenuFuncCreate(Resource):

    @clear_cache
    @auth_required
    @log_action()
    @api.expect(dto.menu_func_create)
    def post(self):
        """增加菜单资源与功能定义（viewEnabled）"""

        user = auth_user()
        args = Dict(request.json)
        if not args.url:
            return {'message': 'url required'}, 400
        if not args.name:
            return {'message': 'name required'}, 400

        resource = db.query_one(f"select * from _resource where type='menu' and resource=:url",
                                url=args.url)
        if not resource:
            resource = {
                'name': args.name,
                'resource': args.url,
                'module': args.module,
                'type': 'menu',
            }
            res, status = dbplus.create(user, '_resource', resource)
            if status != 200:
                return res, status
            resource['id'] = res['id']

        acl_func = {
            'resourceId': resource['id'],
            'funcKey': 'viewEnabled'
        }
        with db.session() as s:
            sql = f"select * from _acl_func where resourceId=:resourceId and funcKey='viewEnabled'"
            func = s.query_one(sql, resourceId=resource['id'])
            if not func:
                return s.add('_acl_func', acl_func)
            return func


@ns.route('/menu_delete')
class MenuDelete(Resource):

    @clear_cache
    @auth_required
    @log_action('delete')
    @api.expect(dto.menu_func)
    def delete(self):
        """根据菜单URL删除菜单，包括资源和功能定义"""

        u = auth_user()
        args = Dict(request.json)
        if not args.url:
            return {'message': 'url required'}, 400

        with db.session() as s:
            r = db.query_one(f"select * from _resource where resource=:url and type='menu'", url=args.url)
            if not r:
                return {'message': f'Menu({args.url}) not found'}, 404

            # clean role auth data first
            sql = f"""delete rf from _role_acl_func rf
            join _acl_func f on rf.aclFuncId=f.id
            join _resource r on f.resourceId=r.id
            where r.resource=:url and r.type='menu'"""
            s.execute(sql, url=args.url)

            sql = f"""
            delete f from _acl_func f left join _resource r on f.resourceId=r.id
            where r.type='menu' and f.funcKey='viewEnabled' and r.resource=:url
            """
            s.execute(sql, url=args.url)

            res, status = dbplus.delete(u, '_resource', r.id, s)
            if status != 200:
                raise Exception()  # rollback


@ns.route('/menu_func')
class MenuFuncGet(Resource):
    @auth_required
    @api.expect(dto.menu_func)
    def post(self):
        """根据菜单URL获取菜单功能（ID）"""

        args = Dict(request.json)
        if not args.url:
            return {'message': 'url required'}, 400
        sql = f"""
        select f.* from _acl_func f left join _resource r on f.resourceId=r.id
        where r.type='menu' and f.funcKey='viewEnabled' and r.resource=:url
        """
        func = db.query_one(sql, url=args.url)
        if not func:
            return {'message': 'Menu function not found'}, 404

        return func


@ns.route('/model_sync')
class ModelSync(Resource):

    @clear_cache
    @auth_required
    @log_action()
    @api.expect(dto.model_sync)
    def post(self):
        """同步创建表元信息，可重复调用"""

        args = Dict(request.json)
        model = args.model
        if not model:
            return {'message': 'model required'}, 400
        res, status = dbplus.sync_model(model)
        if status != 200:
            return res, status

        sql = f"select * from _prop order by model"
        return db.query_page(sql)


@ns.route('/model_delete')
class ModelDelete(Resource):

    @clear_cache
    @auth_required
    @log_action(action='delete')
    @api.expect(dto.model_delete)
    def delete(self):
        """删除模型"""

        user = auth_user()
        args = Dict(request.json)
        model = args.model
        if not model:
            return {'message': 'Model required'}, 400

        with db.session() as s:
            return dbplus.delete_model(user, model, session=s)


@ns.route('/module_delete')
class ModuleDelete(Resource):

    @clear_cache
    @auth_required
    @log_action(action='delete')
    @api.expect(dto.module_delete)
    def delete(self):
        """删除模块"""

        user = auth_user()
        args = Dict(request.json)
        module = args.module
        if not module:
            return {'message': 'module required'}, 400
        if module == 'system':
            return {'message': '系统模块不能删除'}, 403

        with db.session() as s:
            return dbplus.delete_module(user, module, session=s)


@ns.route('/module_export/<module>')
class ModuleExport(Resource):

    @auth_required
    @log_action()
    def post(self, module):
        """模块导出"""
        res = dbplus.export_module(module)

        @after_this_request
        def set_cookie(response):
            file_name = f"module_{module}"
            response.headers["Content-Disposition"] = f"attachment; filename={file_name}.json"
            return response

        return res


@ns.route('/module_import')
class ModuleImport(Resource):

    @clear_cache
    @auth_required
    @log_action()
    @api.expect(dto.module_import)
    def post(self):
        """模块导入"""
        user = auth_user()
        args = dto.module_import.parse_args()
        data = parse_json(args)
        dbplus.import_module(user, data)


def parse_json(args):
    f = args.file
    data = json.loads(f.read(), encoding='utf8')
    f.close()
    return data


def get_col_from_title(title):
    patten = re.compile(r'(?<=\()[\w_]+(?=\))')
    res = re.search(patten, title)
    try:
        return res.group()
    except Exception as e:
        return title


@ns.route('/import')
class GenericImport(Resource):

    @auth_required
    @log_action()
    @api.expect(dto.generic_import)
    def post(self):
        """通用导入"""
        u = auth_user()
        args = dto.generic_import.parse_args()
        model = args.model
        overwrite = args.overwrite
        if overwrite is None:
            overwrite = True
        else:
            overwrite = args.overwrite != '0'

        if not model:
            return {'message': '模型必须'}, 400
        if not args.file:
            return {'message': 'EXCEL文件必须'}, 400

        filename = args.file.filename
        ext = filename.rsplit('.')[-1].lower()

        if ext != 'xls' and ext != 'xlsx':
            return {'message': '文件类型必须是Excel'}, 400

        check = dbplus.check_perm(u, model, 'importEnabled', '导入')
        if check.status != 200:
            return check.message, check.status

        xls = pd.read_excel(args.file)

        rename = {}
        for c in xls.columns.values:
            rename[c] = get_col_from_title(c)
        xls.rename(columns=rename, inplace=True)

        data = xls.fillna('').to_dict('records')

        tag = args.tag or None
        zip = args.zip
        column = args.column
        if column and zip:
            column = column.split(',')
            upload_zip(data, column, zip, tag)

        return dbplus.save_many(u, model, data, overwrite=overwrite)


def filter_menus(menu, urls):
    if 'children' not in menu:
        if 'path' not in menu:
            return
        if menu['path'] in urls:
            return menu
        return None

    children = []
    for m in menu['children']:
        res = filter_menus(m, urls)
        if res:
            children.append(res)
    if len(children) == 0:
        return None
    menu['children'] = children
    return menu


@ns.route('/menu')
class Menu(Resource):
    @auth_required
    @api.expect(dto.menu)
    def get(self):
        """获取菜单JSON数据"""
        u = auth_user()
        args = dto.menu.parse_args()
        org_id = u.orgId
        if args.orgId:
            org_id = args.orgId

        sql = f"""
        SELECT * FROM _menu WHERE orgId=:orgId
        """

        res = db.query_one(sql, orgId=org_id)
        if not res:
            return {}, 200
        return {'id': res['id'], 'json': json.loads(res['json'])}

    @auth_required
    @log_action()
    @api.expect(dto.generic_entity)
    def post(self):
        """保存菜单JSON数据"""
        user = auth_user()
        menu = Dict(request.json)
        menu.updateDate = datetime.now()
        if not menu.json:
            return {'message': '配置不能为空'}, 400
        org_id = user.orgId
        if menu.orgId:
            org_id = menu.orgId
        menu.json = json.dumps(menu.json, indent=4)
        sql = f"select id from _menu where orgId=:orgId"
        menu_db = db.query_one(sql, orgId=org_id)
        if not menu_db:
            del menu.id
            return dbplus.create(user, 'menu', menu)
        else:
            menu.id = menu_db.id
            return dbplus.update(user, 'menu', menu)


@ns.route('/sysconfig')
class SysconfigSpecial(Resource):
    @auth_required
    @api.expect(dto.sys_config)
    def get(self):
        """
        获取特定组织的系统配置
        :return:
        """
        user = auth_user()
        args = dto.sys_config.parse_args()
        org_id = user.orgId
        if args.orgId:
            org_id = args.orgId

        sql = f"""SELECT * FROM _sysconfig WHERE orgId=:orgId"""
        res = db.query_one(sql, orgId=org_id)
        if not res:
            return {}, 200
        return {'id': res['id'], 'json': json.loads(res['json'])}

    @auth_required
    @log_action()
    @api.expect(dto.generic_entity)
    def post(self):
        """
        保存特定组织的系统配置
        :return:
        """
        user = auth_user()
        conf = Dict(request.json)
        conf.updateDate = datetime.now()
        if not conf.json:
            return {'message': '配置不能为空'}, 400
        if not conf.orgId:
            return {"message": "缺少 orgId"}, 400
        conf.json = json.dumps(conf.json, indent=4)
        conf_db = db.query_one(f"select id from _sysconfig where orgId=:orgId", orgId=conf.orgId)
        if not conf_db:
            del conf.id
            return dbplus.create(user, 'sysconfig', conf)
        else:
            conf.id = conf_db.id
            return dbplus.update(user, 'sysconfig', conf)


@ns.route('/org_create')
class CreateOrg(Resource):
    @auth_required
    @log_action()
    @api.expect(dto.create_org)
    def post(self):
        """
        创建组织
        :return:
        """
        user = auth_user()
        args = Dict(request.json)

        with dbplus.session() as s:
            if not args.parentId:
                args.parentId = user.orgId  # 默认的父节点
            org, status = dbplus.create(user, '_org', args, session=s)
            if status != 200:
                return org, status

            # 找出当前新建组织的所有父节点，默认增加到所有上级组织的可管理组织中
            parent_id = org.id  # 第一个默认自己管理自己
            while parent_id:
                sql = 'select * from _org_owner where orgId=:orgId and ownerOrgId=:ownerOrgId'
                org_owner = db.query_one(sql, orgId=org.id, ownerOrgId=parent_id, session=s)
                if not org_owner:
                    db.add('_org_owner', {"ownerOrgId": parent_id, 'orgId': org.id}, session=s)

                porg = db.query_one('select * from _org where id=:id', id=parent_id, session=s)
                if not porg:
                    break
                parent_id = porg.parentId

            copy_org_id = args.copyOrgId
            if not copy_org_id:
                copy_org = s.query_one("select * from _org where id=:id", id=copy_org_id)
                if not copy_org:
                    copy_org_id = user.orgId
            if not copy_org_id:
                copy_org_id = user.orgId

            # 复制组织的菜单
            sql = f"""
            SELECT * FROM _menu WHERE orgId=:orgId
            """
            menu_db = s.query_one(sql, orgId=copy_org_id)
            sql = "insert into _menu (json,orgId,updateDate) values (:json,:orgId,:updateDate)"
            s.execute(sql, json=menu_db.json, orgId=org.id, updateDate=datetime.now())

            # 复制组织的角色
            to_org_id = org['id']
            role_owners = s.query("select * from _role_owner where orgId=:orgId", orgId=copy_org_id)
            for ro in role_owners:
                ro['orgId'] = to_org_id
            if len(role_owners) > 0:
                s.add_many('_role_owner', role_owners)

            # 创建页面配置
            cfg = {
                "logo": args.name,
                "desc": args.desc,
                "copyright": "",
                "beian": "",
                "shortLogo": "",
                "logoChart": ""
            }
            data = {
                'json': json.dumps(cfg),
                'orgId': org.id,
                'updateDate': datetime.now()
            }
            s.add('_sysconfig', data)
            return org, status


@ns.route('/org_delete')
class DeleteOrg(Resource):
    @auth_required
    @log_action(action='delete')
    @api.expect(dto.delete_org)
    def delete(self):
        """
        删除组织
        :return:
        """
        user = auth_user()
        args = Dict(request.json)

        with db.session() as s:
            sql = "select id from _org where id=:orgId"

            db_org = s.query_one(sql, orgId=args.id)
            if not db_org:
                return {"message": "组织不存在"}, 404

            if db_org['id'] == user.orgId:
                return {"message": "无权限删除自己所属的组织"}, 403

            res, status = dbplus.delete(user, '_org', args.id, session=s)
            if status != 200:
                return res, status

            # 删除组织管理关系
            sql = """
            delete from _org_owner where ownerOrgId=:ownerOrgId
            """
            s.execute(sql, ownerOrgId=args.id)
            # 删除菜单
            sql = """
            delete from _menu where orgId=:id
            """
            s.execute(sql, id=args.id)
            # 删除页面配置
            sql = """
            delete from _sysconfig where orgId=:id
            """
            s.execute(sql, id=args.id)

            return {'message': 'success'}, 200


def gen_role_code(name):
    return base64.b64encode(hashlib.sha1(name.encode('utf-8')).digest())[0:6].decode('utf-8')


@ns.route('/role_create')
class CreateRole(Resource):
    @auth_required
    @log_action()
    @api.expect(dto.create_role)
    def post(self):
        """
        创建角色，并把上级角色或者当前账户所有角色的功能和数据权限默认继承给下级角色
        :return:
        """
        user = auth_user()
        args = Dict(request.json)
        params = {}
        if not args.name:
            return {'message': '缺少角色名'}, 400

        if args.parentId:
            params['roleId'] = args.parentId
        if not args.code:
            args.code = gen_role_code(args.name)

        with dbplus.session() as s:
            role, status = dbplus.create(user, '_role', args, session=s)
            if status != 200:
                return role, status
            # 增加当前用户所在组织对该角色的可见权限
            db.add('_role_owner', {'roleId': role.id, 'orgId': user.orgId})

            sql = f"select distinct aclDataId from _role_acl_data where roleId=:roleId"
            if not args.parentId:
                sql = f"""select distinct {_t('aclDataId')} from _role_acl_data rd
                join _user_role ur on ur.{_t('roleId')}=rd.{_t('roleId')}
                where ur.{_t('userId')} = :userId"""
                params['userId'] = user.id

            data = [{'aclDataId': r['aclDataId'], 'roleId': role['id']} for r in db.query(sql, **params)]
            if len(data) > 0:
                db.execute_many('insert into _role_acl_data(roleId,aclDataId) values(:roleId, :aclDataId)', data,
                                session=s)

            sql = 'select distinct aclFuncId from _role_acl_func where roleId=:roleId'
            if not args.parentId:
                sql = f"""select distinct aclFuncId from _role_acl_func rf
                join _user_role ur on ur.roleId=rf.roleId
                where ur.userId = :userId"""
                params['userId'] = user.id

            data = [{'aclFuncId': r['aclFuncId'], 'roleId': role['id']} for r in db.query(sql, **params)]
            if len(data) > 0:
                db.execute_many('insert into _role_acl_func(roleId,aclFuncId) values(:roleId, :aclFuncId)', data,
                                session=s)

            sql = 'select distinct propId from _role_prop where roleId=:roleId'
            if not args.parentId:
                sql = f"""select distinct propId from _role_prop rf
                join _user_role ur on ur.roleId=rf.roleId
                where ur.userId = :userId"""
                params['userId'] = user.id

            data = [{'propId': r['propId'], 'roleId': role['id']} for r in db.query(sql, **params)]
            if len(data) > 0:
                db.execute_many('insert into _role_prop(roleId,propId) values(:roleId, :propId)', data,
                                session=s)
            return role, status


def copy_role_acl(session, change_role_id, role_id):
    # 拷贝功能权限
    sql = f"""
    insert into _role_acl_func(roleId, aclFuncId)
    select {change_role_id} as "roleId", aclFuncId from _role_acl_func f where roleId={role_id} and f.aclFuncId not in
    (select aclFuncId from _role_acl_func where roleId={change_role_id})
    """
    session.execute(sql)

    # 拷贝数据行权限
    sql = f"""
    insert into _role_acl_data(roleId, aclDataId)
    select {change_role_id} as "roleId", aclDataId from _role_acl_data where roleId={role_id} and aclDataId not in
    (select aclDataId from _role_acl_data where roleId={change_role_id})
    """
    session.execute(sql)

    # 拷贝数据列权限
    sql = f"""
    insert into _role_prop(roleId, propId)
    select {change_role_id} as "roleId", propId from _role_prop where roleId={role_id} and propId not in
    (select propId from _role_prop where roleId={change_role_id})
    """
    session.execute(sql)


def del_role_acl(session, change_role_id, role_id):
    # 删除功能权限
    sql = f"""
    select aclFuncId from _role_acl_func where roleId=:roleId
    """
    res = session.query(sql, roleId=role_id)
    func_ids = [r.aclFuncId for r in res]
    if func_ids:
        sql = "delete from _role_acl_func where roleId=:roleId and aclFuncId in :func_ids"
        session.execute(sql, roleId=change_role_id, func_ids=func_ids)

    # 删除数据行权限
    sql = "select aclDataId from _role_acl_data where roleId=:roleId"
    res = session.query(sql, roleId=role_id)
    data_ids = [r.aclDataId for r in res]
    if data_ids:
        sql = "delete from _role_acl_data where roleId=:roleId and aclDataId in :data_ids"
        session.execute(sql, roleId=change_role_id, data_ids=data_ids)

    # 删除数据列权限
    sql = "select propId from _role_prop where roleId=:roleId"
    res = session.query(sql, roleId=role_id)
    prop_ids = [r.propId for r in res]
    if prop_ids:
        sql = "delete from _role_prop where roleId=:roleId and propId in :prop_ids"
        session.execute(sql, roleId=change_role_id, prop_ids=prop_ids)


@ns.route('/role_op')
class RoleOp(Resource):
    @auth_required
    @log_action()
    @api.expect(dto.role_op)
    def post(self):
        """
        针对需要改变的角色，增加或者减少指定的角色对应的权限
        changeRole = changeRole +/- role
        :return:
        """
        user = auth_user()
        args = Dict(request.json)
        change_role_id = args.changeRoleId
        role_id = args.roleId
        if not change_role_id:
            return {'message': '缺少待改变角色ID'}, 400
        if not role_id:
            return {'message': '缺少角色ID'}, 400
        op = args.op
        if not op:
            return {'message': '缺少角色操作'}, 400
        if op not in ['plus', 'minus']:
            return {'message': '操作必须plus或者minus'}, 400

        change_role = db.query_one("select * from _role where id=:id", id=change_role_id)
        if not change_role:
            return {'message': f'待改变角色(ID={change_role_id})不存在'}, 404
        role = db.query_one("select * from _role where id=:id", id=change_role_id)
        if not role:
            return {'message': f'角色(ID={role_id})不存在'}, 404

        with dbplus.session() as s:
            check = dbplus.check_perm(user, '_role', 'updateEnabled', '更新角色权限', session=s)
            if check.status != 200:
                return check.message, check.status

            if op == 'plus':
                copy_role_acl(s, change_role_id, role_id)
            else:
                del_role_acl(s, change_role_id, role_id)


def delete_role(session, user, role_id):
    sql = 'delete from _role_acl_data where roleId=:roleId'
    db.execute(sql, roleId=role_id, session=session)
    sql = 'delete from _role_acl_func where roleId=:roleId'
    db.execute(sql, roleId=role_id, session=session)
    sql = 'delete from _user_role where roleId=:roleId'
    db.execute(sql, roleId=role_id, session=session)
    sql = 'delete from _role_prop where roleId=:roleId'
    db.execute(sql, roleId=role_id, session=session)
    sql = 'delete from _role_owner where roleId=:roleId'
    db.execute(sql, roleId=role_id, session=session)
    return dbplus.delete(user, '_role', id=role_id, session=session)


@ns.route('/role_delete/<id>')
class DeleteRole(Resource):
    @auth_required
    @log_action(action='delete')
    def delete(self, id):
        """
        删除角色，并删除与当前role的（数据权限、功能权限、用户角色、角色列权限）关联关系
        :return:
        """
        user = auth_user()

        with dbplus.session() as s:
            return delete_role(s, user, id)


logger_entry = settings.get('logger_entry',[
    "sqlalchemy.engine.base.Engine",
    "werkzeug",
    "tornado.access",
    "buildmaster.app"
])

logger_level = {
    "DEBUG": 10,
    "DEFAULT": 20,
    "INFO": 20,
    "WARNING": 30,
    "ERROR": 40,
    "OFF": 100,
}


@ns.route('/logger')
class ControlLog(Resource):
    @auth_required
    @log_action()
    @api.expect(dto.logger_control)
    def post(self):
        """
        控制日志
        :return:
        """
        u = auth_user()

        check = dbplus.check_perm_ext(u, 'configLog', '配置日志级别')
        if check.status != 200:
            return check.message, check.status

        args = Dict(request.json)
        if not args.level:
            return {'message': f'level required'}, 400
        level = args.level.upper()
        if level not in logger_level:
            return {'message': f'level({level}) invalid'}, 400

        entry = args.entry
        if entry:
            if entry not in logger_entry:
                return {'message': f'entry({entry}) invalid'}, 400
            logger = logging.getLogger(entry)
            logger.setLevel(logger_level[level])
        else:
            for e in logger_entry:
                logger = logging.getLogger(e)
                logger.setLevel(logger_level[level])

        return {"message": "success"}, 200
