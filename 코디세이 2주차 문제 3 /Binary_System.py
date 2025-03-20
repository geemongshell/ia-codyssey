def read_csv(file_path):
    """CSV 파일을 읽어 리스트로 변환"""
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        header = lines[0].strip().split(',')
        data = [line.strip().split(',') for line in lines[1:]]
    return header, data

def write_binary(output_file_path, data):
    """데이터를 이진 파일로 저장"""
    with open(output_file_path, 'wb') as bin_file:
        for row in data:
            bin_file.write(('|'.join(row) + '\n').encode('utf-8'))

def read_binary(file_path):
    """이진 파일에서 데이터를 읽어 리스트로 변환"""
    with open(file_path, 'rb') as bin_file:
        lines = bin_file.readlines()
        return [line.decode('utf-8').strip().split('|') for line in lines]

def main():
    sorted_input_path = 'C:\\Users\\dino1\\codyssey\\문제3\\Sorted_Flammability_List.csv'
    binary_output_path = 'C:\\Users\\dino1\\codyssey\\문제3\\Mars_Base_Inventory_List.bin'
    
    header, sorted_data = read_csv(sorted_input_path)
    print(f'정렬된 CSV 파일이 리스트로 변환되었습니다: {sorted_input_path}')
    
    write_binary(binary_output_path, [header] + sorted_data)
    print(f'정렬된 인화성 데이터가 이진 파일로 저장되었습니다: {binary_output_path}')
    
    loaded_data = read_binary(binary_output_path)
    print('\n[이진 파일에서 불러온 데이터]')
    for row in loaded_data:
        print(row)

if __name__ == "__main__":
    main()
