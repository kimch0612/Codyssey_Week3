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

    return average * 1000.0 # ms 단위로 반환

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

def read_valid_matrix(m_iSize: int, m_sTitle: str, m_sName: str) -> list[list[float]]:
    while True:
        try:
            matrix = read_matrix(m_iSize, m_sTitle)
        except (KeyboardInterrupt, InterruptedError, EOFError):
            print("\n입력이 중단되었습니다.")
            sys.exit()

        if validate_matrix(matrix, m_iSize):
            print(f"{m_sName} 저장 완료")
            return matrix

        print(f"입력 형식 오류: 각 줄에 {m_iSize}개의 숫자를 공백으로 구분해 입력하세요.")
        print("처음부터 다시 입력해주세요.")

def make_result(m_sDescription, m_sExpected, m_sPredicted, m_bPassed, m_sReason):
    return {
        "description": m_sDescription,
        "expected": m_sExpected,
        "predicted": m_sPredicted,
        "passed": m_bPassed,
        "reason": m_sReason
    }

def add_failure_result(m_lResults, m_sPatternKey, m_sExpected, m_sPredicted, m_sReason) -> None:
    print(f"--- {m_sPatternKey} ---")
    print(f"판정: {m_sPredicted} | expected: {m_sExpected} | FAIL ({m_sReason})")
    print()
    m_lResults.append(make_result(
        m_sPatternKey,
        m_sExpected,
        m_sPredicted,
        False,
        m_sReason
    ))

def generate_cross_matrix(m_iSize):
    matrix = []
    m_iCenter = m_iSize // 2 # 중심 인덱스를 구하자. (3은 1, 5는 2, 13은 6..)

    for i in range(m_iSize):
        row = []
        for j in range(m_iSize):
            if (i == m_iCenter) or (j == m_iCenter): # 중심과 일치하는 행/열은 1.0으로 설정하자
                row.append(1.0)
            else:
                row.append(0.0)
        matrix.append(row)

    return matrix

def sort_pattern_key(key):
    if not isinstance(key, str):
        return (999999, 999999, str(key)) # 키가 문자열이 아닌 경우, 순서를 맨 뒤로 보내자

    parts = key.split("_") # size_5_1 -> ["size", "5", "1"]
    if len(parts) == 3 and parts[0] == "size": # 요소의 개수가 3개이고, 첫번째 요소가 size인 경우에만 수행
        try:
            return (int(parts[1]), int(parts[2]), key) # n과 idx를 정수로 변환해서 반환하자. (size_5_1 -> (5, 1, "size_5_1"))
        except ValueError:
            return (999999, 999999, key)

    return (999999, 999999, key)

    
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
    m_iSize = 3
    m_iRepeat = 10
    m_fEpsilon = 1e-9

    print("#---------------------------------------")
    print("# [1] 필터 입력")
    print("#---------------------------------------")
    m_lFilterA = read_valid_matrix(m_iSize, "필터 A (3줄 입력, 공백 구분)", "필터 A")
    print()
    m_lFilterB = read_valid_matrix(m_iSize, "필터 B (3줄 입력, 공백 구분)", "필터 B")

    print()
    print("#---------------------------------------")
    print("# [2] 패턴 입력")
    print("#---------------------------------------")
    m_lPattern = read_valid_matrix(m_iSize, "패턴 (3줄 입력, 공백 구분)", "패턴")

    m_fScoreA = calc_mac(m_lPattern, m_lFilterA)
    m_fScoreB = calc_mac(m_lPattern, m_lFilterB)

    m_fStart = time.perf_counter()
    for i in range(m_iRepeat):
        calc_mac(m_lPattern, m_lFilterA)
        calc_mac(m_lPattern, m_lFilterB)
    m_fEnd = time.perf_counter()
    m_fAverageTimeMs = ((m_fEnd - m_fStart) / m_iRepeat) * 1000.0

    if abs(m_fScoreA - m_fScoreB) < m_fEpsilon:
        m_sDecision = "판정 불가"
    elif m_fScoreA > m_fScoreB:
        m_sDecision = "A"
    else:
        m_sDecision = "B"

    print()
    print("#---------------------------------------")
    print("# [3] MAC 결과")
    print("#---------------------------------------")
    print(f"A 점수: {m_fScoreA}")
    print(f"B 점수: {m_fScoreB}")
    print(f"연산 시간(평균/{m_iRepeat}회): {m_fAverageTimeMs:.6f} ms")

    if m_sDecision == "판정 불가":
        print(f"판정: 판정 불가 (|A-B| < {m_fEpsilon})")
    else:
        print(f"판정: {m_sDecision}")

    print()
    print("#---------------------------------------")
    print("# [4] 성능 분석 (3x3)")
    print("#---------------------------------------")
    print("크기       평균 시간(ms)    연산 횟수")
    print("-------------------------------------")
    print(f"3x3       {m_fAverageTimeMs:>12.6f}    {m_iSize * m_iSize}")

