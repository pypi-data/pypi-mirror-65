# encoding=utf8
from . import _dbplus
from .xlsx import create_sheet
from .db import Dict


class DbPlus(_dbplus.DbPlus):
    def __init__(self, db):
        super(DbPlus, self).__init__(db)

    def escape(self, key):
        """
        SQL转义
        :param key:
        :return:
        """
        return self.db.escape(key)

    def session(self):
        """
        产生事务Session
        :return:
        """
        return super(DbPlus, self).session()

    def clear_cache(self):
        """
        清除缓存
        :return:
        """
        return super(DbPlus, self).clear_cache()

    def evict_cache(self, model):
        """
        根据模型清除缓存数据
        :param model:
        :return:
        """
        return super(DbPlus, self).evict_cache(model)

    def model_info(self, model, user=None, session=None):
        """
        获取模型的元数据信息
        :param model: 模型
        :param user: 登录用户
        :param session: 事务Session, 不指定则内部产生独立的Session事务
        :return:
        """
        return super(DbPlus, self).model_info(model, user=user, session=session)

    def acl_data(self, uid, model, session=None):
        """
        根据用户ID获取某个模型的数据权限
        :param uid: 用户ID
        :param model: 模型
        :param session: 事务Session, 不指定则内部产生独立的Session事务
        :return:
        """
        return super(DbPlus, self).acl_data(uid, model, session=session)

    def acl_model(self, uid, model, session=None):
        """
        【模型】根据用户ID获取某个模型的功能权限
        :param uid: 用户ID
        :param model: 模型
        :param session: 事务Session, 不指定则内部产生独立的Session事务
        :return:
        """
        return super(DbPlus, self).acl_model(uid, model, session=session)

    def acl_func(self, uid, resource_type=None, resource=None, session=None):
        """
        【通用】根据用户ID获取某个资源的功能权限
        :param uid: 用户ID
        :param resource_type: 资源类型，model|func|menu
        :param resource: 资源字符串，比如模型的名字，自定义功能的名字，菜单的URL
        :param session: 事务Session, 不指定则内部产生独立的Session事务
        :return:
        """
        return super(DbPlus, self).acl_func(uid, resource_type=resource_type, resource=resource, session=session)

    def acl_prop(self, uid, model, session=None):
        """
        根据用户获取模型的数据列级权限数据
        :param uid: 用户ID
        :param model: 模型
        :param session: 事务Session, 不指定则内部产生独立的Session事务
        :return:
        """
        return super(DbPlus, self).acl_prop(uid, model, session=session)

    def build_sql(self, user, model, args={}, extra_conds=[], extra_params={}):
        """
        从模型与登录用户生成查询SQL分解

        args示例 {
          "key": "",     #查询关键词，后台动态匹配设置了可以搜索的列
          "page": 0,     #指定从返回结果中的第几页开始显示。默认值是1。
          "limit": 0,    #指定返回结果中每页显示的记录数量，默认值10
          "doCount": 0,  #统计总数, 0–仅数据, 1/None–数据+总数, 2–仅总数
          "columns": [], #指定需要的列[prop]
          "filters": {}, #服务器端过滤{ prop: [] }
          "where": {},   #JSON条件表达式 { 'name’: 'rushmore’, 'age’: {’>’: 10 } }, 'and', 'or' 支持数组
          "joinCond": {},#关联表的条件表达式，{'_user_role': {JSON条件}}， key为关联表，用于附加JOIN条件
          "order": []    #排序, 示例['id desc']
        }

        extra_conds示例
        ['name=:name', 'age>:age']

        extra_params示例
        {'name': 'rushmore', 'age': 20 }

        :param user: 登录用户对象
        :param model: 指定的业务模型
        :param args: JSON格式参数
        :param extra_conds: SQLAlchemy key=:val 形式的参数组
        :param extra_params: extra_conds中参数指定的值
        :return: SqlResult对象 {
            'distinct': True|False #select 中是否需要用distinct
            'columns': [], #指定的列集合
            'tables': [],  #JOIN的表数组
            'conds': [],   #WHERE条件数组
            'orderby': [], #OrderBy数组
            'groupby': [], #GroupBy数组
            'params': {}   #参数Key-Value
        }
        """
        return super(DbPlus, self).build_sql(user, model, args=args, extra_conds=extra_conds, extra_params=extra_params)

    def search_one(self, user, model, args={}, extra_conds=[], extra_params={}, session=None):
        """
        根据模型和登录用户查询单条数据

        args示例 {
          "columns": [], #指定需要的列[prop]
          "where": {},   #JSON条件表达式 { 'name’: 'rushmore’, 'age’: {’>’: 10 } }, 'and', 'or' 支持数组
          "joinCond": {},#关联表的条件表达式，{'_user_role': {JSON条件}}--key为关联表，用于附加JOIN条件
        }

        extra_conds示例
        ['name=:name', 'age>:age']

        extra_params示例
        {'name': 'rushmore', 'age': 20 }

        :param user: 登录用户对象
        :param model: 指定的业务模型
        :param args: JSON格式参数
        :param extra_conds: SQLAlchemy key=:val 形式的参数组
        :param extra_params: extra_conds中参数指定的值
        :param session: 事务Session, 不指定则内部产生独立的Session事务
        :return: 单条数据对象
        """
        return super(DbPlus, self).search_one(user, model, args=args, extra_conds=extra_conds,
                                              extra_params=extra_params, session=session)

    def search_all(self, user, model, args={}, extra_conds=[], extra_params={}, session=None):
        """
        根据模型和登录用户查询所有数据，limit默认不需要，最大支持1000条数据

        args示例 {
          "key": "",     #查询关键词，后台动态匹配设置了可以搜索的列
          "columns": [], #指定需要的列[prop]
          "where": {},   #JSON条件表达式 { 'name’: 'rushmore’, 'age’: {’>’: 10 } }, 'and', 'or' 支持数组
          "joinCond": {},#关联表的条件表达式，{'_user_role': {JSON条件}}--key为关联表，用于附加JOIN条件
          "order": []    #排序, 示例[“id desc”]
        }

        extra_conds示例
        ['name=:name', 'age>:age']

        extra_params示例
        {'name': 'rushmore', 'age': 20 }

        :param user: 登录用户对象
        :param model: 指定的业务模型
        :param args: JSON格式参数
        :param extra_conds: SQLAlchemy key=:val 形式的参数组
        :param extra_params: extra_conds中参数指定的值
        :param session: 事务Session, 不指定则内部产生独立的Session事务
        :return: 分页数据
        """
        return super(DbPlus, self).search_all(user, model, args=args, extra_conds=extra_conds, extra_params=extra_params,
                                          session=session)

    def search(self, user, model, args={}, extra_conds=[], extra_params={}, session=None):
        """
        根据模型和登录用户查询数据

        args示例 {
          "key": "",     #查询关键词，后台动态匹配设置了可以搜索的列
          "page": 0,     #指定从返回结果中的第几页开始显示。默认值是1。
          "limit": 0,    #指定返回结果中每页显示的记录数量，默认值10
          "doCount": 0,  #统计总数, 0–仅数据, 1/None–数据+总数, 2–仅总数
          "columns": [], #指定需要的列[prop]
          "where": {},   #JSON条件表达式 { 'name’: 'rushmore’, 'age’: {’>’: 10 } }, 'and', 'or' 支持数组
          "joinCond": {},#关联表的条件表达式，{'_user_role': {JSON条件}}--key为关联表，用于附加JOIN条件
          "order": []    #排序, 示例[“id desc”]
        }

        extra_conds示例
        ['name=:name', 'age>:age']

        extra_params示例
        {'name': 'rushmore', 'age': 20 }

        :param user: 登录用户对象
        :param model: 指定的业务模型
        :param args: JSON格式参数
        :param extra_conds: SQLAlchemy key=:val 形式的参数组
        :param extra_params: extra_conds中参数指定的值
        :param session: 事务Session, 不指定则内部产生独立的Session事务
        :return: 分页数据
        """
        return super(DbPlus, self).search(user, model, args=args, extra_conds=extra_conds, extra_params=extra_params,
                                          session=session)

    def export(self, user, model, args={}, extra_conds=[], extra_params={}, session=None):
        """
        根据模型和登录用户查询数据

        args示例 {
          "key": "",     #查询关键词，后台动态匹配设置了可以搜索的列
          "page": 0,     #指定从返回结果中的第几页开始显示。默认值是1。
          "limit": 0,    #指定返回结果中每页显示的记录数量，默认值10
          "doCount": 0,  #统计总数, 0–仅数据, 1/None–数据+总数, 2–仅总数
          "columns": [], #指定需要的列[prop]
          "where": {},   #JSON条件表达式 { 'name’: 'rushmore’, 'age’: {’>’: 10 } }, 'and', 'or' 支持数组
          "joinCond": {},#关联表的条件表达式，{'_user_role': {JSON条件}}--key为关联表，用于附加JOIN条件
          "order": []    #排序, 示例[“id desc”]
        }

        extra_conds示例
        ['name=:name', 'age>:age']

        extra_params示例
        {'name': 'rushmore', 'age': 20 }

        :param user: 登录用户对象
        :param model: 指定的业务模型
        :param args: JSON格式参数
        :param extra_conds: SQLAlchemy key=:val 形式的参数组
        :param extra_params: extra_conds中参数指定的值
        :param session: 事务Session, 不指定则内部产生独立的Session事务
        :return: 分页数据
        """
        check = self.check_perm(user, model, 'exportEnabled', '导出')
        if check.status != 200:
            return check.message, check.status

        sql_obj, status = self.build_sql(user, model, args=args, extra_conds=extra_conds, extra_params=extra_params)
        if status != 200:
            return sql_obj, status
        if len(sql_obj.export_columns) == 0:
            return {'message': 'No column to export'}, 600

        sql = sql_obj.to_sql(export=True)

        page_size = 2000
        page = args.get('page') or 1
        data = []
        while True:
            res = self.db.query_page(sql, page=page, limit=page_size, do_count=0, **sql_obj.params, session=session)
            if len(res.data) == 0:
                break
            data.extend(res.data)
            page += 1

        info = sql_obj.metadata
        # 读取字典信息翻译
        dict_domains = [info.props[c].get('transDict') for c in info.props if info.props[c].get('transDict')]
        domains = {}
        if len(dict_domains):
            domains = self.find_dict_domains(dict_domains)

        model = info.model['displayName']
        props = sql_obj.export_props
        props.sort(key=lambda p: p.displayOrder)
        headers = [f'{p.displayName}({p.name})' for p in props]
        props_names = []
        props_name_dict = {}
        for p in props:
            name = p['name']
            if p.transObjectName and p.transColumns:  # 关联表字段，属性名字组合
                show_column = p.transColumns.split(',')[0]
                name = f"{p.transObjectName}.{show_column}"
            props_names.append(name)
            if p.transDict:
                dict_ = domains.get(p.transDict)
                if dict_:
                    props_name_dict[name] = dict_

        for row in data:  # 翻译带字典的
            for col in row:
                dict_ = props_name_dict.get(col)
                if dict_:
                    val = row[col]
                    val_ = dict_.get(f'{val}')
                    if val_:
                        row[col] = val_['label']

        path, name = create_sheet(info, model, headers, props_names, data)
        return Dict({'path': path, 'filename': name}), 200

    def query_one(self, user, model, id, session=None):
        """
        根据用户和模型以及模型数据ID查询单条数据
        :param user: 登录用户
        :param model: 指定的业务模型
        :param id: 数据主键ID
        :param session: 事务Session, 不指定则内部产生独立的Session事务
        :return:
        """
        return super(DbPlus, self).query_one(user, model, id, session=session)

    def check_perm(self, user, model, op_key, op_name='', session=None):
        """
        根据用户和模型查询某个操作是否有权限
        如果有权限返回 { 'status' : 200 其他附加信息}
        否则返回 { 'status' : 403, 'message': {} }

        :param user: 登录用户
        :param model: 指定的业务模型
        :param op_key: 操作key，示例: createEnabled, updateEnabled ...
        :param op_name: 操作名字
        :param session: 事务Session, 不指定则内部产生独立的Session事务
        :return:
        """
        return super(DbPlus, self).check_perm(user, model, op_key, op_name, session=session)

    def check_perm_ext(self, user, func, func_name='', session=None):
        """
        根据用户查询是否有权限
        如果有权限返回 { 'status' : 200 其他附加信息}
        否则返回 { 'status' : 403, 'message': {} }

        :param user: 登录用户
        :param func: 扩展功能资源名字，示例: configModel, configLog
        :param func_name: 操作名字, 示例： 配置模型，配置日志
        :param session: 事务Session, 不指定则内部产生独立的Session事务
        :return:
        """
        return super(DbPlus, self).check_perm_ext(user, func, func_name, session=session)

    def create(self, user, model, data, session=None):
        """
        创建某个模型业务记录

        :param user: 登录用户
        :param model: 指定的业务模型
        :param data: 业务数据对象
        :param session: 事务Session, 不指定则内部产生独立的Session事务
        :return:
        """
        return super(DbPlus, self).create(user, model, data, session=session)

    def create_many(self, user, model, data, session=None):
        """
        批量创建某个模型业务数据
        :param user: 登录用户
        :param model: 指定的业务模型
        :param data: 业务数据对象数组
        :param session: 事务Session, 不指定则内部产生独立的Session事务
        :return:
        """
        return super(DbPlus, self).create_many(user, model, data, session=session)

    def update(self, user, model, data, session=None):
        """
        更新某个模型业务记录，需要data中制定主键数据
        :param user: 登录用户
        :param model: 指定的业务模型
        :param data: 业务数据对象
        :param session: 事务Session, 不指定则内部产生独立的Session事务
        :return:
        """
        return super(DbPlus, self).update(user, model, data, session=session)

    def update_many(self, user, model, data, keys=None, session=None):
        """
        批量更新，验证更新功能权限，批量数据各个对应的数据权限
        :param user: 登录用户
        :param model: 指定的业务模型
        :param data: 业务数据对象数组
        :param session: 事务Session, 不指定则内部产生独立的Session事务
        :return:
        """
        _t = self.escape
        check = self.check_perm(user, model, 'updateEnabled', '更新', session=session)
        if check.status != 200:
            return check.message, check.status

        info = check.info

        if not isinstance(data, (tuple, list)):
            data = [data]

        self.normalize_update_entity_list(user, data, info)

        t = info.main_table

        self.db.update_many(t.name, data, keys=keys)
        return {'message': '批量更新成功！'}, 200

    def save_many(self, user, model, data, overwrite=True, session=None):
        """
        批量增加或更新
        :param user: 登录用户
        :param model: 指定的业务模型
        :param data: 业务数据对象数组
        :param session: 事务Session, 不指定则内部产生独立的Session事务
        :return:
        """
        _t = self.escape
        check = self.check_perm(user, model, 'updateEnabled', '更新', session=session)
        if check.status != 200:
            return check.message, check.status
        check = self.check_perm(user, model, 'createEnabled', '创建', session=session)
        if check.status != 200:
            return check.message, check.status

        info = check.info

        if not isinstance(data, (tuple, list)):
            data = [data]

        self.normalize_create_entity_list(user, data, info)
        self.normalize_update_entity_list(user, data, info)

        t = info.main_table

        self.db.save_many(t.name, data, overwrite=overwrite)
        return {'message': '批量保存成功！'}, 200

    def delete(self, user, model, id, session=None):
        """
        根据用户和模型和主键id删除记录
        :param user: 登录用户
        :param model: 指定的业务模型
        :param id: 业务数据记录主键Id
        :param session: 事务Session, 不指定则内部产生独立的Session事务
        :return:
        """
        return super(DbPlus, self).delete(user, model, id, session=session)

    def relation_update(self, user, relation_model, add_data=None, del_data=None, session=None):
        """
        根据用户与关联模型更新关联数据（增加或者删除）
        :param user: 登录用户
        :param relation_model: 关联模型
        :param add_data: 增加的关联记录数据
        :param del_data: 删除的关联记录数据
        :param session: 事务Session, 不指定则内部产生独立的Session事务
        :return:
        """
        return super(DbPlus, self).relation_update(user, relation_model,
                                                   add_data=add_data, del_data=del_data, session=session)

    def sync_model(self, model, session=None):
        """
        同步模型元数据
        :param model: 业务模型名字
        :param session: 事务Session, 不指定则内部产生独立的Session事务
        :return:
        """
        return super(DbPlus, self).sync_model(model, session=session)

    def copy_model(self, user, from_model, to_model, display_name=None, copy_acl=True, session=None):
        """
        拷贝模型，包括模型的资源数据，授权数据
        :param user: 登录用户
        :param from_model: 拷贝的源模型名字
        :param to_model: 目标模型名字
        :param display_name: 目标模型的显示名
        :param copy_acl: 是否拷贝授权数据
        :param session:
        :return:
        """
        m = self.db.query_one('select * from _model where model=:model', model=from_model, session=session)
        if not m:
            return {'message': f'Model({from_model}) not found'}, 404
        m.id = None
        m['model'] = to_model
        if display_name:
            m['displayName'] = display_name
        res, status = self.create(user, '_model', m, session=session)
        if status != 200:
            return res, status

        # 拷贝属性
        props = self.db.query('select * from _prop where model=:model', model=from_model, session=session)
        for p in props:
            p.id = None
            p['model'] = to_model
        self.db.add_many('_prop', props, session=session)
        # 拷贝关联表
        link_tables = self.db.query('select * from _model_table where model=:model', model=from_model, session=session)
        for t in link_tables:
            del t.id
            t.model = to_model
        if link_tables:
            self.db.add_many('_model_table', link_tables, session=session)

        # 拷贝数据权限
        link_acl_data = self.db.query('select * from _acl_data where model=:model', model=from_model, session=session)
        for t in link_acl_data:
            del t.id
            t.model = to_model
        if link_acl_data:
            self.db.add_many('_acl_data', link_acl_data, session=session)

        # 拷贝联动模型
        link_models = self.db.query('select * from _model_relation where model=:model', model=from_model, session=session)
        for t in link_models:
            del t.id
            t.model = to_model
        if link_models:
            self.db.add_many('_model_relation', link_models, session=session)

        # 创建资源信息
        old_res = self.db.query_one(f"select * from _resource where resource=:model and type='model'",
                               model=from_model, session=session)
        if not old_res:
            return None, 200  # no need to copy resource

        resource = {
            'name': display_name or m.displayName,
            'resource': to_model,
            'type': 'model',
            'module': m.module
        }
        new_res, status = self.create(user, '_resource', resource, session=session)
        if status != 200:
            return new_res, status

        sql = 'select * from _acl_func where resourceId=:id order by funcKey'
        func_list = self.db.query(sql, id=old_res['id'], session=session)
        func_id_mapping = {}
        for r in func_list:
            func = {'resourceId': new_res['id'], 'funcKey': r['funcKey']}
            new_func = self.db.add('_acl_func', func, session=session)
            func_id_mapping[r['id']] = new_func['id']

        if not copy_acl:
            return None, 200

        # 拷贝权限控制信息
        sql = """
            select rf.roleId, rf.aclFuncId from _role_acl_func rf
            join _acl_func f on rf.aclFuncId=f.id
            join _resource r on f.resourceId=r.id
            where r.resource=:model and r.type='model'
        """
        role_func_list = self.db.query(sql, model=from_model, session=session)
        new_role_func_list = []
        for r in role_func_list:
            new_r = {
                'roleId': r['roleId'],
                'aclFuncId': func_id_mapping[r['aclFuncId']]
            }
            new_role_func_list.append(new_r)
        self.db.add_many('_role_acl_func', new_role_func_list, session=session)
        return None, 200

    def delete_model(self, user, model, session=None):
        """
        删除模型相关的所有数据

        1）模型本身，
        2）属性，
        3）关联表，
        4）资源，
        5）数据权限（行）定义，
        6）数据权限（行）授权，
        7）功能权限定义，
        8）功能权限授权，
        9）数据权限（列）授权
        10）联动模型

        :param user:
        :param model:
        :param session:
        :return:
        """
        if session is None:
            with self.session() as s:
                return self._delete_model(user, model, s)
        else:
            return self._delete_model(user, model, session)

    def _delete_model(self, user, model, s):
        m = s.query_one(f"select id from _model where model=:model", model=model)
        if not m:
            return {'message': f"Model({model}) not found"}, 404

        res = self.check_perm(user, '_model', 'deleteEnabled', '删除模型', session=s)
        if res.status != 200:
            return res.message, res.status

        # 数据权限（列）授权
        sql = f"""
        DELETE _role_prop FROM _role_prop 
        JOIN _prop p on _role_prop.propId = p.id
        JOIN _model m ON p.model=:model
        """
        s.execute(sql, model=model)

        # 功能权限授权
        sql = f"""
        delete rf from _role_acl_func rf
        join _acl_func f on rf.aclFuncId=f.id
        join _resource s on f.resourceId=s.id
        where s.type='model' and s.resource=:model
        """
        s.execute(sql, model=model)

        # 功能权限定义
        sql = f"""
        delete f from _acl_func f join _resource s on f.resourceId=s.id
        where s.type='model' and s.resource=:model
        """
        s.execute(sql, model=model)

        # 数据权限（行）授权
        sql = f"""
        delete rd from _role_acl_data rd 
        join _acl_data d on rd.aclDataId=d.id 
        where d.model=:model
        """
        s.execute(sql, model=model)

        # 数据权限（行）定义
        sql = f"""
        delete from _acl_data where model=:model
        """
        s.execute(sql, model=model)

        # 清理资源
        sql = f"""
        delete s from _resource s where s.type='model' and s.resource=:model
        """
        s.execute(sql, model=model)

        # 清理关联表
        s.execute(f"delete from _model_table where model=:model", model=model)

        # 清理属性
        s.execute(f"delete from _prop where model=:model", model=model)

        # 联动模型
        s.execute(f"delete from _model_relation where model=:model or linkModel=:model", model=model)

        # 最后删除模型本身
        s.execute(f"delete from _model where model=:model", model=model)

        return None, 200

    def delete_module(self, user, module, session=None):
        """
        删除模块相关的所有数据
        比删除模块多增加了删除模块的字典数据
        :param user:
        :param module:
        :param session:
        :return:
        """
        if session is None:
            with self.session() as s:
                return self._delete_module(user, module, s)
        else:
            return self._delete_module(user, module, session)

    def _delete_module(self, user, module, s):
        m = s.query_one(f"select * from _module where name=:name", name=module)
        if not m:
            return {'message': f'Module({module}) Not Found'}, 404
        res = self.check_perm(user, '_module', 'deleteEnabled', '删除模块', session=s)
        if res.status != 200:
            return res.message, res.status

        # 数据权限（列）授权 _role_prop
        sql = f"""
        DELETE _role_prop FROM _role_prop 
        JOIN _prop p on _role_prop.propId = p.id
        JOIN _model m ON p.model = m.model
        WHERE m.module=:module
        """
        s.execute(sql, module=module)

        # 列属性(_prop)
        sql = f"""
        DELETE p FROM _prop p JOIN _model m ON p.model = m.model
        WHERE m.module=:module
        """
        s.execute(sql, module=module)

        # 功能权限授权 _role_acl_func
        sql = f"""
        delete rf from _role_acl_func rf
        join _acl_func f on rf.aclFuncId=f.id
        join _resource s on f.resourceId=s.id
        where s.module=:module
        """
        s.execute(sql, module=module)

        # 功能权限定义 _acl_func
        sql = f"""
        delete f from _acl_func f join _resource s on f.resourceId=s.id
        where s.module=:module
        """
        s.execute(sql, module=module)

        # 数据权限（行）授权_role_acl_data
        sql = f"""
        delete rd from _role_acl_data rd 
        join _acl_data d on rd.aclDataId=d.id 
        join _model m on d.model=m.model where m.module=:module
        """
        s.execute(sql, module=module)

        # 数据权限（行）定义 _acl_data
        sql = f"""
        delete d from _acl_data d join _model m on d.model=m.model 
        where m.module=:module
        """
        s.execute(sql, module=module)

        # 资源定义 _resource
        sql = f"""
        delete s from _resource s where s.module=:module
        """
        s.execute(sql, module=module)

        # 模型关联表 _model_table
        sql = f"""
        delete mt from _model_table mt left join _model m on mt.model=m.model where m.module=:module
        """
        s.execute(sql, module=module)

        # 字典 _dict
        sql = f"""
        DELETE FROM _dict WHERE module=:module
        """
        s.execute(sql, module=module)

        # 序列发生器 _seq
        sql = f"""
        delete sv from _seq_value sv join _seq s on s.id = sv.seqId where module=:module
        """
        s.execute(sql, module=module)
        sql = f"""
        DELETE FROM _seq WHERE module=:module
        """
        s.execute(sql, module=module)

        # 联动模型
        sql = f"""
        delete mr from _model_relation mr join _model m
        on mr.model=m.model or mr.linkModel=m.model
        where m.module=:module
        """
        s.execute(sql, module=module)

        # 模型 _model
        sql = f"""
        DELETE _model FROM _model WHERE _model.module=:module
        """
        s.execute(sql, module=module)

        sql = f"""
        DELETE _module FROM _module WHERE name=:module
        """
        s.execute(sql, module=module)

        return None, 200

    @staticmethod
    def _clear_id(arr):
        for item in arr:
            item.pop('id', None)
        return arr

    def export_module(self, module):
        """模块导出"""
        res = {
            'name': module,
            'displayName': '',
            'roles': '',

            '_model': [],
            '_model_table': [],
            '_model_relation': [],
            '_prop': [],
            '_dict': [],
            '_seq': [],
            '_resource': [],
            '_acl_data': [],
            '_role_prop': [],
            '_role_acl_func': [],
            '_role_acl_data': []
        }

        module_obj = self.db.query_one("select * from _module where name=:name", name=module)
        if not module_obj:
            return {'message': f'{module} not found'}, 404
        res['displayName'] = module_obj.displayName

        # 模型本身 _model
        models = self.db.query(f"select * from _model where module=:module", module=module)
        res['_model'] = self._clear_id(models)

        # 模型属性 _prop
        sql = f"select p.* from _prop p join _model m on p.model=m.model where m.module=:module"
        props = self.db.query(sql, module=module)
        res['_prop'] = self._clear_id(props)

        # 关联表 _model_table
        sql = f"""
        select mt.* from _model_table mt
        join _model m on mt.model = m.model
        where m.module=:module
        """
        model_tables = self.db.query(sql, module=module)
        res['_model_table'] = self._clear_id(model_tables)

        # 联动模型 _model_relation
        sql = f"""
        select mr.* from _model_relation mr
        join _model m on mr.model = m.model
        where m.module=:module
        """
        model_relations = self.db.query(sql, module=module)
        res['_model_relation'] = self._clear_id(model_relations)

        # 资源 _resource
        resources = self.db.query(f"select * from _resource where module=:module", module=module)
        res['_resource'] = self._clear_id(resources)

        # 功能权限定义 _acl_func
        sql = f"""
        select r.resource, r.type, f.funcKey from _acl_func f join _resource r on f.resourceId=r.id
        where r.module=:module
        """
        acl_func = self.db.query(sql, module=module)
        res['_acl_func'] = acl_func

        # 数据权限定义 _acl_data
        sql = f"""
        select d.* from _acl_data d join _model m on d.model=m.model where m.module=:module
        """
        acl_data = self.db.query(sql, module=module)
        for r in acl_data:  # orgId信息不导出
            r.pop('orgId', None)
        res['_acl_data'] = self._clear_id(acl_data)

        # 字典 _dict
        dict_array = self.db.query(f"select * from _dict where module=:module", module=module)
        res['_dict'] = self._clear_id(dict_array)

        # 序列发生器 _seq
        seq_array = self.db.query(f"select * from _seq where module=:module", module=module)
        res['_seq'] = self._clear_id(seq_array)

        # 授权数据 _role_prop
        sql = f"""
        select p.model, p.name, rp.roleId, rp.mask from _prop p join _role_prop rp on p.id=rp.propId 
        join _model m on m.model=p.model 
        where m.module=:module
        """
        role_props = self.db.query(sql, module=module)
        res['_role_prop'] = role_props

        # 授权数据 _role_acl_func
        sql = f"""
        select r.type, r.resource, f.funcKey, rf.roleId from _acl_func f join _resource r on f.resourceId=r.id
        join _role_acl_func rf on f.id=rf.aclFuncId
        where r.module=:module
        """
        role_funcs = self.db.query(sql, module=module)
        res['_role_acl_func'] = role_funcs

        # 授权数据 _role_acl_data
        sql = f"""
        select d.model, d.name, rd.roleId from _acl_data d join _role_acl_data rd on d.id=rd.aclDataId
        join _model m on d.model = m.model
        where m.module=:module
        """
        role_data = self.db.query(sql, module=module)
        res['_role_acl_data'] = self._clear_id(role_data)

        related_roles = set()
        for r in role_props:
            related_roles.add(r['roleId'])
        for r in role_funcs:
            related_roles.add(r['roleId'])
        for r in role_data:
            related_roles.add(r['roleId'])
        if len(related_roles) > 0:
            res['roles'] = self.db.query("select * from _role where id in :ids", ids=related_roles)

        return res

    def import_module(self, user, data):
        """
        导入模块
        :param user:
        :param data:
        :return:
        """
        with self.session() as s:
            module = data['name']
            db_module = self.db.query_one(f"select * from _module where name=:name", name=module, session=s)
            if not db_module:
                res, status = self.create(user, '_module',
                                          {'name': module, 'displayName': data['displayName']}, session=s)
                if status != 200:
                    return res, status

            self._batch_import_model(user, module, data['_model'], s)
            self._batch_import_prop(module, data['_prop'], s)
            self._batch_import_model_table(module, data['_model_table'], s)
            self._batch_import_model_relation(module, data['_model_relation'], s)
            self._batch_import_dict(module, data['_dict'], s)
            self._batch_import_seq(module, data['_seq'], s)
            self._batch_import_resource(module, data['_resource'], s)
            self._batch_import_acl_func(module, data['_acl_func'], s)
            self._batch_import_acl_data(module, data['_acl_data'], s)

            # 导入授权数据
            role_mapping = self._load_role_mapping(data['roles'])
            if len(role_mapping) == 0:
                return
            self._batch_import_role_prop(module, data['_role_prop'], role_mapping, s)
            self._batch_import_role_acl_func(module, data['_role_acl_func'], role_mapping, s)
            self._batch_import_role_acl_data(module, data['_role_acl_data'], role_mapping, s)

    def _batch_import_model(self, user, module, new_data, sess):
        sql = f"""
        select * from _model where module=:module
        """
        old_data = self.db.query(sql, module=module, session=sess)
        keys = ['model']
        to_delete, _ = self._array_minus(old_data, new_data, keys=keys)
        to_add, to_update = self._array_minus(new_data, old_data, keys=keys)
        for r in to_delete:     # 删除掉模型，需要复杂的删除掉所有的依赖
            self._delete_model(user, r['model'], sess)

        if len(to_update) > 0:
            self.db.update_many('_model', to_update, keys=keys, session=sess)

        if len(to_add) > 0:
            for item in to_add:
                item.pop('id', None)
            self.db.add_many('_model', to_add, session=sess)

    def _batch_import_prop(self, module, new_data, sess):
        sql = f"""
        select p.* from _prop p join _model m on p.model=m.model where m.module=:module
        """
        old_data = self.db.query(sql, module=module, session=sess)
        keys = ['name', 'model']
        to_delete, _ = self._array_minus(old_data, new_data, keys=keys)
        to_add, to_update = self._array_minus(new_data, old_data, keys=keys)
        delete_ids = [r['id'] for r in to_delete]

        # 删除数据权限（列）授权数据
        if len(delete_ids) > 0:
            sql = f"""
            delete rp from _role_prop rp join _prop p on rp.propId=p.id
            where p.id in :ids
            """
            self.db.execute(sql, ids=delete_ids, session=sess)

        if len(delete_ids) > 0:
            self.db.execute(f"delete from _prop where id in :ids", ids=delete_ids, session=sess)

        if len(to_update) > 0:
            self.db.update_many('_prop', to_update, keys=keys, session=sess)

        if len(to_add) > 0:
            for item in to_add:
                item.pop('id', None)
            self.db.add_many('_prop', to_add, session=sess)

    def _batch_import_model_table(self, module, new_data, sess):
        sql = f"""
        select mt.* from _model_table mt join _model m on mt.model=m.model and m.module=:module
        """
        old_data = self.db.query(sql, module=module, session=sess)
        self._batch_import('_model_table', ['model', 'table'], new_data, old_data, sess)

    def _batch_import_model_relation(self, module, new_data, sess):
        sql = f"""
        select mr.* from _model_relation mr join _model m on mr.model=m.model and m.module=:module
        """
        old_data = self.db.query(sql, module=module, session=sess)
        self._batch_import('_model_relation', ['model', 'linkModel'], new_data, old_data, sess)

    def _batch_import_dict(self, module, new_data, sess):
        sql = f"""
        select * from _dict where module=:module
        """
        old_data = self.db.query(sql, module=module, session=sess)
        self._batch_import('_dict', ['domain', 'key', 'module'], new_data, old_data, sess)

    def _batch_import_seq(self, module, new_data, sess):
        sql = f"""
        select * from _seq where module=:module
        """
        old_data = self.db.query(sql, module=module, session=sess)
        self._batch_import('_seq', ['name', 'module'], new_data, old_data, sess)

    def _batch_import_resource(self, module, new_data, sess):
        sql = f"""
        select * from _resource r where r.module=:module
        """
        old_data = self.db.query(sql, module=module, session=sess)
        keys = ['resource', 'type']
        to_delete, _ = self._array_minus(old_data, new_data, keys=keys)
        to_add, to_update = self._array_minus(new_data, old_data, keys=keys)

        delete_ids = [r['id'] for r in to_delete]
        if len(delete_ids) > 0:
            # 删除对应资源的功能权限授权
            sql = f"""
            delete rf from _acl_func f join _resource r on f.resourceId=r.id
            join _role_acl_func rf on rf.aclFuncId=f.id
            where r.id in :resourceIds
            """
            self.db.execute(sql, resourceIds=delete_ids, session=sess)

            # 删除对应资源的功能定义
            sql = f"""
            delete f from _acl_func f join _resource r on f.resourceId=r.id
            where r.id in :resourceIds
            """
            self.db.execute(sql, resourceIds=delete_ids, session=sess)

        self._batch_execute('_resource', keys, to_delete, to_add, to_update, sess)

    def _batch_import_acl_func(self, module, new_data, sess):
        sql = f"""
        select f.*, r.resource, r.type from _acl_func f 
        join _resource r on f.resourceId=r.id and r.module=:module
        """
        old_data = self.db.query(sql, module=module, session=sess)
        keys = ['resource', 'type', 'funcKey']
        to_delete, _ = self._array_minus(old_data, new_data, keys=keys)
        to_add, to_update = self._array_minus(new_data, old_data, keys=keys)
        delete_ids = [r['id'] for r in to_delete]

        # 删除功能权限授权数据
        if len(delete_ids) > 0:
            sql = f"""
            delete rf from _acl_func f join _role_acl_func rf on rf.aclFuncId=f.id
            where f.id in :ids
            """
            self.db.execute(sql, ids=delete_ids, session=sess)

        if len(delete_ids) > 0:
            self.db.execute(f"delete from _acl_func where id in :ids", ids=delete_ids, session=sess)

        if len(to_update) > 0:
            pass
            # 暂时只有funcKey，没有其他字段，不需要更新
            # to_update = self._query_resource_id(to_update, module)
            # if len(to_update) > 0:
            #    self.db.update_many('_acl_func', to_update, keys=['resourceId', 'funcKey'], session=sess)

        if len(to_add) > 0:
            for item in to_add:
                item.pop('id', None)
            to_add = self._query_resource_id(to_add, module, sess)
            if to_add:
                self.db.add_many('_acl_func', to_add, session=sess)

    def _batch_import_acl_data(self, module, new_data, sess):
        sql = f"""
        select d.* from _acl_data d join _model m on d.model=m.model and m.module=:module
        """
        old_data = self.db.query(sql, module=module, session=sess)
        keys = ['model', 'name']
        to_delete, _ = self._array_minus(old_data, new_data, keys=keys)
        to_add, to_update = self._array_minus(new_data, old_data, keys=keys)
        delete_ids = [r['id'] for r in to_delete]

        # 删除数据权限授权数据
        if len(delete_ids) > 0:
            sql = f"""
            delete rd from _role_acl_data rd join _acl_data d on rd.aclDataId=d.id
            where d.id in :ids
            """
            self.db.execute(sql, ids=delete_ids, session=sess)

        if len(delete_ids) > 0:
            self.db.execute(f"delete from _acl_data where id in :ids", ids=delete_ids, session=sess)

        if len(to_update) > 0:
            self.db.update_many('_acl_data', to_update, keys=keys, session=sess)

        if len(to_add) > 0:
            for item in to_add:
                item.pop('id', None)
            self.db.add_many('_acl_data', to_add, session=sess)

    def _load_role_mapping(self, from_roles):
        if len(from_roles) == 0:
            return {}

        role_codes = [r['code'] for r in from_roles]
        db_roles = self.db.query('select * from _role where code in :codes', codes=role_codes)
        db_roles = {r.code: r.id for r in db_roles}

        checked_mapping = {r['id']: db_roles[r['code']] for r in from_roles if r['code'] in db_roles}
        return checked_mapping

    def _query_resource_id(self, records, module, sess):
        res = []
        for r in records:  # TODO 如何批量完成资源ID获取
            sql = f"""
            select * from _resource where resource=:resource and type=:type and module=:module
            """
            resource = self.db.query_one(sql, resource=r['resource'], type=r['type'], module=module, session=sess)
            if resource:
                r['resourceId'] = resource['id']
                res.append(r)
        return res

    def _query_prop_id(self, records, module, sess):
        res = []
        for r in records:  # TODO 如何批量完成
            sql = f"""
            select p.* from _prop p join _model m on p.model=m.model
            where p.model=:model and p.name=:name and m.module=:module
            """
            p = self.db.query_one(sql, model=r['model'], name=r['name'], module=module, session=sess)
            if p:
                r['propId'] = p['id']
                res.append(r)
        return res

    def _query_acl_func_id(self, records, module, sess):
        res = []
        for r in records:  # TODO 如何批量完成
            sql = f"""
            select f.* from _acl_func f join _resource r on f.resourceId=r.id
            where r.resource=:resource and r.type=:type and f.funcKey=:funcKey and r.module=:module
            """
            f = self.db.query_one(sql, resource=r['resource'],
                                  type=r['type'], funcKey=r['funcKey'], module=module, session=sess)
            if f:
                r['aclFuncId'] = f['id']
                res.append(r)
        return res

    def _query_acl_data_id(self, records, module, sess):
        res = []
        for r in records:  # TODO 如何批量完成
            sql = f"""
            select d.* from _acl_data d join _model m on d.model=m.model
            where d.model=:model and d.name=:name and m.module=:module
            """
            d = self.db.query_one(sql, model=r['model'], name=r['name'], module=module, session=sess)
            if d:
                r['aclDataId'] = d['id']
                res.append(r)
        return res

    def _batch_import_role_prop(self, module, new_data, role_mapping, sess):
        roles_affected = [role_mapping[r] for r in role_mapping]    # 只处理受到影响的角色
        new_data = self._query_prop_id(new_data, module, sess)
        new_data_affected = []  # 原系统不存在的角色的新数据忽略掉
        for r in new_data:
            mapped_role = role_mapping.get(r['roleId'])
            if mapped_role:
                r['roleId'] = mapped_role
                new_data_affected.append(r)
        new_data = new_data_affected

        sql = f"""
        select rp.* from _role_prop rp join _prop p on rp.propId = p.id
        join _model m on p.model=m.model and m.module=:module
        where rp.roleId in :roleIds
        """
        old_data = self.db.query(sql, roleIds=roles_affected, module=module, session=sess)
        keys = ['roleId', 'propId']
        to_delete, _ = self._array_minus(old_data, new_data, keys=keys)
        to_add, to_update = self._array_minus(new_data, old_data, keys=keys)

        if len(to_delete) > 0:
            self.db.execute_many(f"delete from _role_prop where roleId=:roleId and propId=:propId", to_delete, session=sess)

        if len(to_update) > 0:
            self.db.update_many('_role_prop', to_update, keys=keys, session=sess)

        if len(to_add) > 0:
            for item in to_add:
                item.pop('id', None)
            self.db.add_many('_role_prop', to_add, session=sess)

    def _batch_import_role_acl_func(self, module, new_data, role_mapping, sess):
        roles_affected = [role_mapping[r] for r in role_mapping]    # 只处理受到影响的角色
        new_data = self._query_acl_func_id(new_data, module, sess)
        new_data_affected = []  # 原系统不存在的角色的新数据忽略掉
        for r in new_data:
            mapped_role = role_mapping.get(r['roleId'])
            if mapped_role:
                r['roleId'] = mapped_role
                new_data_affected.append(r)
        new_data = new_data_affected

        sql = f"""
        select rf.* from _role_acl_func rf join _acl_func f on rf.aclFuncId=f.id
        join _resource r on r.id=f.resourceId and r.module=:module
        where rf.roleId in :roleIds
        """
        old_data = self.db.query(sql, roleIds=roles_affected, module=module, session=sess)
        keys = ['roleId', 'aclFuncId']
        to_delete, _ = self._array_minus(old_data, new_data, keys=keys)
        to_add, to_update = self._array_minus(new_data, old_data, keys=keys)

        if len(to_delete) > 0:
            self.db.execute_many(f"delete from _role_acl_func where roleId=:roleId and aclFuncId=:aclFuncId",
                                 to_delete, session=sess)

        if len(to_update) > 0:
            pass    # 关联表无其他需要更新字段
            # self.db.update_many('_role_prop', to_update, keys=keys, session=sess)

        if len(to_add) > 0:
            for item in to_add:
                item.pop('id', None)
            self.db.add_many('_role_acl_func', to_add, session=sess)

    def _batch_import_role_acl_data(self, module, new_data, role_mapping, sess):
        roles_affected = [role_mapping[r] for r in role_mapping]    # 只处理受到影响的角色
        new_data = self._query_acl_data_id(new_data, module, sess)
        new_data_affected = []  # 原系统不存在的角色的新数据忽略掉
        for r in new_data:
            mapped_role = role_mapping.get(r['roleId'])
            if mapped_role:
                r['roleId'] = mapped_role
                new_data_affected.append(r)
        new_data = new_data_affected

        sql = f"""
        select rd.* from _role_acl_data rd join _acl_data d on rd.aclDataId=d.id
        join _model m on d.model=m.model and m.module=:module and rd.roleId in :roleIds
        """
        old_data = self.db.query(sql, roleIds=roles_affected, module=module, session=sess)
        keys = ['roleId', 'aclDataId']
        to_delete, _ = self._array_minus(old_data, new_data, keys=keys)
        to_add, to_update = self._array_minus(new_data, old_data, keys=keys)

        if len(to_delete) > 0:
            self.db.execute_many(f"delete from _role_acl_data where roleId=:roleId and aclDataId=:aclDataId",
                                 to_delete, session=sess)

        if len(to_update) > 0:
            pass    # 关联中间无需更新
            # self.db.update_many('_role_acl_data', to_update, keys=keys, session=sess)

        if len(to_add) > 0:
            for item in to_add:
                item.pop('id', None)
            self.db.add_many('_role_acl_data', to_add, session=sess)

    def _array_minus(self, data, compared_data, keys):
        diff = []
        same = []
        for item in data:
            exists = False
            for compared_item in compared_data:
                equal = True
                for key in keys:
                    if item[key] != compared_item[key]:
                        equal = False
                        break
                if equal:
                    exists = True
            if exists:
                same.append(item)
            else:
                diff.append(item)
        return diff, same

    def _batch_import(self, table, keys, new_data, old_data, sess):
        to_delete, _ = self._array_minus(old_data, new_data, keys)
        to_add, to_update = self._array_minus(new_data, old_data, keys)

        self._batch_execute(table, keys, to_delete, to_add, to_update, sess)

    def _batch_execute(self, table, keys, to_delete, to_add, to_update, sess):
        ids = [r['id'] for r in to_delete]
        if len(ids) > 0:
            self.db.execute(f"delete from {table} where id in :ids", ids=ids, session=sess)

        if len(to_update) > 0:
            self.db.update_many(table, to_update, keys=keys, session=sess)

        if len(to_add) > 0:
            for item in to_add:
                item.pop('id', None)
            self.db.add_many(table, to_add, session=sess)
