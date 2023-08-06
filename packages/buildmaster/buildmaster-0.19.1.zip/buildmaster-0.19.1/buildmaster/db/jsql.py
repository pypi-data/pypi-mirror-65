# encoding=utf8

support_ops = set(['=', '>', '<', '>=', '<=', '<>', 'like', 'is', 'in'])
support_conds = set(['and', 'or'])


class JsonSqlParser:
    def __init__(self, info, db):
        self.info = info
        self.tables = info.tables
        self.default_table = info.main_table_name()
        self.key_count = {}
        self.db = db

    def table_column(self, c):
        bb = c.split('.')
        if len(bb) > 2:
            return None, None
        if len(bb) == 1:
            table, column = self.default_table, bb[0]
        else:
            table, column = bb[0], bb[1]

        t = self.tables.get(table)
        if t is None:
            if self.info.model['sql'] and column in self.info.props:    # 模型为完整SQL的场景
                return table, column
            return None, None
        if column not in t.c:
            return None, None
        return table, column

    def simple_cond(self, params, key=None, value=None, op='='):
        if isinstance(value, (list, tuple)):
            sub_simple = True
            for sub_v in value:
                if not self.is_simple_type(sub_v):
                    sub_simple = False
                    break
            if not sub_simple:
                return

        if op not in support_ops:
            if key not in support_conds:
                return
            key = op
            op = '='

        table, column = self.table_column(key)
        if not table or not column:
            return

        if key not in self.key_count:
            self.key_count[key] = 1
            new_key = key.replace('.', '_')
        else:
            self.key_count[key] += 1
            new_key = f"{key.replace('.', '_')}_{self.key_count[key]}"

        real_key = f":{new_key}"
        if op == 'in':  # in表达式针对SQLServer特殊处理
            real_key, real_params = self.db.in_clause(new_key, value)
            params.update(real_params)
        else:
            params[new_key] = value
        return f"{self.db.escape(table)}.{self.db.escape(column)} {op} {real_key}"

    @staticmethod
    def is_simple_type(value):
        return not isinstance(value, (dict, tuple, list)) or value is None

    @staticmethod
    def cond_string(conds, rel):
        if len(conds) > 0:
            word = f" {rel} "
            if len(conds) > 1:
                return f"({word.join(conds)})"
            else:
                return f"{word.join(conds)}"

    def parse_cond(self, params, cond_json, rel='and', uplevel_key=None):
        conds = []
        if not isinstance(cond_json, dict):
            return

        for key in cond_json:
            cond = cond_json[key]
            if self.is_simple_type(cond):  # 普通类型，当前key-value视为 key=value条件
                parsed_cond = self.simple_cond(params, key=key, value=cond, op='=')
                if parsed_cond:
                    conds.append(parsed_cond)
                continue

            if isinstance(cond, (tuple, list)):
                sub_simple = True
                for sub_cond in cond:
                    if not self.is_simple_type(sub_cond):
                        sub_simple = False
                        break

                if sub_simple:
                    simple_key = uplevel_key
                    op = key
                    if simple_key is None:
                        simple_key = key
                        op = 'in'
                    parsed_cond = self.simple_cond(params, key=simple_key, value=cond, op=op)
                    if parsed_cond:
                        conds.append(parsed_cond)
                    continue

                sub_rel = key.lower()
                if sub_rel != 'or' and sub_rel != 'and':
                    continue

                sub_conds = []
                for sub_cond in cond:
                    parsed_cond = self.parse_cond(params, sub_cond, rel='and', uplevel_key=key)
                    if parsed_cond:
                        sub_conds.append(parsed_cond)
                if len(sub_conds) > 0:
                    list_cond = self.cond_string(sub_conds, sub_rel)
                    conds.append(list_cond)
                continue

            # dict
            if len(cond) == 0:
                continue
            if len(cond) > 1:
                sub_rel = key.lower()
                if sub_rel != 'and' and sub_rel != 'or':
                    continue
                parsed_cond = self.parse_cond(params, cond, rel=sub_rel, uplevel_key=key)
                if parsed_cond:
                    conds.append(parsed_cond)
                continue

            sub_key, sub_cond = None, None
            # dict with one key
            for k in cond:  # only one
                sub_key = k
                sub_cond = cond[k]
            if self.is_simple_type(sub_cond) or isinstance(sub_cond, (tuple, list)):
                parsed_cond = self.simple_cond(params, key=key, value=sub_cond, op=sub_key)
                if parsed_cond:
                    conds.append(parsed_cond)
            else:
                parsed_cond = self.parse_cond(params, sub_cond, rel, uplevel_key=sub_key)
                if parsed_cond:
                    conds.append(parsed_cond)

        if len(conds) > 0:
            word = f" {rel} "
            if len(conds) > 1:
                return f"({word.join(conds)})"
            else:
                return f"{word.join(conds)}"

    def parse_orderby(self, order_json):
        _t = self.db.escape
        if not order_json:
            return
        if not isinstance(order_json, (tuple, list)):
            order_json = [order_json]
        order_columns = []
        for order in order_json:
            if not isinstance(order, str):
                if not isinstance(order, dict):
                    continue
                if len(order) > 1:
                    continue

                for c in order:
                    dir = order[c].lower()
                    if dir != 'asc' and dir != 'desc':
                        continue
                    table, column = self.table_column(c)
                    if not table or not column:
                        continue
                    full_c = f'{_t(table)}.{_t(column)} {dir}'
                    order_columns.append(full_c)
                continue

            bb = order.split(' ')
            if len(bb) > 2:
                continue
            c = bb[0]
            dir = 'asc'
            if len(bb) > 1:
                dir = bb[1].lower()
                if dir != 'asc' and dir != 'desc':
                    continue
            table, column = self.table_column(c)
            if not table or not column:
                continue
            full_c = f'{_t(table)}.{_t(column)} {dir}'
            order_columns.append(full_c)
        return order_columns
