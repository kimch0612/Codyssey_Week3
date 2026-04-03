import sys, json

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

def parse_row() -> list[int] | None:
    # TODO: 사용자가 입력한 한 줄 문자열을 숫자 리스트로 바꾸는 함수
    pass

def read_matrix(size, title) -> list[list[int]] | None:
    # TODO: N x N 행렬 하나를 콘솔에서 안전하게 입력받는 함수
    pass

def validate_matrix(matrix, size) -> bool:
    # TODO: 입력받은 행렬이 올바른지 검증하는 함수
    pass

def calc_mac(pattern, matrix) -> int:
    # TODO: MAC 연산 후 점수 계산
    pass

def decide_label(
        score_corss, 
        score_x, 
        epsilon = 1e-9
) -> str:
    # TODO: 두 점수 비교 후 최종 판정
    pass

def normalize_label(raw_label) -> str:
    # TODO: 입력 라벨을 내부 표준 라벨로 통일
    pass

def extract_size_from_pattern_key(key) -> int | None:
    # TODO: size_5_1 같은 키에서 크기 5를 뽑는 함수
    pass

def measure_mac_time(
        pattern, 
        filter_matrix, 
        repeat=10
) -> float:
    # TODO: MAC 연산의 평균 시간 측정
    pass

def compare_with_expected(predicted, expected) -> bool:
    # TODO: 판정 결과와 정답 비교해서 PASS/FAIL 결정
    pass

def summarize_results(results) -> None:
    # TODO: 전체 테스트 요약
    pass
    
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