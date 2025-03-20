def read_csv(file_path):
    """CSV 파일을 읽어 리스트로 변환"""
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        header = lines[0].strip().split(',')
        data = [line.strip().split(',') for line in lines[1:]]
    return header, data

def filter_and_sort_flammability(header, data):
    """인화성 데이터만 추출하여 정렬"""
    try:
        flammability_index = header.index('Flammability')
        substance_index = header.index('Substance')
        
        valid_rows = [row for row in data if row[flammability_index].replace('.', '', 1).isdigit()]
        
        # 인화성이 높은 순으로 정렬 (내림차순)
        valid_rows.sort(key=lambda x: float(x[flammability_index]), reverse=True)
        
        return [[row[substance_index], row[flammability_index]] for row in valid_rows]
    except ValueError:
        print("'Flammability' 또는 'Substance' 열을 찾을 수 없습니다. CSV 파일을 확인하세요.")
        return []

def filter_dangerous_items(header, data, threshold=0.7):
    """인화성 지수가 특정 값 이상인 위험 물질 필터링"""
    try:
        flammability_index = header.index('Flammability')
        return [row for row in data if float(row[1]) >= threshold]
    except ValueError:
        print("유효한 'Flammability' 데이터가 없습니다.")
        return []

def write_csv(output_file_path, header, data):
    """정렬된 데이터를 새로운 CSV 파일로 저장"""
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(','.join(header) + '\n')
        for row in data:
            output_file.write(','.join(row) + '\n')

def main():
    file_path = 'C:\\Users\\dino1\\codyssey\\문제3\\Mars_Base_Inventory_List.csv'
    sorted_output_path = 'C:\\Users\\dino1\\codyssey\\문제3\\Sorted_Flammability_List.csv'
    danger_output_path = 'C:\\Users\\dino1\\codyssey\\문제3\\Mars_Base_Inventory_danger.csv'
    
    header, inventory_list = read_csv(file_path)
    print([header] + inventory_list)
    print('CSV 파일이 리스트로 변환되었습니다.')
    
    sorted_data = filter_and_sort_flammability(header, inventory_list)
    if sorted_data:
        write_csv(sorted_output_path, ['Substance', 'Flammability'], sorted_data)
        print(f'정렬된 인화성 데이터가 {sorted_output_path} 파일로 저장되었습니다.')
    
    dangerous_items = filter_dangerous_items(['Substance', 'Flammability'], sorted_data)
    if dangerous_items:
        write_csv(danger_output_path, ['Substance', 'Flammability'], dangerous_items)
        print(f'위험 목록이 {danger_output_path} 파일로 저장되었습니다.')

if __name__ == "__main__":
    main()
