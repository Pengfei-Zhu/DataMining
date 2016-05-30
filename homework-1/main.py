
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.pyplot import savefig
import os
#pip install StatsModels
#http://nullege.com/codes/search/statsmodels.api.qqplot
import statsmodels.api as sm
import re

NAME_NOMINAL_ATTRIBUTE 				= 'nominal_attribute'
NAME_CHEMISTRY_PARAMETER 			= 'chemistry_parameter'
NAME_ALGAE							= 'algae'
NAME_SEASON							= 'season'
NAME_SIZE							= 'size'
NAME_SPEED							= 'speed'
NAME_MXPH							= 'mxPH'
NAME_MNO2							= 'mnO2'
NAME_CI								= 'CI'
NAME_NO3							= 'NO3'
NAME_NH4							= 'NH4'
NAME_OPO4							= 'oPO4'
NAME_PO4							= 'PO4'
NAME_CHLA							= 'Chla'
NAME_A_1							= 'a1'
NAME_A_2							= 'a2'
NAME_A_3							= 'a3'
NAME_A_4							= 'a4'
NAME_A_5							= 'a5'
NAME_A_6							= 'a6'
NAME_A_7							= 'a7'

item_number = 200

river_info = []

number_attribute_remove_lost_arr = {}

def parse_data():
	fp = open('Analysis.txt')
	i = 0
	for line in fp:
		#print('===============================')
		#print(line.split('|'))
		#line_no_blank = "|".join(line.split())
		#print(line_no_blank) 
		#line_details = line_no_blank.split('|')

		line_details = line.split()
		#print(line_details)
		if len(line_details) >= 17:
			item_detail = {}
			item_detail[NAME_NOMINAL_ATTRIBUTE] = {}
			item_detail[NAME_NOMINAL_ATTRIBUTE][NAME_SEASON] = line_details[0]
			item_detail[NAME_NOMINAL_ATTRIBUTE][NAME_SIZE] = line_details[1]
			item_detail[NAME_NOMINAL_ATTRIBUTE][NAME_SPEED] = line_details[2]

			item_detail[NAME_CHEMISTRY_PARAMETER] = {}
			item_detail[NAME_CHEMISTRY_PARAMETER][NAME_MXPH] = line_details[3]
			item_detail[NAME_CHEMISTRY_PARAMETER][NAME_MNO2] = line_details[4]
			item_detail[NAME_CHEMISTRY_PARAMETER][NAME_CI] = line_details[5]
			item_detail[NAME_CHEMISTRY_PARAMETER][NAME_NO3] = line_details[6]
			item_detail[NAME_CHEMISTRY_PARAMETER][NAME_NH4] = line_details[7]
			item_detail[NAME_CHEMISTRY_PARAMETER][NAME_OPO4] = line_details[8]
			item_detail[NAME_CHEMISTRY_PARAMETER][NAME_PO4] = line_details[9]
			item_detail[NAME_CHEMISTRY_PARAMETER][NAME_CHLA] = line_details[10]

			item_detail[NAME_ALGAE] = {}
			item_detail[NAME_ALGAE][NAME_A_1] = line_details[11]
			item_detail[NAME_ALGAE][NAME_A_2] = line_details[12]
			item_detail[NAME_ALGAE][NAME_A_3] = line_details[13]
			item_detail[NAME_ALGAE][NAME_A_4] = line_details[14]
			item_detail[NAME_ALGAE][NAME_A_5] = line_details[15]
			item_detail[NAME_ALGAE][NAME_A_6] = line_details[16]
			item_detail[NAME_ALGAE][NAME_A_7] = line_details[17]

			river_info.append(item_detail)
			i = i + 1
	fp.close()

def parse_nominal_attribute(na_arr, na_dic):
	for i in range(0, len(na_arr)):
		na_info = na_arr[i]
		#print(na_dic.keys())
		#if na_dic.has_key(na_info):
		if str(na_info) in na_dic.keys():
			na_dic[na_info] = na_dic[na_info] + 1
		else:
			na_dic[na_info] = 1

