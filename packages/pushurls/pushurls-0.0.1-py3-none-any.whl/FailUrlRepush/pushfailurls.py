import json
import os
import re
import sys
import time

import pymongo
from tqdm import tqdm

from FailUrlRepush.gears import printer, redis_cli


class PushFailUrls(object):
    def __init__(self, args=None):
        self.default_mos_path = self._mos_path(args, 'push_fail_urls_set.json')
        self.fromdb_collection = None
        self.fromdb_client = None
        self.fromdb = None
        self.fromdb_set = None
        self.fromdb_str = None
        self.todb_client = None
        self.to_redis_key = None
        self.condition = None
        self.tdb_str = None
        self.f_mos = None
        self.t_mos = None

    def starter(self):
        try:
            self.main_process()
        except KeyboardInterrupt:
            try:
                self.end()
            except:
                sys.exit(0)

    def main_process(self):
        self.f_mos = self._get_from_mos()
        self.t_mos = self._get_to_mos()
        self._save_mos(self.f_mos, self.t_mos)
        from_data = self.fromdb_set.find(self.condition)
        from_count = self.fromdb_set.count_documents(self.condition)
        url_head = self.f_mos.get('url_head', '')
        url_tail = self.f_mos.get('url_tail', '')
        adder_sep = self.f_mos.get('adder_sep', '>')
        in_db_urls = {x.decode() for x in self.todb_client.lrange(self.to_redis_key, 0, -1) if isinstance(x, bytes)}
        printer('start push ...')
        time.sleep(0.1)
        t = tqdm(total=from_count)
        count = 0
        for d in from_data:
            url = d.get('url')
            url_lis = [url_head, url, url_tail]
            p_url = adder_sep.join([x for x in url_lis if x])
            if p_url not in in_db_urls:
                self.todb_client.rpush(self.to_redis_key, p_url)
                count += 1
            t.update()
        t.close()
        time.sleep(0.1)
        printer('process done')
        printer(f'push done! total: [ {from_count} ], success: [ {count} ]')

    def _get_from_mos(self):
        printer('format the "from data":')
        f_md = {}
        if os.path.exists(self.default_mos_path):
            with open(self.default_mos_path, 'r') as rf:
                mos_raw = json.loads(rf.read())
            f_md = mos_raw.get('from') if mos_raw else f_md
            f_host = f_md.get('host') or input('host({}): '.format('127.0.0.1'))
            f_port = int(f_md.get('port') or input('port({}): '.format('27017')))
            f_user = f_md.get('user') or input('user({}): '.format('root'))
            f_pwd = f_md.get('password') or input('password({}): '.format('123456'))
            f_source = f_md.get('source') or input('source({}): '.format('admin'))
            self.fromdb_client = pymongo.MongoClient(self._format_uri(f_host, f_port, f_user, f_pwd, f_source))
            f_db = f_md.get('db') or self._show_dbs(db=self.fromdb_client)
            self.fromdb = self.fromdb_client[f_db]
            f_col = f_md.get('from_collection') or self._show_clos(db=self.fromdb)
            self.fromdb_collection = f_col
            self.fromdb_set = self.fromdb[self.fromdb_collection]
            con = f_md.get('condition') or self._get_filer(self.fromdb_set, self.fromdb_collection)
            self.condition = con
        else:
            f_host = input('host({}): '.format('127.0.0.1')) or '127.0.0.1'
            f_port = int(input('port({}): '.format('27017')) or '27017')
            f_user = input('user({}): '.format('root')) or 'root'
            f_pwd = input('password({}): '.format('123456')) or '123456'
            f_source = input('source({}): '.format('admin')) or 'admin'
            self.fromdb_client = pymongo.MongoClient(self._format_uri(f_host, f_port, f_user, f_pwd, f_source))
            f_db = self._show_dbs(db=self.fromdb_client)
            self.fromdb = self.fromdb_client[f_db]
            f_col = self._show_clos(db=self.fromdb)
            self.fromdb_collection = f_col
            self.fromdb_set = self.fromdb[self.fromdb_collection]
            con = self._get_filer(self.fromdb_set, self.fromdb_collection)
            self.condition = con
        self.fromdb_str = f"{f_host}.{f_db}.{f_col}"
        dic = {'host': f_host, 'port': f_port, 'user': f_user, 'password': f_pwd, 'source': f_source, 'db': f_db, 'from_collection': f_col, 'condition': con, }
        dic.update(self._get_head_tail(f_md))
        printer(f"copy data from: [ {self.fromdb_str} ]")
        return dic

    @staticmethod
    def _get_head_tail(f_md=None):
        adder_sep_str = "adder's sep（default '>', Don't enter any characters that may exist in the url）: "
        if not f_md:
            head = input("add sth to url's head: ") or ''
            tail = input("add to tail: ") or ''
            adder_sep = input(adder_sep_str) or '>'
        else:
            head = f_md.get('url_head') or input("add sth to url's head: ") or ''
            tail = f_md.get('url_tail') or input("add to tail: ") or ''
            adder_sep = f_md.get('adder_sep') or input(adder_sep_str) or '>'
        return {'url_head': head, 'url_tail': tail, 'adder_sep': adder_sep}

    def _get_to_mos(self):
        printer('push data to:')
        t_md = {}
        if os.path.exists(self.default_mos_path):
            with open(self.default_mos_path, 'r') as rf:
                mos_raw = json.loads(rf.read())
            t_md = mos_raw.get('to') or {}
            t_host = t_md.get('host') or input('host(127.0.0.1): ')
            t_port = int(t_md.get('port') or input('port(6379): '))
            t_db = int(t_md.get('db') or input('db(0): '))
        else:
            t_host = input('host(127.0.0.1): ') or '127.0.0.1'
            t_port = int(input('port(6379): ') or '6379')
            t_db = input('db(0): ') or '0'
        self.to_redis_key, new_spider_names_dic = self._ready_spider_redis_key(t_md)
        self.todb_client = redis_cli(t_host, t_port, t_db)
        self.tdb_str = f"{t_host}:{t_port}.{t_db}"
        dic = {'host': t_host, 'port': t_port, 'db': t_db, 'spiders': new_spider_names_dic}
        printer(f"push data to: [ {self.tdb_str} ]")
        return dic

    def _save_mos(self, f_dic, t_dic):
        dic = {
            'from': f_dic,
            'to': t_dic
        }
        if not os.path.exists(self.default_mos_path):
            with open(self.default_mos_path, 'w+') as wf:
                wf.write(json.dumps(dic))

    def _ready_spider_redis_key(self, t_dic=None):

        def add_new():
            add_new_tmp_n = input("Add a new spider's name: ")
            add_new_tmp_k = input("and its redis start urls' key: ")
            add_new_tmp = [add_new_tmp_n, add_new_tmp_k]
            if not any(add_new_tmp):
                printer("Wrong input!")
                raise KeyboardInterrupt
            return add_new_tmp

        if t_dic:
            name_dic = t_dic.get('spiders', {})
            new_dic = name_dic
            if name_dic:
                names = []
                keys = []
                tmp = [[names.append(k), keys.append(v)] for k, v in name_dic.items()]
                del tmp
                printer("spiders redis keys:", fill_with='*', alignment='m', msg_head_tail=['*', '*'])
                for i, name in enumerate(names):
                    printer(f"[ {i} ]: {name} >> {keys[i]}")
                printer("[ a ]: add a new one")
                printer('*', fill_with='*')
                sel = input("chose the num of the spider's name: ")
                if sel == 'a':
                    add_new_lis = add_new()
                    new_dic.update({add_new_lis[0]: add_new_lis[1]})
                    return [add_new_lis[1], new_dic]
                elif sel.isdigit() and int(sel) in [x for x in range(len(names))]:
                    return [keys[int(sel)], new_dic]
                else:
                    printer("Wrong input!")
                    raise KeyboardInterrupt
        else:
            add_new_lis = add_new()
            new_dic = {add_new_lis[0]: add_new_lis[1]}
            return [add_new_lis[1], new_dic]

    def _show_dbs(self, db):
        sel = input('db(empty to show all): ')
        if sel:
            return sel
        db_names = db.list_database_names()
        printer("database names:", fill_with='*', alignment='m', msg_head_tail=['*', '*'])
        for i, name in enumerate(db_names):
            printer(f"[ {i} ]: {name}")
        printer('*', fill_with='*')
        sel = input("chose the num of the database's name: ")
        if sel:
            return db_names[int(sel)]
        else:
            sys.exit(0)

    def _show_clos(self, db):
        sel = input('collection(empty to show all): ')
        if sel:
            return sel

        names = db.list_collection_names(include_system_collections=False)
        printer("collection names:", fill_with='*', alignment='m', msg_head_tail=['*', '*'])
        for i, name in enumerate(names):
            printer(f"[ {i} ]: {name}")
        printer('*', fill_with='*')
        sel = input("chose the num of the collection's name: ")
        sel = re.findall(r'\d+', sel)
        sel = int(sel[0]) if sel else None
        if sel not in [x for x in range(len(names))]:
            printer("Wrong input!")
            raise KeyboardInterrupt
        return names[sel]

    def _get_filer(self, db_set, collection):
        sel = input('input condition dict(empty to show all keys, or input "a" to push all urls): ')
        if sel.lower() == 'a':
            return {}
        if not sel:
            doc = db_set.find_one()
            doc = dict(doc) if doc else dict()
            keys_lis = self._get_key_path(doc)
            printer(f'keys in [ {collection} ]:', fill_with='*', alignment='m', msg_head_tail=['*', '*'])
            for i, name in enumerate(keys_lis):
                printer(f" * : {name}")
            printer('*', fill_with='*')
            sel = input("input condition dict(such as {'%s': 'condition_value'}), input 'a' to push all urls: " % keys_lis[-1])
            if sel == 'a':
                return {}
        try:
            sel = json.loads(sel)
        except:
            printer('wrong input, make sure it is a json format')
            time.sleep(1)
            return self._get_filer(db_set, collection)
        return sel

    def _get_key_path(self, dic, key_up='', sep='.'):
        """
        递归获取多层字典的所有的 key, 可以以指定的分割符组合
        :param dic:     源字典
        :param key_up:  上层键, 第一次传入是空字符
        :param sep:     上下层的键的分割符, 默认是 .
        :return:        返回键列表
        """
        se = list()
        for k, v in dic.items():
            i_k = "{}{}{}".format(key_up, sep, k) if key_up else k
            if isinstance(v, dict):
                se.extend(self._get_key_path(v, i_k, sep))
            else:
                se.append(i_k)
        return se

    @staticmethod
    def _format_uri(host, port, user, pwd, sou):
        uri = 'mongodb://{}:{}@{}:{}/{}'.format(user, pwd, host, port, sou)
        return uri

    @staticmethod
    def _mos_path(args, default=None):
        args = args or default
        return args

    def end(self):
        self.fromdb_client.close()
        self.todb_client.close()
        printer('system exits')


def rp_starter(args=None):
    args = args if args else (sys.argv[1] if len(sys.argv) > 1 else None)
    ck = PushFailUrls(args)
    ck.starter()


if __name__ == '__main__':
    RP = PushFailUrls()
    RP.starter()
