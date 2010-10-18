# encoding: UTF-8
#
import movie
M = movie.Movie()

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

for item in M.getListFormData():
    html += '<h3>%s (%s)</h3>' % (item.filename.encode('utf-8'), item.dname.encode('utf-8'))
    html += '<div class="box">'.encode('utf-8')
    html += '<img src="%s" />' % item.imglink.encode('utf-8')
    html += '<p style="color:red;">rate from douban : %s </p>' % item.rate.encode('utf-8')
    html += '<p>intro : %s </p>' % item.intro.encode('utf-8')
    html += '<p style="color:blue; font-size:11px">%s</p>' % item.link.encode('utf-8')
    html += '</div>'

html += '''
    <hr />
    <div class="foot">Not for public, please do not tell anyone!</div>
    <script type="text/javascript">
      var _gaq = _gaq || [];
      _gaq.push(['_setAccount', 'UA-17348181-2']);
      _gaq.push(['_trackPageview']);

      (function() {
        var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
        ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
        var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
      })();
    </script>
    </body></html>
'''

print html
