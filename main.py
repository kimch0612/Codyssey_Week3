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
    
def main_menu() -> int:
    print("=== Mini NPU Simulator ===\n")
    print("[모드 선택]\n")
    print("1. 사용자 입력 (3x3)")
    print("2. data.json 분석")

    while True:
        m_iSelectedMode = verify_number_input("선택: ", 1, 2)
        if m_iSelectedMode is not None:
            return m_iSelectedMode
        
def user_menu() -> None:
    # TODO: 사용자 입력(3x3) 메뉴 구현
    return None

def data_menu() -> None:
    # TODO: data.json 분석 메뉴 구현
    return None

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