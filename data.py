#coding:utf-8

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import pickle

if __name__=="__main__":
	# データの読み込み
	data = np.array(pd.read_csv("flight_path.csv",header=None))
	
	times = data[:,0]
	latitude = data[:,1]
	longitude = data[:,2]
	height = data[:,3]
	n_data = len(times)
	threshold = 1.8e4		# 閾値(高度18km)

	# 地図を用意
	m = Basemap(projection='merc',llcrnrlat=30.0,urcrnrlat=45.0,
	llcrnrlon=130.0,urcrnrlon=145.0, lat_ts=20,resolution='f')

	# 地図の土地と海・湖を描画
	m.drawmapboundary(fill_color='white')
	m.fillcontinents(color='lightgrey',lake_color='white')
	m.drawcoastlines()

	# 経路をプロットしていく
	for i in range(n_data-1):
		x1,y1 = m(longitude[i],latitude[i])
		x2,y2 = m(longitude[i+1],latitude[i+1])
		m.plot([x1,x2],[y1,y2],"k")

	# 最高到達点の要素番号
	p2 = np.argmax(height)
	# thresholdに達した時の要素番号(上昇）
	p0 = np.argsort(np.abs(height-threshold)[:p2])[0]
	# thresholdに達した時の要素番号(下降)
	p1 = np.argsort(np.abs(height-threshold)[p2:])[0] + p2
	
	# p0,p1,p2をプロット
	x,y = m(longitude[p2],latitude[p2])
	m.plot(x,y,"b*",ms=20)
	x,y = m(longitude[p0],latitude[p0])
	m.plot(x,y,"r.",ms=20)
	x,y = m(longitude[p1],latitude[p1])
	m.plot(x,y,"r.",ms=20)
	
	plt.show()
	