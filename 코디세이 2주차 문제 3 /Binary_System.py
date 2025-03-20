import csv
import pickle

input_file_path = 'C:\\Users\\dino1\\codyssey\\문제3\\Sorted_Flammability_List.csv'
output_file_path = 'C:\\Users\\dino1\\codyssey\\문제3\\Mars_Base_Inventory_List.bin'

# CSV 파일 읽기
inventory_data = []
with open(input_file_path, 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    inventory_data = list(reader)  # 전체 데이터를 리스트로 변환

# 이진 파일로 저장
with open(output_file_path, 'wb') as bin_file:
    pickle.dump(inventory_data, bin_file)

print(f'CSV 데이터가 이진 파일로 변환되어 {output_file_path}에 저장되었습니다.')

# 저장된 이진 파일 읽기
with open(output_file_path, 'rb') as bin_file:
    loaded_data = pickle.load(bin_file)

# 읽어온 데이터 출력
print('\n[이진 파일에서 불러온 데이터]')
for row in loaded_data:
    print(row)
