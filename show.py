# encoding: UTF-8
#
import movie
M = Movie()

html = '''
    <!doctype html>
    <html>
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>Download Movies</title>
    <style>
        p { margin:0; padding:0}
        .foot {font-size:12px; color:gray}
        .box { overflow: hidden }
        img { float:left; left: 0; top: 0; }
        p { padding: 0 0 5px 100px }
    </style>
    <body>
    <h1>电影下载</h1>
'''    
for key in keys:
    o = self.douban(key[1])
    downlink = self.getDownloadLinks(key[0])
    if o != 0 and downlink != 0: 
        html += '<h3>%s</h3>' % o['name']
        html += '<div class="box">'
        html += '<img src="%s" />' % o['img']
        html += '<p style="color:red;">rate from douban : %s </p>' % o['rate']
        html += '<p>intro : %s </p>' % o['intro']
        html += '<p style="color:blue; font-size:11px">%s</p>' % downlink
        html += '</div>'

html += '''
    <hr />
    <div class="foot">Not for public, please do not tell anyone!</div>
    </body></html>
'''
