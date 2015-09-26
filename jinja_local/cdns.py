import flask
import os
import sys
import urlparse
import urllib2
import argparse

from flask import url_for


class CDNSpec():
    use_min = False

    def __init__(self, urlBase, version=None, hasMin=True, subdir='js'):
        self.urlBase = urlBase
        self.hasMin = hasMin
        self.version = version
        self.subdir = subdir

    def url(self, file_name, use_static=False, version=None):
        if not version:
            version = self.version
        if self.use_min and self.hasMin:
            file_basename, extension = os.path.splitext(file_name)
            if extension == '.js':
                file_name = file_basename + '.min' + extension

        url = os.path.join(self.urlBase, file_name)
        oo = urlparse.urlparse(url)
        if oo.scheme == 'file':
            url = url_for('static', filename=oo.path[1:])
        elif use_static:
            url = url_for('static', filename=os.path.join(self.subdir, file_name))

        return url.format(version=version or '')


# note that file: schema items have 3 / because the netloc is empty
cdns = {
    'jquery.js': CDNSpec('//ajax.googleapis.com/ajax/libs/jquery/{version}/', version='1.11.2'),
    'jquery-ui.js': CDNSpec('//cdnjs.cloudflare.com/ajax/libs/jqueryui/{version}/', version='1.11.2'),

    'bootstrap.js': CDNSpec('//netdna.bootstrapcdn.com/bootstrap/{version}/js/', version='3.3.2'),
    'bootstrap.css': CDNSpec('//netdna.bootstrapcdn.com/bootstrap/{version}/css/', version='3.3.2', subdir='css'),
    'bootstrap.css.map': CDNSpec('//netdna.bootstrapcdn.com/bootstrap/{version}/css/', version='3.3.2', subdir='css'),

    'jquery.dataTables.js': CDNSpec('//cdn.datatables.net/{version}/js', version='1.10.7'),
    'jquery.dataTables.css': CDNSpec('//cdn.datatables.net/{version}/css', version='1.10.7'),
    'dataTables.responsive.js': CDNSpec('//cdn.datatables.net/responsive/{version}/js', version='1.0.4'),
    'dataTables.responsive.css': CDNSpec('//cdn.datatables.net/responsive/{version}/css', version='1.0.4'),
    'dataTables.bootstrap.js': CDNSpec('//cdn.datatables.net/plug-ins/{version}/integration/bootstrap/3/', version='1.10.7'),
    'dataTables.bootstrap.css': CDNSpec('//cdn.datatables.net/plug-ins/{version}/integration/bootstrap/3/', version='1.10.7'),

    'dataTables.fixedColumns.js': CDNSpec('//cdn.datatables.net/fixedcolumns/{version}/js', version='3.0.4'),
    'dataTables.fixedColumns.css': CDNSpec('//cdn.datatables.net/fixedcolumns/{version}/css', version='3.0.4'),

    'moment.js': CDNSpec('//cdnjs.cloudflare.com/ajax/libs/moment.js/{version}/', version='2.10.3'),

    'filesize.js': CDNSpec('//cdn.filesizejs.com/', version=''),

    'dtables.js': CDNSpec('file:///js/', hasMin=False)
}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file')
    parser.add_argument('-s', '--static', action="store_true")
    args = parser.parse_args()

    def test_schemed(url):
        if url[:2] == '//':
            return "http:" + url, 'http'
        elif url[0] == '/':
            return "file:/" + url, 'file'
        else:
            print "unknown scheme on", url
            sys.exit(1)
    agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0'
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', agent)]
    app = flask.Flask('__name__')
    with app.test_request_context():
        for file_key in cdns.keys():
            # for msn in filter(None, ['', cdns[file_key].hasMin
            # file_basename, extension = os.path.splitext(file_name)
            # if extension == '.js':
            #     file_name = file_basename + '.min' + extension

            url = cdns[file_key].url(file_key, use_static=args.static)
            qo, scheme = test_schemed(url)
            if scheme == 'http':
                try:
                    response = opener.open(qo)
                except Exception as e:
                    print "error", e, "on ", file_key, "as", url, "tried", qo
                else:
                    print "OK found", file_key
                if args.file:
                    path = os.path.join(args.file, cdns[file_key].subdir, file_key)
                    print "Write to '%s'" % path
                    ff = open(path, 'w')
                    ff.write(response.read())
                    ff.close()
            elif scheme == 'file':
                uparsed = urlparse.urlparse(qo)
                fpath = uparsed.netloc + uparsed.path
                if not os.path.isfile(fpath):
                    print "error", file_key, "as", url, "tried", fpath
                else:
                    print "OK found file", file_key
