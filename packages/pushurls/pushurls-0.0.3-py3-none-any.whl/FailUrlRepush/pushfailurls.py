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
        self.f_mos_lis = None
        self.t_mos = None
        self.t_mos_lis = None

    def starter(self):
        try:
            self.main_process()
        except KeyboardInterrupt:
            try:
                self.end()
            except:
                sys.exit(0)

    def main_process(self):
        self.f_mos_lis = self._get_from_mos()
        self.f_mos = self.f_mos_lis[0]
        self.t_mos_lis = self._get_to_mos()
        self.t_mos = self.t_mos_lis[0]
        self._save_mos(self.f_mos_lis, self.t_mos_lis)
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
            url_head = self._format_urls_adder(url_head, d)
            url_tail = self._format_urls_adder(url_tail, d)
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

    def _format_urls_adder(self, adder_raw, data):
        url_adder = ''
        if '**-source-**' in adder_raw:
            url_adder = adder_raw.strip('**-source-**')
            try:
                url_adder = eval('data["' + '"]["'.join(url_adder.split('.')) + '"]')
            except Exception as E:
                print(E)
                url_adder = ''
        if '**-fixed-**' in adder_raw:
            url_adder = adder_raw.strip('**-fixed-**')
        return str(url_adder)

    def _get_from_mos(self):
        printer('setting source data:', fill_with='*', alignment='m')
        if os.path.exists(self.default_mos_path):
            with open(self.default_mos_path, 'r') as rf:
                mos_raw = json.loads(rf.read())
            n_lis = self._show_fromdb_servers(mos_raw.get('from') if mos_raw else [])
        else:
            n_lis = [self._format_fromdb({})]
        return n_lis

    def _format_fromdb(self, f_dic):
        f_host = f_dic.get('host') or input('host(27.0.0.1): ') or "127.0.0.1"
        f_port = int(f_dic.get('port') or input('port(27017): ') or '27017')
        f_user = f_dic.get('user') or input('user(root): ') or "root"
        f_pwd = f_dic.get('password') or input('password(123456): ') or '123456'
        f_source = f_dic.get('source') or input('source(admin): ') or 'admin'

        self.fromdb_client = pymongo.MongoClient(self._format_uri(f_host, f_port, f_user, f_pwd, f_source))
        f_db = f_dic.get('db') or self._show_dbs(db=self.fromdb_client)
        self.fromdb = self.fromdb_client[f_db]
        f_col = f_dic.get('from_collection') or self._show_clos(db=self.fromdb)
        self.fromdb_collection = f_col
        self.fromdb_set = self.fromdb[self.fromdb_collection]
        con = f_dic.get('condition') or self._get_filer(self.fromdb_set, self.fromdb_collection)
        self.condition = con

        self.fromdb_str = f"{f_host}.{f_db}.{f_col}"
        dic = {'host': f_host, 'port': f_port, 'user': f_user, 'password': f_pwd, 'source': f_source, 'db': f_db, 'from_collection': f_col, 'condition': con, "fromdb_str": self.fromdb_str}
        dic.update(self._get_head_tail(f_dic))
        printer(f"copy data from: [ {self.fromdb_str} ]")
        return dic

    def _get_to_mos(self):
        printer('push data to:', fill_with='*', alignment='m')
        if os.path.exists(self.default_mos_path):
            with open(self.default_mos_path, 'r') as rf:
                mos_raw = json.loads(rf.read())
            n_lis = self._show_todb_servers(mos_raw.get('to') if mos_raw else [])
        else:
            n_lis = [self._format_todb({})]
        return n_lis

    def _format_todb(self, t_dic):
        t_host = t_dic.get('host') or input('host(127.0.0.1): ') or '127.0.0.1'
        t_port = int(t_dic.get('port') or input('port(6379): ') or '6379')
        t_db = int(t_dic.get('db') or input('db(0): ') or '0')

        self.to_redis_key, new_spider_names_dic = self._ready_spider_redis_key(t_dic)
        self.todb_client = redis_cli(t_host, t_port, t_db)
        self.tdb_str = f"{t_host}:{t_port}.{t_db}"
        dic = {'host': t_host, 'port': t_port, 'db': str(t_db), 'spiders': new_spider_names_dic, 'todb_str': self.tdb_str}
        printer(f"push data to: [ {self.tdb_str} ]")
        return dic

    def _show_fromdb_servers(self, f_lis):
        f_dic = {}
        n_lis = []
        if f_lis:
            printer("from servers: ")
            for i, f_dic in enumerate(f_lis):
                printer(f"[ {i} ]: {f_dic.get('fromdb_str')}")
            printer("[ n ]: add a new server")
            printer("empty to exit")
            printer(fill_with='*')
            sel = input("insert a num or a letter: ")
            if sel and sel.isdigit():
                f_dic = f_lis[int(sel)]
            elif sel:
                f_dic = {}
            else:
                raise KeyboardInterrupt

        f_dic = self._format_fromdb(f_dic=f_dic)
        n_lis.append(f_dic)
        tmp = [n_lis.append(x) for x in f_lis if x not in n_lis]
        del tmp
        n_lis = [x for x in n_lis if x]
        return n_lis

    def _show_todb_servers(self, t_lis):
        t_dic = {}
        n_lis = []
        if t_lis:
            printer("select server: ")
            for i, f_dic in enumerate(t_lis):
                printer(f"[ {i} ]: {f_dic.get('todb_str')}")
            printer("[ n ]: add a new redis server")
            printer("empty to exit")
            printer(fill_with='*')
            sel = input("insert a num or a letter: ")
            if sel and sel.isdigit():
                t_dic = t_lis[int(sel)]
            elif sel:
                t_dic = {}
            else:
                raise KeyboardInterrupt
        t_dic = self._format_todb(t_dic=t_dic)
        n_lis.append(t_dic)
        tmp = [n_lis.append(x) for x in t_lis if x not in n_lis]
        del tmp
        n_lis = [x for x in n_lis if x]
        return n_lis

    def _save_mos(self, f_lis, t_lis):
        dic = {
            'from': f_lis,
            'to': t_lis
        }
        with open(self.default_mos_path, 'w+') as wf:
            wf.write(json.dumps(dic))

    def _get_head_tail(self, f_md=None):
        adder_sep_str = "adder's sep（default '>', Don't enter any characters that may exist in the url）: "
        f_md = {} if not f_md or not isinstance(f_md, dict) else f_md
        head = f_md.get('url_head') or self._is_add_to('head')
        tail = f_md.get('url_tail') or self._is_add_to('tail')
        adder_sep = f_md.get('adder_sep') or input(adder_sep_str) or '>' if any([head, tail]) else '>'
        return {'url_head': head, 'url_tail': tail, 'adder_sep': adder_sep}

    def _is_add_to(self, HoT):
        a_str = ''
        is_add_ = input(f"add {HoT} to urls(y/empty)?: ").lower()
        if is_add_ == 'y':
            a_str = self._get_head_tail_str(HoT)
        return a_str

    def _get_head_tail_str(self, HoT):
        printer(f"add to url's {HoT}", fill_with='*', alignment='m')
        add_str = ''
        sel = input("from source data(s), or fixed characters(f)?: ").lower()
        if sel == 's':
            add_str = "**-source-**"
            printer("from which keys?: ")
            keys_lis = self._get_key_path(self.fromdb_set.find_one())
            for i, name in enumerate(keys_lis):
                printer(f" [ {i} ] : {name}")
            printer(' [ i ] : the key is not on the list above')
            printer(fill_with='*')
            k_sel = input("input a num or letter: ")
            if k_sel.lower() == 'i':
                note = """Note: Define the keys of a multi-layer dictionary by points, example: \n
                a dictionary like {"a0": {"b0": 123}}, you should input "a0.b0" to get the "b0" key."""
                printer(note, length_ctrl=False)
                c_sel = input("customize key: ")
                add_str += c_sel
            if k_sel and k_sel.isdigit() and int(k_sel) in {x for x in range(len(keys_lis))}:
                add_str += keys_lis[int(k_sel)]
        elif sel == 'f':
            add_str = input("input characters to add to all urls: ")
            if add_str:
                add_str = "**-fixed-**" + add_str

        return add_str

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
                printer("spiders redis keys:", fill_with='*', alignment='m')
                for i, name in enumerate(names):
                    printer(f"[ {i} ]: {name} >> {keys[i]}")
                printer("[ a ]: add a new one")
                printer(fill_with='*')
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
        printer("database names:", fill_with='*', alignment='m')
        for i, name in enumerate(db_names):
            printer(f"[ {i} ]: {name}")
        printer(fill_with='*')
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
        printer("collection names:", fill_with='*', alignment='m')
        for i, name in enumerate(names):
            printer(f"[ {i} ]: {name}")
        printer(fill_with='*')
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
            printer(f'keys in [ {collection} ]:', fill_with='*', alignment='m')
            for i, name in enumerate(keys_lis):
                printer(f" * : {name}")
            printer(fill_with='*')
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
