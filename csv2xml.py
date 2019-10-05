# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 17:00:01 2019

@author: Dell
"""

import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET


def xml_to_csv(path):
    xml_list = []
    # 读取注释文件
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            value = ('train_part1\\image\\' + root.find('frame').text + '.jpg',
                     int(member[1][0].text),
                     int(member[1][1].text),
                     int(member[1][2].text),
                     int(member[1][3].text),
                     member[0].text
                     )
            xml_list.append(value)
    column_name = ['frame', 'name', 'xmin', 'ymin', 'xmax', 'ymax']
 
    # 将所有数据分为样本集和验证集，一般按照3:1的比例
    train_list = xml_list
    filename= xml_list[0][0] + '.csv'
    # 保存为CSV格式
    train_df = pd.DataFrame(train_list, columns=column_name)
    train_df.to_csv('train_part1\\box_csv\\'+filename, index=None)
 
 
def main(path):
#    path = './xml'
    xml_to_csv(path)
    print('Successfully converted xml to csv.')
 

if __name__ =='__main__':
    path = r'F:\BaiduNetdiskDownload\train_part1\box'
#    save_path = r'F:\BaiduNetdiskDownload\train_part1\box_csv'
#    files = os.listdir(path)
#    for i in range(len(files)):
#    file_path = '\\'.join([path,files[i]])
#    file_name = file_path.split('.')[0]
#    xml_df = xml_to_csv(files)
#    file_name = file_name + r'.csv'
#    xml_df.to_csv(file_name, index=None)
    main(path)