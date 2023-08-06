# -*- coding: UTF-8 -*
from __future__ import print_function

__version__ = "1.2.0"


def get_certificate(hostname, port, sername=None, timeout=None):
    import idna
    from socket import socket
    from OpenSSL import SSL

    sock = socket()
    sock.settimeout(timeout)
    sock.connect((hostname, port), )
    ctx = SSL.Context(SSL.SSLv23_METHOD)
    ctx.check_hostname = False
    ctx.verify_mode = SSL.VERIFY_NONE

    sock_ssl = SSL.Connection(ctx, sock)
    sock_ssl.set_tlsext_host_name(idna.encode(sername or hostname))
    sock_ssl.set_connect_state()
    sock_ssl.do_handshake()
    cert = sock_ssl.get_peer_certificate()
    sock_ssl.close()
    sock.close()
    return cert


_last_line = ''


def _print_status(s):
    import sys
    global _last_line
    if not sys.stdout.isatty():
        return
    if _last_line:
        print('\b' * len(_last_line), end='')
        sys.stdout.flush()
        print(' ' * len(_last_line), end='')
        sys.stdout.flush()
    print(u'\r%s' % s, end='')
    _last_line = s
    sys.stdout.flush()


def main():
    import io
    import sys
    import time
    import socket
    import argparse
    import datetime

    from collections import OrderedDict
    import ssl

    try:
        import urlparse as parse
        import urllib2
        urlopen = urllib2.urlopen
    except:
        from urllib import parse, request
        urlopen = request.urlopen

    ssl._create_default_https_context = ssl._create_unverified_context

    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('-f', '--file', help='the text file(or uri) to read URLs')
    parser.add_argument('-e', '--expire', help='the expire days for ssl certificate', type=int, default=7)
    parser.add_argument('-c', '--code', help='the http response status code', type=int, default=[200], nargs='*')
    parser.add_argument('-t', '--timeout', help='the timeout to check', type=int, default=10)
    parser.add_argument('urls', help='the URLs what will be check', default=[], type=str, nargs='*')
    args = parser.parse_args()
    start = time.time()
    rawurls = [] + args.urls
    if args.file:
        if '://' in args.file:
            # uri
            _print_status('fetch urls file from %s...' % args.file)
            r = urlopen(args.file)
            for l in r.readlines():
                if type(l) != type(''):
                    l = l.decode()
                rawurls.append(l)
        else:
            rawurls += list(io.open(args.file, encoding='utf-8').readlines())
    urls = []
    for l in rawurls:
        if '://' not in l:
            continue
        ls = l.split('#')
        if not ls:
            continue
        u = ls[0].strip()
        if not u or u in urls:
            continue
        ud = {
            'url': u
        }
        urls.append(ud)
    if not urls:
        _print_status('')
        print('no url to check', file=sys.stderr)
        exit(1)
    today = datetime.datetime.today()
    results = []
    socket.setdefaulttimeout(args.timeout)
    errct = 0
    for ix, ud in enumerate(urls):
        url = ud['url']
        _print_status(u'%s/%d/%d %s...' % (errct, ix + 1, len(urls), url))
        rs = parse.urlparse(url)
        res = OrderedDict()
        if args.expire and rs.scheme == 'https':
            # ssl check
            err = ''
            try:
                cert = get_certificate(rs.hostname, int(rs.port or 443))
                es = cert.get_notAfter()[:-1]
                if type(es) != type(''):
                    es = es.decode()
                expdate = datetime.datetime.strptime(es, '%Y%m%d%H%M%S')
                offdays = (expdate - today).days
                if offdays <= args.expire:
                    err = 'days %s' % offdays
            except Exception as e:
                err = str(e) or str(type(e).__name__)
            res['ssl'] = {
                'title': 'ssl',
                'error': err
            }
        if args.code:
            # check http status
            err = ''
            try:
                code = urlopen(url, timeout=args.timeout).getcode()
                if code not in args.code:
                    err = 'code %s' % code
            except Exception as e:
                err = str(e)
            res['http'] = {
                'title': 'http',
                'error': err
            }
        errors = list([u'%s(%s)' % (r['title'], r['error']) for r in res.values() if r['error']])
        results.append({
            'title': ud.get('title', url),
            'url': url,
            'result': res,
            'error': u'/'.join(errors) if errors else ''
        })
        if errors:
            errct += 1
    # print(results)
    _print_status('')
    errors = list(['%s [%s]' % (r['title'], r['error']) for r in results if r['error']])
    print('TIME:%ds CHECKED:%d ERROR:%s' % (int(time.time() - start), len(results), len(errors)))
    if errors:
        print('\n'.join(errors))


if __name__ == '__main__':
    main()
