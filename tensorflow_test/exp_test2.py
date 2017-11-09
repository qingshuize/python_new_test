#coding:utf8
from flask import Flask,Response
import pygal
import numpy
import math
from pygal.style import RotateStyle,LightColorizedStyle

app=Flask(__name__)

@app.route('/')
def index():
    return  '''
        <html>
            <body>
                <h1>hello pygal and flask</h1>
                <figure>
                <embed type="image/svg+xml" src="/random/" />
                </figure>
            </body>
        </html>
    '''

@app.route('/random/')
def graph():
    bar_style=RotateStyle('#3322ee',base_style=LightColorizedStyle)

    bar_config=pygal.Config()   #pygal的config类
    bar_config.x_label_rotation=40  #x轴
    bar_config.title_font_size=14   #标题字体大小
    bar_config.show_legend=True #是否显示标注
    bar_config.width=800    #自定义宽度
    bar_config.show_y_guides=False  #是否显示y轴线
    bar_config.show_dots=False  #是否显示点
    bar_config.truncate_label=30    #将项目名限制30字符

    raw_img=pygal.Bar(xlabel_roration=4,style=bar_style)
    #raw_img=pygal.Line(bar_config,style=bar_style)
    #date_series = ['2015-2-2', '2015-10-10', '2016-4-9', '2016-10-9', '2017-3-2', '2017-11-11']
    data_series = numpy.random.randint(1,2*math.pi,30)
    raw_img.title='Random Numbers graph'
    raw_img.x_labels=[i for i in range(30)]
    raw_img.add('Random series',data_series)
    raw_img.add('log series', [math.log(x) for x in data_series])
    raw_img.add('sin series', [math.sin(x) for x in data_series])
    return Response(response=raw_img.render(),content_type="image/svg+xml")

if __name__ == '__main__':
    app.run(debug=True)