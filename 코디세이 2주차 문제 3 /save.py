input_file_path = 'C:\\Users\\dino1\\codyssey\\문제3\\Sorted_Flammability_List.csv'
output_file_path = 'C:\\Users\\dino1\\codyssey\\문제3\\Mars_Base_Inventory_danger.csv'

dangerous_items = []

# 정렬된 인화성 목록 파일 읽기
with open(input_file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()
    header = lines[0].strip().split(',')  # 첫 번째 행을 헤더로 저장
    
    for line in lines[1:]:
        row = line.strip().split(',')
        try:
            if float(row[1]) >= 0.7:  # 인화성 지수가 0.7 이상인 경우
                dangerous_items.append(row)
        except ValueError:
            continue  # 변환할 수 없는 값이 있을 경우 무시

# 위험 목록 출력
print('인화성 지수가 0.7 이상인 목록:')
print([header] + dangerous_items)

# 위험 목록을 새로운 CSV 파일로 저장
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    output_file.write(','.join(header) + '\n')
    for row in dangerous_items:
        output_file.write(','.join(row) + '\n')

print(f'위험 목록이 {output_file_path} 파일로 저장되었습니다.')