def cal_nominal_attribute():

	def cal_na_freq(dic, dic_freq):
		for k, v in dic.iteritems():
			dic_freq[k] = (float(v) / item_number)

	season = []
	size = []
	speed = []
	for i in range(0, len(river_info)):
		season.append(river_info[i][NAME_NOMINAL_ATTRIBUTE][NAME_SEASON])
		size.append(river_info[i][NAME_NOMINAL_ATTRIBUTE][NAME_SIZE])
		speed.append(river_info[i][NAME_NOMINAL_ATTRIBUTE][NAME_SPEED])

	season_statistics = {}
	parse_nominal_attribute(season, season_statistics)
	print(season_statistics)
	'''
	season_freq = {}
	cal_na_freq(season_statistics, season_freq)
	print(NAME_SEASON, season_freq)
	'''

	size_statistics = {}
	parse_nominal_attribute(size, size_statistics)
	print(size_statistics)
	'''
	size_freq = {}
	cal_na_freq(size_statistics, size_freq)
	print(NAME_SIZE, size_freq)
	'''

	speed_statistics = {}
	parse_nominal_attribute(speed, speed_statistics)
	print(speed_statistics)
	'''
	speed_freq = {}
	cal_na_freq(speed_statistics, speed_freq)
	print(NAME_SPEED, speed_freq)
	'''


def parse_number_attribute(key_1, key_2, dic):
	na_removed_lost = []
	na_lost_number = 0
	for i in range(0, len(river_info)):
		try:
			na_removed_lost.append(float(river_info[i][key_1][key_2]))
		except ValueError:
			na_lost_number = na_lost_number + 1
	#print(na_removed_lost)
	na_removed_lost.sort()
	na_len = len(na_removed_lost)

	#http://fhqdddddd.blog.163.com/blog/static/18699154201163095410446/
	na_q1_index = float(na_len + 1) / 4
	na_q2_index = float(na_len + 1) / 2
	na_q3_index = 3 * float(na_len + 1) / 4
	if na_len % 2 == 1:
		na_q1 = na_removed_lost[int(na_q1_index) - 1]
		na_q2 = na_removed_lost[int(na_q2_index) - 1]
		na_q3 = na_removed_lost[int(na_q3_index) - 1]
	else:
		def cal(index):
			return na_removed_lost[int(math.floor(index)) - 1] + \
				(na_removed_lost[int(math.ceil(index)) - 1] - na_removed_lost[int(math.floor(index)) - 1]) * (index - math.floor(index))
		na_q1 = cal(na_q1_index)
		na_q2 = cal(na_q2_index)
		na_q3 = cal(na_q3_index)

	dic['max'] = max(na_removed_lost)
	dic['min'] = min(na_removed_lost)
	dic['mean'] = np.mean(na_removed_lost)
	dic['lost_num'] = na_lost_number
	dic['mid'] = na_q2
	quantile = {}
	quantile['Q1'] = na_q1
	quantile['Q2'] = na_q2
	quantile['Q3'] = na_q3
	dic['quantile'] = quantile

	return na_removed_lost


def cal_number_attribute():

	mxph_info = {}
	number_attribute_remove_lost_arr[NAME_MXPH] = parse_number_attribute(NAME_CHEMISTRY_PARAMETER, NAME_MXPH, mxph_info)
	print(NAME_MXPH, mxph_info)

	mno2_info = {}
	number_attribute_remove_lost_arr[NAME_MNO2] = parse_number_attribute(NAME_CHEMISTRY_PARAMETER, NAME_MNO2, mno2_info)	
	print(NAME_MNO2, mno2_info)

	ci_info = {}
	number_attribute_remove_lost_arr[NAME_CI] = parse_number_attribute(NAME_CHEMISTRY_PARAMETER, NAME_CI, ci_info)	
	print(NAME_CI, ci_info)

	no3_info = {}
	number_attribute_remove_lost_arr[NAME_NO3] = parse_number_attribute(NAME_CHEMISTRY_PARAMETER, NAME_NO3, no3_info)	
	print(NAME_NO3, no3_info)

	nh4_info = {}
	number_attribute_remove_lost_arr[NAME_NH4] = parse_number_attribute(NAME_CHEMISTRY_PARAMETER, NAME_NH4, nh4_info)	
	print(NAME_NH4, nh4_info)

	opo4_info = {}
	number_attribute_remove_lost_arr[NAME_OPO4] = parse_number_attribute(NAME_CHEMISTRY_PARAMETER, NAME_OPO4, opo4_info)	
	print(NAME_OPO4, opo4_info)

	po4_info = {}
	number_attribute_remove_lost_arr[NAME_PO4] = parse_number_attribute(NAME_CHEMISTRY_PARAMETER, NAME_PO4, po4_info)	
	print(NAME_PO4, po4_info)

	chla_info = {}
	number_attribute_remove_lost_arr[NAME_CHLA] = parse_number_attribute(NAME_CHEMISTRY_PARAMETER, NAME_CHLA, chla_info)	
	print(NAME_CHLA, chla_info)

	a1_info = {}
	number_attribute_remove_lost_arr[NAME_A_1] = parse_number_attribute(NAME_ALGAE, NAME_A_1, a1_info)	
	print(NAME_A_1, a1_info)

	a2_info = {}
	number_attribute_remove_lost_arr[NAME_A_2] = parse_number_attribute(NAME_ALGAE, NAME_A_2, a2_info)	
	print(NAME_A_2, a2_info)

	a3_info = {}
	number_attribute_remove_lost_arr[NAME_A_3] = parse_number_attribute(NAME_ALGAE, NAME_A_3, a3_info)	
	print(NAME_A_3, a3_info)

	a4_info = {}
	number_attribute_remove_lost_arr[NAME_A_4] = parse_number_attribute(NAME_ALGAE, NAME_A_4, a4_info)	
	print(NAME_A_4, a4_info)

	a5_info = {}
	number_attribute_remove_lost_arr[NAME_A_5] = parse_number_attribute(NAME_ALGAE, NAME_A_5, a5_info)	
	print(NAME_A_5, a5_info)

	a6_info = {}
	number_attribute_remove_lost_arr[NAME_A_6] = parse_number_attribute(NAME_ALGAE, NAME_A_6, a6_info)	
	print(NAME_A_6, a6_info)

	a7_info = {}
	number_attribute_remove_lost_arr[NAME_A_7] = parse_number_attribute(NAME_ALGAE, NAME_A_7, a7_info)	
	print(NAME_A_7, a7_info)

	
	
