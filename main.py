import sys, json, time

def verify_number_input(
        m_sString: str,
        m_iMin: int | None = None,
        m_iMax: int | None = None
) -> int | None:
    if ( m_iMin is None ) or ( m_iMax is None ):
        print("값을 다시 입력해주세요.")
        return None
    
    try:
        m_iValue = int(input(m_sString))
    except (KeyboardInterrupt, InterruptedError, EOFError):
        print("\n입력이 중단되었습니다.")
        sys.exit()
    except ValueError:
        print("숫자만 입력해주세요.")
        return None
    
    if (m_iValue < m_iMin) or (m_iValue > m_iMax):
        print("올바른 범위의 값을 입력해 주세요.")
        return None
    
    return m_iValue

def parse_row(row_text, size) -> list[float] | None:
    m_sText = row_text.strip()
    if not m_sText:
        print("텍스트를 입력해주세요.")
        return None

    m_lStringValues = m_sText.split()
    if len(m_lStringValues) != size:
        print("입력한 값을 다시 확인해주세요.")
        return None
    
    m_fFloatValues = []
    for str_value in m_lStringValues:
        try:
            m_fFloatValues.append(float(str_value))
        except ValueError:
            print("숫자만 입력해주세요.")
            return None
        
    return m_fFloatValues

def read_matrix(size, title) -> list[ list[float] ]:
    matrix = []
    print(title)

    for i in range(0, size):
        while True:
            row = parse_row(input(), size)
            if row is None:
                continue
            else:
                matrix.append(row)
                break

    return matrix

def validate_matrix(matrix, size) -> bool:
    if matrix is None:
        print("matrix 정보가 이상합니다. 분명 앞에서 확인했을텐데.."); return False
    elif not (isinstance(matrix, list)):
        print("matrix가 list 타입이 아닙니다. 분명 앞에서 확인했을텐데.."); return False
    elif len(matrix) != size:
        print("matrix 행 개수가 기대한 값과 다릅니다."); return False
    
    for row in matrix:
        if not isinstance(row, list):
            print("matrix의 행이 list 타입이 아닙니다."); return False
        elif len(row) != size:
            print("matrix 열 개수가 기대한 값과 다릅니다."); return False
        
        for value in row:
            if (value is None) or (not isinstance(value, (int, float))):
                print("matrix의 값이 숫자가 아닙니다."); return False
            
    return True

def calc_mac(pattern, matrix) -> float:
    score = 0.0

    for i in range(len(pattern)):
        for j in range(len(pattern[i])):
            score += pattern[i][j] * matrix[i][j]

    return score

def decide_label(
        score_cross, 
        score_x, 
        epsilon = 1e-9
) -> str:
    
    if abs(score_cross - score_x) < epsilon:
        return "UNDECIDED"
    elif score_cross > score_x:
        return "Cross"
    else:
        return "X"

def normalize_label(raw_label) -> str | None:
    if raw_label is None:
        print("값이 비었습니다.")
        return None
    elif not isinstance(raw_label, str):
        print("기대한 값과 다른 타입이 들어왔습니다.")
        return None

    label = raw_label.strip().lower()
    if label in ["+", "cross"]: return "Cross"
    if label in ["x"]: return "X"

    print("식별할 수 없는 값입니다.")
    return None

def extract_size_from_pattern_key(key) -> int | None:    
    if not isinstance(key, str):
        print("입력 값이 문자열 타입이 아닙니다.")
        return None
    
    parts = key.split("_")
    if len(parts) != 3:
        print("키 형식이 예상과 다릅니다.")
        return None
    
    if parts[0] != "size":
        print("키 형식이 예상과 다릅니다..")
        return None
    
    try:
        size = int(parts[1])
    except:
        print("키에서 크기를 추출하는 과정에서 오류가 발생했습니다.")
        return None

    return size

def measure_mac_time(
        pattern, 
        filter_matrix, 
        repeat=10
) -> float | None:
    
    if repeat <= 0:
        print("반복 횟수가 이상합니다.")
        return None

    start = time.perf_counter()

    for i in range(repeat):
        calc_mac(pattern, filter_matrix)

    end = time.perf_counter()

    total = end - start
    average = total / repeat

    return average * 1000.0

def compare_with_expected(predicted, expected) -> bool:
    if predicted is None or expected is None:
        print("입력 값이 비었습니다.")
        return False
    
    return predicted == expected

def summarize_results(results) -> None:
    total = len(results)
    passed = 0

    for result in results:
        if result["passed"]: passed += 1
    failed = total - passed

    print("---------------------")
    print(f"총 테스트 케이스 수: {total}")
    print(f"통과한 케이스 수: {passed}")
    print(f"실패한 케이스 수: {failed}")

    if failed > 0:
        print("\n실패한 케이스:")
        for result in results:
            if not result["passed"]:
                print(f"- {result['description']} (예상: {result['expected']}, 실제: {result['predicted']})")

    
def main_menu() -> int:
    print("=== Mini NPU Simulator ===\n")
    print("[모드 선택]\n")
    print("1. 사용자 입력 (3x3)")
    print("2. data.json 분석")

    while True:
        m_iSelectedMode = verify_number_input("선택: ", 1, 2)
        if m_iSelectedMode is not None:
            return m_iSelectedMode
        
def user_input_menu() -> None:
    print("#--------------")
    print("# [1] 필터 입력")
    print("#--------------")
        
def user_menu() -> None:
    # TODO: 사용자 입력(3x3) 메뉴 구현
    return None

def data_menu() -> None:
    # TODO: data.json 분석 메뉴 구현
    with open("data.json", "r") as file:
        data = json.load(file)

def main() -> None:
    m_iSelectedMode = main_menu()
    
    if m_iSelectedMode == 1:
        user_menu()
    elif m_iSelectedMode == 2:
        data_menu()
    else:
        print("알 수 없는 모드입니다. 분명 앞에서 값을 체크했을텐데..?")

if __name__ == "__main__":
    main()