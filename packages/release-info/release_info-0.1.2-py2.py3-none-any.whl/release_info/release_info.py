# coding: utf-8

import sys
import os
from pathlib import Path
import datetime
from configparser import ConfigParser
import urllib.request

import hashlib
import tarfile


from _ast import *  # NOQA
from ast import parse  # NOQA

if sys.version_info >= (3, 8):
    from ast import Str, Num, Bytes, NameConstant  # NOQA

from .__init__ import version_info  # NOQA


class ReleaseInfo:
    def __init__(self):
        self._config = None
        self._config_name = 'config.ini'
        self._config_dir = None
        self._data = None

    @property
    def config(self):
        """read config file, create template if not available"""
        if self._config is not None:
            return self._config
        cp = self.config_path.expanduser()
        if not cp.exists():
            cp.write_text(_CONFIG_TEMPLATE)
        self._config = ConfigParser()
        self._config.read(cp)
        return self._config

    @property
    def config_path(self):
        # this is usually unexpanded
        return self.config_dir / self._config_name

    @config_path.setter
    def config_path(self, p):
        p = Path(p)
        if not p.expanduser().exists():
            print('config_path', p, 'does not exist')
            sys.exit(1)
        self._config_name = p.name
        self._config_dir = p.parent

    @property
    def config_dir(self):
        if self._config_dir:
            return self._config_dir
        if sys.platform.startswith('win32'):
            d = Path(os.environ['APPDATA'])
        else:
            d = Path(os.environ.get('XDG_CONFIG_HOME', '~/.config'))
        d /= 'python_release_info'
        d.expanduser().mkdir(parents=True, exist_ok=True)
        self._config_dir = d
        return d

    @property
    def data_path(self):
        return self.config_dir.expanduser() / 'release_info.pon'

    @property
    def data(self):
        if self._data is None:
            self._data = _literal_eval(self.data_path.read_text())
            nv = self._data.get('util_version', (0, 0))
            if nv > version_info:
                if nv[0] == version_info[0]:
                    print(f'a newer version ({nv} > {version_info} is '
                          'available please update')
                else:
                    print(
                        f'a newer major version ({nv} > {version_info} '
                        'is available you have to update'
                    )
            for key, ow in (('add', False), ('overwrite', True)):
                try:
                    add_path = self.config['INFO'][key]
                except KeyError:
                    add_path = None
                if add_path is not None:
                    if os.path.sep not in add_path:
                        add_path = self.config_dir.expanduser() / add_path
                    else:
                        add_path = Path(add_path).expanduser()
                    d = _literal_eval(add_path.read_text())
                    update_data(self._data, d, overwrite=ow)
        return self._data

    def check(self, type=None, args=None):
        """check loaded pon files (release_info.pon and add/overwrite file from config.ini"""
        if type is None:
            type = 'cpython' if args is None or args.type is None else args.type
        last = (0, 0)
        for major_minor, data in self.data[type].items():
            assert len(major_minor) == 2
            assert major_minor > last
            last = major_minor
            prev_date = datetime.date(1900, 1, 1)
            for k, v in data.items():
                if not isinstance(v, dict):
                    continue
                rel_date = v.get('rel', None)
                if rel_date is not None:
                    # print(k, rel_date, prev_date)
                    assert rel_date >= prev_date
                    prev_date = rel_date
        print('check: ok')

    def current(self, type=None, dd=None, pre=False):
        """return highest (major, minor, micro) for non-eol major/minor version
        pre: False -> skip , None -> include, True -> only: pre-release information
        """
        if type is None:
            type = 'cpython'
        if dd is None:
            dd = datetime.date.today()
        for major_minor, data in self.data[type].items():
            mmm = (major_minor[0], major_minor[1], -1)
            eol = None
            for k, v in data.items():
                if k == 'eol':
                    eol = v
                if isinstance(k, tuple):
                    if v['rel'] > dd:
                        continue
                    try:
                        if k > mmm:
                            mmm = k
                    except TypeError:
                        # can be None,  there was e.g. never a 2.6.0 and
                        # 2.6 is  coded as (2, 6, None)
                        mmm = k
            else:
                if eol is True:
                    eol = data[mmm]['rel']  # take eol date from last release
                # print(f'{eol=}')
                assert isinstance(eol, datetime.date)
                if len(mmm) == 3:
                    if pre is True:
                        continue
                else:
                    if pre is False:
                        continue
                if eol > dd and mmm[2] != -1:
                    yield mmm

    def print_current(self, type=None, dd=None, args=None, pre=False):
        if type is None:
            type = 'cpython' if args is None or args.type is None else args.type
        if dd is None:
            dd = (
                datetime.date.today()
                if args is None or args.dd is None
                else datetime.date.strptime(args.dd.replace('-', ''), '%Y%m%d')
            )
        for v in self.current(type=type, dd=dd, pre=pre):
            print('.'.join((str(s) for s in v)))

    def print_pre(self, type=None, dd=None, args=None):
        self.print_current(type=type, dd=dd, args=args, pre=True)

    def release_date(self, version, type='cpython'):
        data = self.data[type][version[0:2]][version]
        return data['rel']

    def src_url(self, version, type='cpython'):
        # >= 2011-02-20 -> tar.xz
        # >= 2003-10-03 -> tar.bz2
        rd = self.release_date(version)
        if rd >= datetime.date(2011, 2, 20):
            ext = 'tar.xz'
        elif rd >= datetime.date(2003, 10, 3):
            ext = 'tar.bz2'
        else:
            ext = '.tgz'
        svb = '.'.join([str(d) for d in version[:3]])
        sv = '.'.join(
            [str(version[0]), str(version[1]), "".join((str(d) for d in version[2:]))]
        )
        return f'https://www.python.org/ftp/python/{svb}/Python-{sv}.{ext}'

    def src_md5(self, version, type='cpython'):
        data = self.data[type][version[0:2]][version]
        return data.get('md5', None)

    @staticmethod
    def split_version(vs):
        version = []
        for x in vs.split('.'):
            try:
                ix = int(x)
                version.append(ix)
            except ValueError:
                while x:
                    d = ""
                    if x[0].isdigit():
                        while x and x[0].isdigit():
                            d += x[0]
                            x = x[1:]
                        version.append(int(d))
                        d = ""
                    else:
                        while x and not x[0].isdigit():
                            d += x[0]
                            x = x[1:]
                        version.append(d)
                        d = ""
        return tuple(version)

    def download(self, version=None, dir=None, type=None, extract=None, force=None, args=None):
        if version is None:
            if args is None or args.version is None:
                print('need to specify version to download')
            if args is None:
                return 1
            version = self.split_version(args.version)
        if type is None:
            type = 'cpython' if args is None or args.type is None else args.type
        if dir is None:
            dir = '.' if args is None or args.dir is None else args.dir
        if extract is None:
            extract = args.extract if args is not None else False
        if force is None:
            force = args.force if args is not None else False
        url = self.src_url(version, type=type)
        path = Path(dir) / url.rsplit('/', 1)[1]
        if not path.exists() or force:
            md5 = release_info.src_md5(version)
            with urllib.request.urlopen(url) as response:
                with path.open('wb') as fp:
                    if md5:
                        fh = hashlib.md5()
                    # 3.8 -> while chunk := response.read(16384)
                    chunk = response.read(16384)
                    while chunk:
                        if md5:
                            fh.update(chunk)
                        fp.write(chunk)
                        chunk = response.read(16384)
                if md5 and fh.hexdigest() != md5:
                    print("md5sum doesn't match for {path}")
        if extract:  # extract what is on disk, not as efficient as direct from download...
            extr_dir = Path(str(path).rsplit('.tar', 1)[0])
            if not extr_dir.exists() or force:
                tf = tarfile.open(path, 'r:*')
                tf.extractall(path=path.parent)

    def download_data(self, args=None):
        try:
            old_date = self.data['dd']
        except KeyError:
            old_date = datetime.date(2020, 1, 1)
        url = 'https://sourceforge.net/p/release-info/code/ci/default/tree/' \
            'release_info.pon?format=raw'
        dp = self.data_path.expanduser()
        tmp_file = dp.with_suffix('.pon.new')
        with urllib.request.urlopen(url) as response:
            with tmp_file.open('wb') as fp:
                chunk = response.read(16384)
                while chunk:
                    fp.write(chunk)
                    chunk = response.read(16384)
        tmp_data = _literal_eval(tmp_file.read_text())
        nv = tmp_data.get('util_version', (0, 1))
        if nv > version_info:
            if nv[0] == version_info[0]:
                print(f'a newer version ({nv} > {version_info} is available please update')
            else:
                print(f'a newer major version ({nv} > {version_info} is available')
                print(
                    f'you will have to upgrade the utility to use new data format '
                    '(and get rid of this message)'
                )
                return
        self.data_path.unlink(missing_ok=True)
        tmp_file.rename(self.data_path)
        self._data = tmp_data
        if self.data.get('dd', old_date) >= old_date:
            return 0
        return 1


