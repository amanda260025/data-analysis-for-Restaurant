# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 16:30:44 2020

@author: Jack
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource

'''
（1）加载数据
'''

import os
os.chdir('C:\\Users\\Jack\\Desktop\\')
df2=pd.read_excel('data_point.xlsx')
df2.fillna(0,inplace=True)
df2.columns=['人口密度','道路长度','餐饮计数','素菜餐饮计数','lng','lat']
'''
（2）指标统计
'''
df2['rkmd_norm']=(df2['人口密度']-df2['人口密度'].min())/(df2['人口密度'].max()-df2['人口密度'].min())
df2['cyrd_norm']=(df2['餐饮计数']-df2['餐饮计数'].min())/(df2['餐饮计数'].max()-df2['餐饮计数'].min())
df2['tljp_norm']=(df2['素菜餐饮计数'].max()-df2['素菜餐饮计数'])/(df2['素菜餐饮计数'].max()-df2['素菜餐饮计数'].min())#负向指标，同类竞品越少分越高
df2['dlmd_norm']=(df2['道路长度']-df2['道路长度'].min())/(df2['道路长度'].max()-df2['道路长度'].min())
#指标标准化

df2['final_score']=df2['rkmd_norm']*0.4+df2['cyrd_norm']*0.3+df2['tljp_norm']*0.1+df2['dlmd_norm']*0.2
data_final_q2=df2.sort_values(by='final_score',ascending=False).reset_index()

'''
（3）bokeh制图
'''
data_final_q2['size']=data_final_q2['final_score']*20
data_final_q2['color']='green'
data_final_q2['color'].iloc[:10]='red'
output_file('project0702.html')
source=ColumnDataSource(data_final_q2)
hover=HoverTool(tooltips=[('经度','@lng'),
                           ('纬度','@lat'),
                           ('最终得分','@final_score')])

p=figure(plot_width=800,plot_height=800,title='空间散点图', tools=[hover,'box_select,reset,wheel_zoom,pan,crosshair'])
p.square(x='lng',y='lat',source=source,line_color='black',fill_alpha=0.5,size='size',color='color')

show(p)
#结论：如果要开素菜馆，就可以在红色方块区域开，综合评分最高