def plot_histogram():

	#http://matplotlib.org/api/pyplot_summary.html
	#http://matplotlib.org/examples/index.html
	
	#http://blog.csdn.net/lilianforever/article/details/48786795
	#http://blog.csdn.net/xuyanan3/article/details/46755419
	#http://www.codes51.com/article/detail_105523.html
	#http://blog.csdn.net/wishchin/article/details/24906175
	#http://blog.csdn.net/u013524655/article/details/41291715

	path = './histogram'
	if os.path.exists(path) == False:
		os.mkdir(path)

	global number_attribute_remove_lost_arr
	for k, v in number_attribute_remove_lost_arr.iteritems():
		plt.hist(v, 100, facecolor = 'g', alpha = 0.75)
		plt.xlabel(k)
		plt.ylabel('value')
		plt.grid(True)
		
		plt.show()
		plt.savefig(path + '/' + k + '.png')
		plt.close()

def plot_qq_checkout():

	path = './qq_checkout'
	if os.path.exists(path) == False:
		os.mkdir(path)

	global number_attribute_remove_lost_arr
	for k, v in number_attribute_remove_lost_arr.iteritems():
		sm.qqplot(np.array(v), line='r')
		#plt.xlabel(k)
		plt.title(k)
		plt.grid(True)
		#plt.show()
		plt.savefig(path + '/' + k + '.png')
		plt.close()

def plot_box():

	path = './box'
	if os.path.exists(path) == False:
		os.mkdir(path)

	global number_attribute_remove_lost_arr
	for k, v in number_attribute_remove_lost_arr.iteritems():
		plt.boxplot(v)
		plt.xlabel(k)
		plt.ylabel('value')
		plt.grid(True)
		#plt.show()
		plt.savefig(path + '/' + k + '.png')
		plt.close()

def plot_as():

	na_obj = {}
	
	path = './as'
	if os.path.exists(path) == False:
		os.mkdir(path)

	for na_key_name in river_info[0][NAME_NOMINAL_ATTRIBUTE].keys():
			for a_index in range(1, 8):
				a_index_key = 'a' + str(a_index)
				na_obj.clear()
				for i in range(0, len(river_info)):
					if (river_info[i][NAME_NOMINAL_ATTRIBUTE][na_key_name] in na_obj.keys()) == False:
						na_obj[river_info[i][NAME_NOMINAL_ATTRIBUTE][na_key_name]] = []
					na_obj[river_info[i][NAME_NOMINAL_ATTRIBUTE][na_key_name]].append(float(river_info[i][NAME_ALGAE][a_index_key]))

				na_value = []
				labels = []
				for key in na_obj.keys():
					na_value.append(na_obj[key])
					labels.append(key)
				
				plt.boxplot(na_value, labels = labels)
				plt.xlabel(na_key_name)
				plt.ylabel(a_index_key)
				plt.grid(True)
				#plt.show()
				plt.savefig(path + '/' + na_key_name + '_' + a_index_key + '.png')
				plt.close()