def data_menu() -> None:
    m_iRepeat = 10
    m_fEpsilon = 1e-9
    m_dFiltersBySize = {}
    m_lResults = []

    try:
        with open("data.json", "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        print("data.json 파일을 찾을 수 없습니다.")
        return
    except json.JSONDecodeError:
        print("data.json 형식이 올바르지 않습니다.")
        return

    if not isinstance(data, dict):
        print("data.json 최상위 구조 오류: 객체 형태여야 합니다.")
        return

    m_dRawFilters = data.get("filters")
    m_dRawPatterns = data.get("patterns")

    if not isinstance(m_dRawFilters, dict):
        print("data.json 구조 오류: filters 항목이 필요합니다.")
        return

    if not isinstance(m_dRawPatterns, dict):
        print("data.json 구조 오류: patterns 항목이 필요합니다.")
        return

    print("#---------------------------------------")
    print("# [1] 필터 로드")
    print("#---------------------------------------")
    for m_iSize in [5, 13, 25]:
        m_sSizeKey = f"size_{m_iSize}"
        m_dRawFilterSet = m_dRawFilters.get(m_sSizeKey)

        if not isinstance(m_dRawFilterSet, dict):
            print(f"{m_sSizeKey} 필터 FAIL: 필터 묶음이 없거나 형식이 잘못되었습니다.")
            continue

        m_dNormalizedFilterSet = {}
        m_lFilterErrors = []

        for m_sRawFilterName, m_lMatrix in m_dRawFilterSet.items():

            # m_sRawFilterName = "cross" 또는 "x"
            # m_lMatrix = 필터값

            m_sNormalizedLabel = normalize_label(m_sRawFilterName) # 값이 비었거나, 문자열이 아니거나, [+, cross, x]가 아닌 값이 들어온 경우
            if m_sNormalizedLabel is None:
                m_lFilterErrors.append(f"필터 라벨 정규화 실패({m_sRawFilterName})")
                continue

            if m_sNormalizedLabel in m_dNormalizedFilterSet: # filters에서 normalize_label한 값이 중복인 경우
                m_lFilterErrors.append(f"중복 필터 라벨({m_sNormalizedLabel})")
                continue

            if not validate_matrix(m_lMatrix, m_iSize): # matrix가 없거나, 리스트 타입이 아니거나, 행과 요소의 개수가 m_iSize와 다르거나, 요소가 숫자가 아닌 경우
                m_lFilterErrors.append(f"{m_sNormalizedLabel} 필터 크기 불일치")
                continue

            m_dNormalizedFilterSet[m_sNormalizedLabel] = m_lMatrix
            
            """
            m_dNormalizedFilterSet = {
                "Cross": [
                    [0.0, 0.0, 1.0, 0.0, 0.0],
                    ...
                ],
                "X": [
                    [1.0, 0.0, 0.0, 0.0, 1.0],
                    ...
                ]
            }
            """

        if "Cross" not in m_dNormalizedFilterSet:
            m_lFilterErrors.append("Cross 필터 누락")
        if "X" not in m_dNormalizedFilterSet:
            m_lFilterErrors.append("X 필터 누락")

        if len(m_lFilterErrors) > 0:
            print(f"{m_sSizeKey} 필터 FAIL: {'; '.join(m_lFilterErrors)}")
            continue # 필터 등록 건너 뛰고 넘어가고, calc_mac 직전에 'm_iSize not in m_dFiltersBySize' 단계에서 걸림

        m_dFiltersBySize[m_iSize] = m_dNormalizedFilterSet
        print(f"{m_sSizeKey} 필터 로드 완료 (Cross, X)")

    # DATA Preprocessing Done

    print()
    print("#---------------------------------------")
    print("# [2] 패턴 분석 (라벨 정규화 적용)")
    print("#---------------------------------------")
    for m_sPatternKey in sorted(m_dRawPatterns.keys(), # m_dRawPatterns에서 keys(size_5_1, ...)를 가져오고
                                key=sort_pattern_key): # 가져온 값을 sort_pattern_key 기준에 맞춰서 정렬한다
        m_dPatternInfo = m_dRawPatterns[m_sPatternKey] # m_dRawPatterns["size_5_1"] = { input: [...], expected: "Cross" }

        if not isinstance(m_dPatternInfo, dict):
            add_failure_result(m_lResults, m_sPatternKey, "UNKNOWN", "INVALID", "패턴 항목 형식 오류")
            """
            --- size_5_1 ---
            판정: INVALID | expected: UNKNOWN | FAIL (패턴 항목 형식 오류)
            """
            continue

        m_iSize = extract_size_from_pattern_key(m_sPatternKey)
        m_sExpected = normalize_label(m_dPatternInfo.get("expected"))

        if m_sExpected is None: # 값이 없거나, 문자열이 아니거나, + cross x가 아닌 값이 들어온 경우
            add_failure_result(
                m_lResults,
                m_sPatternKey,
                str(m_dPatternInfo.get("expected")),
                "INVALID",
                "expected 라벨 정규화 실패"
            )
            continue

        if m_iSize is None: # m_sPatternKey가 문자열이 아니거나, size_5_1 와 같은 형식이 아닌 경우
            add_failure_result(m_lResults, m_sPatternKey, m_sExpected, "INVALID", "패턴 키 형식 오류")
            continue

        if m_iSize not in m_dFiltersBySize: # DATA Preprocessing 단계에서 불러온 필터에 해당 사이즈가 없는 경우
            add_failure_result(
                m_lResults,
                m_sPatternKey,
                m_sExpected,
                "INVALID",
                f"size_{m_iSize} 필터를 찾을 수 없습니다."
            )
            continue

        if "input" not in m_dPatternInfo: # m_dRawPatterns["size_5_1"]에 input 필드가 없는 경우
            add_failure_result(m_lResults, m_sPatternKey, m_sExpected, "INVALID", "input 필드 누락")
            continue

        m_lPattern = m_dPatternInfo.get("input")
        if not validate_matrix(m_lPattern, m_iSize): # matrix가 없거나, 리스트 타입이 아니거나, 행과 요소의 개수가 m_iSize와 다르거나, 요소가 숫자가 아닌 경우
            add_failure_result(
                m_lResults,
                m_sPatternKey,
                m_sExpected,
                "INVALID",
                f"입력 패턴 크기 불일치({m_iSize}x{m_iSize} 아님)"
            )
            continue

        m_lCrossFilter = m_dFiltersBySize[m_iSize]["Cross"]
        m_lXFilter = m_dFiltersBySize[m_iSize]["X"]

        """
        m_dFiltersBySize = {
            5: {
                "Cross": [[...], [...], [...], [...], [...]],
                "X": [[...], [...], [...], [...], [...]]
            },
            13: {
                "Cross": [[...], [...], ...],
                "X": [[...], [...], ...]
            },
            25: {
                "Cross": [[...], [...], ...],
                "X": [[...], [...], ...]
            }
        }
        """

        m_fCrossScore = calc_mac(m_lPattern, m_lCrossFilter)                # 패턴 input 값을 m_lCrossFilter랑 비교해서 나온 점수
        m_fXScore = calc_mac(m_lPattern, m_lXFilter)                        # 패턴 input 값을 m_lXFilter랑 비교해서 나온 점수
        m_sPredicted = decide_label(m_fCrossScore, m_fXScore, m_fEpsilon)   # 두 점수를 비교해서 뭐가 더 유사한지 판정
        m_bPassed = compare_with_expected(m_sPredicted, m_sExpected)        # 판정 결과랑 정답(m_sExpected)을 비교해서 올바른지 판단 (True/False)

        print(f"--- {m_sPatternKey} ---")
        print(f"Cross 점수: {m_fCrossScore}")
        print(f"X 점수: {m_fXScore}")

        """
        --- size_5_1 ---
        Cross 점수: 1.0
        X 점수: 9.0
        """

        if m_bPassed:
            print(f"판정: {m_sPredicted} | expected: {m_sExpected} | PASS")
            # 판정: X | expected: X | PASS
            print()
            m_lResults.append(make_result( # [4] 결과 요약 단계에서 사용
                m_sPatternKey,
                m_sExpected,
                m_sPredicted,
                True,
                "정상 판정"
            ))
        else:
            if m_sPredicted == "UNDECIDED":
                m_sReason = "동점(UNDECIDED) 처리 규칙"
            else:
                m_sReason = "예상 라벨과 판정 결과 불일치"

            print(f"판정: {m_sPredicted} | expected: {m_sExpected} | FAIL ({m_sReason})")
            # 판정: UNDECIDED | expected: X | FAIL (동점(UNDECIDED) 처리 규칙)
            print()
            m_lResults.append(make_result(
                m_sPatternKey,
                m_sExpected,
                m_sPredicted,
                False,
                m_sReason
            ))

    print("#---------------------------------------")
    print(f"# [3] 성능 분석 (평균/{m_iRepeat}회)")
    print("#---------------------------------------")
    print("크기       평균 시간(ms)    연산 횟수")
    print("-------------------------------------")
    for m_iSize in [3, 5, 13, 25]:
        if (m_iSize in m_dFiltersBySize) and ("Cross" in m_dFiltersBySize[m_iSize]):
            # 측정하려고 하는 사이즈가 m_dFiltersBySize에 있으면서 해당 사이즈에 Cross 필터가 존재하는감
            m_lPerformancePattern = m_dFiltersBySize[m_iSize]["Cross"]
            m_lPerformanceFilter = m_dFiltersBySize[m_iSize]["Cross"]
        else:
            # 아니라면 패턴을 새로 만들어서 측정하자
            m_lPerformancePattern = generate_cross_matrix(m_iSize)
            m_lPerformanceFilter = m_lPerformancePattern

        m_fAverageTimeMs = measure_mac_time(
            m_lPerformancePattern,
            m_lPerformanceFilter,
            m_iRepeat
        )

        if m_fAverageTimeMs is None: # 반복 횟수가 0 또는 음수인 경우
            print(f"{m_iSize}x{m_iSize}      측정 실패         {m_iSize * m_iSize}")
        else:
            print(f"{m_iSize}x{m_iSize}      {m_fAverageTimeMs:>10.6f}         {m_iSize * m_iSize}")

    m_iTotal = len(m_lResults)
    m_iPassed = 0
    for result in m_lResults:
        if result["passed"]:
            m_iPassed += 1
    m_iFailed = m_iTotal - m_iPassed

    """
        #---------------------------------------
        # [3] 성능 분석 (평균/10회)
        #---------------------------------------
        크기       평균 시간(ms)    연산 횟수
        -------------------------------------
        3x3        0.001690         9
        5x5        0.003390         25
        13x13        0.016380         169
        25x25        0.056500         625
    """

    print()
    print("#---------------------------------------")
    print("# [4] 결과 요약")
    print("#---------------------------------------")
    print(f"총 테스트: {m_iTotal}개")
    print(f"통과: {m_iPassed}개")
    print(f"실패: {m_iFailed}개")

    if m_iFailed > 0:
        print("\n실패 케이스:")
        for result in m_lResults:
            if not result["passed"]:
                print(f"- {result['description']}: {result['reason']}")

        """
        실패 케이스:
        - size_5_4: 동점(UNDECIDED) 처리 규칙
        - ...
        """

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
