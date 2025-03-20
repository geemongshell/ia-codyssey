import csv

file_path = 'C:\\Users\\dino1\\codyssey\\문제3\\Mars_Base_Inventory_List.csv'
output_file_path = 'C:\\Users\\dino1\\codyssey\\문제3\\Sorted_Flammability_List.csv'

inventory_list = []

# CSV 파일을 읽어 리스트로 변환
with open(file_path, 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    header = next(reader)  # 첫 번째 행을 헤더로 저장
    
    for row in reader:
        inventory_list.append(row)

# 변환된 리스트 출력
print([header] + inventory_list)  # 헤더 포함 출력
print('CSV 파일이 리스트로 변환되었습니다.')

# 인화성 데이터만 추출 및 정렬
try:
    flammability_index = header.index('Flammability')
    substance_index = header.index('Substance')
    
    # 숫자로 변환할 수 있는 행만 필터링
    valid_rows = [row for row in inventory_list if row[flammability_index].replace('.', '', 1).isdigit()]
    
    # 인화성이 높은 순으로 정렬 (내림차순)
    valid_rows.sort(key=lambda x: float(x[flammability_index]), reverse=True)
    
    # 인화성 데이터만 추출
    filtered_inventory = [[row[substance_index], row[flammability_index]] for row in valid_rows]
    
    # 새로운 CSV 파일로 저장
    with open(output_file_path, 'w', encoding='utf-8', newline='') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(['Substance', 'Flammability'])
        writer.writerows(filtered_inventory)
    
    print(f'정렬된 인화성 데이터가 {output_file_path} 파일로 저장되었습니다.')
except ValueError:
    print("'Flammability' 또는 'Substance' 열을 찾을 수 없습니다. CSV 파일을 확인하세요.")