def store_new_data(data_info, file_name):
	data_to_file = ''

	for i in range(0, len(river_info)):
		data_to_file += '|' + river_info[i][NAME_NOMINAL_ATTRIBUTE][NAME_SEASON]
		data_to_file += '|' + river_info[i][NAME_NOMINAL_ATTRIBUTE][NAME_SIZE]
		data_to_file += '|' + river_info[i][NAME_NOMINAL_ATTRIBUTE][NAME_SPEED]
		
		data_info_index = 0
		data_to_file += '|' + data_info[NAME_MXPH][data_info_index]
		data_to_file += '|' + data_info[NAME_MNO2][data_info_index]
		data_to_file += '|' + data_info[NAME_CI][data_info_index]
		data_to_file += '|' + data_info[NAME_NO3][data_info_index]
		data_to_file += '|' + data_info[NAME_NH4][data_info_index]
		data_to_file += '|' + data_info[NAME_OPO4][data_info_index]
		data_to_file += '|' + data_info[NAME_PO4][data_info_index]
		data_to_file += '|' + data_info[NAME_CHLA][data_info_index]
		data_info_index += 1

		data_to_file += '|' + river_info[i][NAME_ALGAE][NAME_A_1]
		data_to_file += '|' + river_info[i][NAME_ALGAE][NAME_A_2]
		data_to_file += '|' + river_info[i][NAME_ALGAE][NAME_A_3]
		data_to_file += '|' + river_info[i][NAME_ALGAE][NAME_A_4]
		data_to_file += '|' + river_info[i][NAME_ALGAE][NAME_A_5]
		data_to_file += '|' + river_info[i][NAME_ALGAE][NAME_A_6]
		data_to_file += '|' + river_info[i][NAME_ALGAE][NAME_A_7]

		data_to_file += '|\r\n'
		#print(data_to_file)
	file = open(file_name, 'w')
	file.write(data_to_file)
	file.close()
		


def fillin_lost_by_freq():
	data_info = {}
	re_value = re.compile(r'^[-+]?[0-9]+\.[0-9]+$')
	for i in range(0, len(river_info)):
		for k, v in river_info[i][NAME_CHEMISTRY_PARAMETER].iteritems():
			if (k in data_info.keys()) == False:
				data_info[k] = []

			data_info[k].append(v)
	#print(data_info)
	
	max_freq = {}
	for k, v in data_info.iteritems():
		#key_max_freq = {}
		#[key_max_freq.setdefault(i, []).append(i) for i in v]
		#print({i:len(key_max_freq[i]) for i in key_max_freq})

		#http://www.cnblogs.com/summer2012/p/3176687.html
		l = ([(x, v.count(x)) for x in set(v)])
		l.sort(key = lambda k:k[1], reverse = True)
		if re_value.match(l[0][0]):
			max_freq_key = l[0][0]
			#max_freq_value = l[0][1]
		else:
			max_freq_key = l[1][0]
			#max_freq_value = l[1][1]
		max_freq[k] = max_freq_key

	#print(max_freq)
	for k in data_info:
		for j in range(0, len(data_info[k])):
			if re_value.match(data_info[k][j]) == None:
				data_info[k][j] = max_freq[k]
	#print(data_info)
	store_new_data(data_info, 'Analysis_freq.txt')



def remove_record_containing_lost():
	fp = open('Analysis.txt')
	re_value = re.compile(r'^[-+]?[0-9]+\.[0-9]+$')
	record_to_file = ''
	def check_dig(info, start_index, end_index):
		for i in range(start_index, end_index):
			if re_value.match(info[i]) == None:
				return False
		return True

	for line in fp:
		line_details = line.split()
		if len(line_details) >= 17:
			if check_dig(line_details, 3, 11):
				#print(line_details)
				for line_detail_index in range(0, 18):
					record_to_file += '|' + line_details[line_detail_index]
				record_to_file += '|\r\n'

	#print(record_to_file)

	file = open('Analysis_without_lost.txt', 'w')
	file.write(record_to_file)
	file.close()

if __name__ == '__main__':
	parse_data()
	cal_nominal_attribute()
	cal_number_attribute()
	#plot_histogram()
	#plot_qq_checkout()
	#plot_box()
	#plot_as()
	remove_record_containing_lost()
	fillin_lost_by_freq()
	

	