release_info = ReleaseInfo()

_CONFIG_TEMPLATE = """\
[INFO]
# you can add to, or overwrite, the default release info in release_info.pon by
# specifying files here. If the filename has no dir seperator, it is assumed to "live"
# next to release_info.pon use add for information missing in release_info.pon,
# use overwrite for information that is incorrect or missing in release_info.pon
#add =
#overwrite =
"""


if sys.version_info < (3,):
    string_type = basestring
else:
    string_type = str


def _literal_eval(node_or_string):
    """
    Safely evaluate an expression node or a string containing a Python
    expression.  The string or node provided may only consist of the following
    Python literal structures: strings, bytes, numbers, tuples, lists, dicts,
    sets, booleans, integer, float, date, datetime, and None.
    You can use add/substract on nodes.
    """
    _safe_names = {'None': None, 'True': True, 'False': False}
    if isinstance(node_or_string, string_type):
        node_or_string = parse(node_or_string, mode='eval')
    if isinstance(node_or_string, Expression):
        node_or_string = node_or_string.body
    else:
        raise TypeError('only string or AST nodes supported')

    def _convert(node):
        if isinstance(node, Str):
            if sys.version_info < (3,) and not isinstance(node.s, unicode):
                return node.s.decode('utf-8')
            return node.s
        elif isinstance(node, Bytes):
            return node.s
        elif isinstance(node, Num):
            return node.n
        elif isinstance(node, Tuple):
            return tuple(map(_convert, node.elts))
        elif isinstance(node, List):
            return list(map(_convert, node.elts))
        elif isinstance(node, Set):
            return set(map(_convert, node.elts))
        elif isinstance(node, Dict):
            return dict((_convert(k), _convert(v)) for k, v in zip(node.keys, node.values))
        elif isinstance(node, NameConstant):
            return node.value
        elif sys.version_info < (3, 4) and isinstance(node, Name):
            if node.id in _safe_names:
                return _safe_names[node.id]
        elif (
            isinstance(node, UnaryOp)
            and isinstance(node.op, (UAdd, USub))
            and isinstance(node.operand, (Num, UnaryOp, BinOp))
        ):  # NOQA
            operand = _convert(node.operand)
            if isinstance(node.op, UAdd):
                return +operand
            else:
                return -operand
        elif (
            isinstance(node, BinOp)
            and isinstance(node.op, (Add, Sub))
            and isinstance(node.right, (Num, UnaryOp, BinOp))
            and isinstance(node.left, (Num, UnaryOp, BinOp))
        ):  # NOQA
            left = _convert(node.left)
            right = _convert(node.right)
            if isinstance(node.op, Add):
                return left + right
            else:
                return left - right
        elif isinstance(node, Call):
            func_id = getattr(node.func, 'id', None)
            if func_id == 'dict':
                return dict((k.arg, _convert(k.value)) for k in node.keywords)
            elif func_id == 'set':
                return set(_convert(node.args[0]))
            elif func_id == 'date':
                return datetime.date(*[_convert(k) for k in node.args])
            elif func_id == 'datetime':
                return datetime.datetime(*[_convert(k) for k in node.args])
        err = SyntaxError('malformed node or string: ' + repr(node))
        err.filename = '<string>'
        err.lineno = node.lineno
        err.offset = node.col_offset
        err.text = repr(node)
        err.node = node
        raise err

    return _convert(node_or_string)


def update_data(d1, d2, overwrite=False):
    """add data to d1 from d2, if overwrite is False, only add new leaf nodes not yet in d1"""
    if isinstance(d2, dict):
        for k in d2:
            if k not in d1:
                d1[k] = d2[k]
            else:
                if isinstance(d2[k], (dict, list)):
                    update_data(d1[k], d2[k], overwrite=overwrite)
                elif overwrite:
                    d1[k] = d2[k]
    elif isinstance(d2, list):  # only works for updating dict/list children in a list
        for idx, e in d2:
            if isinstance(d2[k], (dict, list)):
                update_data(d1[idx], d2[idx], overwrite)
