# encoding: UTF-8
import json
import os
import math
from pymystem3 import Mystem
#подключаемся к json-ам с оценкой
directory = 'materials'
#вычисляем, сколько в директории лежит файлов
number_of_input_files = len(filter(lambda x: not x.endswith('~'), os.listdir(directory)))
output_data = {}
#count_of_good_marks = 0
#count_of_bad_marks = 0
list_of_all_terms = {}
#иду по документам
for i in range(1, number_of_input_files + 1):
    with open('materials/' + str(i)) as data_file:
        data = json.load(data_file)
    #нормализую слова из сообщения
    m = Mystem()
    list_of_terms = filter(lambda x: not x == ' ', m.lemmatize(data['text']))
    #убираю повторяющиеся слова
    output_data[i] = {}
    output_data[i]['id'] = data['id']
    output_data[i]['mark'] = data['mark']
    output_data[i]['terms'] = {}
    for term in list_of_terms:
        if term not in output_data[i]['terms']:
            output_data[i]['terms'][term] = 1
        else:
            output_data[i]['terms'][term] += 1
    for term in output_data[i]['terms'].keys():
        if term not in list_of_all_terms:
            list_of_all_terms[term] = 1
        else:
            list_of_all_terms[term] += 1
        #подсчёт tf
        count_of_terms = output_data[i]['terms'][term]
        output_data[i]['terms'][term] = {'tf': float(count_of_terms)/len(list_of_terms), 'idf': 0}

for i in range(1, number_of_input_files + 1):
    #подсчёт idf
    for term in output_data[i]['terms'].keys():
        output_data[i]['terms'][term]['idf'] = math.log(float(number_of_input_files)/list_of_all_terms[term])
    #запись результата
    with open('results/' + str(i) + '_tf-idf', 'w') as output_file:
        json.dump(output_data[i], output_file)

