import streamlit as st
import random
from math import gcd
from fractions import Fraction

# 페이지 설정
st.set_page_config(page_title="분수의 나눗셈", layout="centered")
st.title("🧮 분수의 나눗셈 학습")

# 세션 상태 초기화
if 'stage' not in st.session_state:
    st.session_state.stage = 1  # 1: 기초 단계, 2: 심화 단계
if 'correct_count' not in st.session_state:
    st.session_state.correct_count = 0
if 'current_problem' not in st.session_state:
    st.session_state.current_problem = None
if 'problem_history' not in st.session_state:
    st.session_state.problem_history = []

def generate_divisible_problem():
    """나누어지는 분수 문제 생성 (단계 1)"""
    # 다양한 형태의 문제를 생성하기 위해 여러 전략 사용
    for _ in range(500):
        # 전략 1: 분모가 배수 관계인 경우
        if random.random() < 0.5:
            denominator2 = random.randint(2, 6)  # 작은 분모
            multiplier = random.randint(2, 4)  # 배수
            denominator1 = denominator2 * multiplier
        else:
            # 전략 2: 더 큰 범위에서 약수 관계 찾기
            denominator1 = random.choice([4, 6, 8, 9, 10, 12, 15, 16, 18, 20])
            divisors = [i for i in range(2, denominator1) if denominator1 % i == 0]
            if not divisors:
                continue
            denominator2 = random.choice(divisors)
        
        # 분자는 더 다양한 범위에서 선택 (1~11)
        numerator1 = random.randint(1, 11)
        numerator2 = random.randint(1, 11)
        
        # 각 분수를 기약분수로 만들기
        gcd1 = gcd(numerator1, denominator1)
        numerator1 //= gcd1
        denominator1 //= gcd1
        
        gcd2 = gcd(numerator2, denominator2)
        numerator2 //= gcd2
        denominator2 //= gcd2
        
        # 분자와 분모가 같으면 스킵 (1/1, 2/2 방지)
        if numerator1 == denominator1 or numerator2 == denominator2:
            continue
        
        # 나눗셈 결과가 정수인지 확인
        result = Fraction(numerator1, denominator1) / Fraction(numerator2, denominator2)
        if result.denominator == 1 and result.numerator > 0:
            # 두 분수의 분모가 서로 달라야 함
            if denominator1 == denominator2:
                continue
            
            return {
                'numerator1': numerator1,
                'denominator1': denominator1,
                'numerator2': numerator2,
                'denominator2': denominator2,
                'result': result,
                'result_num': result.numerator,
                'result_den': result.denominator
            }
        # 아니면 다른 조합을 찾아 재시도
        continue

    # 실패 시(희박) 백업 방식으로 생성 - 정수 결과를 보장해야 함
    for _ in range(1000):
        denominator1 = random.randint(2, 12)
        divisors = [i for i in range(1, denominator1 + 1) if denominator1 % i == 0]
        if len(divisors) > 1:
            divisors.remove(denominator1)
        denominator2 = random.choice(divisors)
        
        if denominator2 % 2 == 0:
            numerator2 = random.choice([2,4,6,8])
        else:
            numerator2 = random.choice([1,3,5,7,9])
        
        if denominator1 % 2 == 0:
            candidates = [2,4,6,8]
        else:
            candidates = [1,3,5,7,9]
        
        # 정수 결과를 만드는 numerator1 찾기
        for numerator1 in candidates:
            # 각 분수를 기약분수로 만들기
            gcd1 = gcd(numerator1, denominator1)
            n1 = numerator1 // gcd1
            d1 = denominator1 // gcd1
            
            gcd2 = gcd(numerator2, denominator2)
            n2 = numerator2 // gcd2
            d2 = denominator2 // gcd2
            
            # 분자와 분모가 같으면 스킵 (1/1, 2/2 방지)
            if n1 == d1 or n2 == d2:
                continue
            
            # 나눗셈 결과가 정수인지 확인
            result = Fraction(n1, d1) / Fraction(n2, d2)
            if result.denominator == 1:
                # 두 분수의 분모가 다른지 확인
                if d1 != d2:
                    # 정수 결과를 찾았으면 반환
                    return {
                        'numerator1': n1,
                        'denominator1': d1,
                        'numerator2': n2,
                        'denominator2': d2,
                        'result': result,
                        'result_num': result.numerator,
                        'result_den': result.denominator
                    }
    
    # 최후의 수단: 간단한 예시 (4/6 ÷ 2/3 = 1)
    numerator1 = 4
    denominator1 = 6
    numerator2 = 2
    denominator2 = 3
    result = Fraction(numerator1, denominator1) / Fraction(numerator2, denominator2)
    
    return {
        'numerator1': numerator1,
        'denominator1': denominator1,
        'numerator2': numerator2,
        'denominator2': denominator2,
        'result': result,
        'result_num': result.numerator,
        'result_den': result.denominator
    }

def generate_non_divisible_problem():
    """나누어지지 않는 분수 문제 생성 (단계 2)
    역수로 곱셈할 때 약분이 가능하도록 생성합니다.
    예: 3/4 ÷ 2/6 = 3/4 × 6/2 → 3과 6이 약분, 4와 2가 약분
    """
    # 약분 가능한 문제를 만들기 위한 전략:
    # numerator1과 denominator2가 공약수를 가지거나
    # denominator1과 numerator2가 공약수를 가지도록 생성
    
    attempts = 0
    while attempts < 100:
        attempts += 1
        
        # 공약수를 만들기 위한 기본 수 선택
        common_factor1 = random.randint(2, 6)  # 첫 번째 공약수
        common_factor2 = random.randint(2, 6)  # 두 번째 공약수
        
        # numerator1과 denominator2가 common_factor1을 공약수로 가지도록
        numerator1 = common_factor1 * random.randint(1, 3)
        denominator2_temp = common_factor1 * random.randint(1, 3)
        
        # denominator1과 numerator2가 common_factor2를 공약수로 가지도록
        denominator1 = common_factor2 * random.randint(1, 4)
        numerator2 = common_factor2 * random.randint(1, 3)
        
        # denominator2는 위에서 만든 값 사용
        denominator2 = denominator2_temp
        
        # 값 범위 확인 (1~12 사이)
        if not (1 <= numerator1 <= 12 and 2 <= denominator1 <= 12 and 
                1 <= numerator2 <= 12 and 2 <= denominator2 <= 12):
            continue
        
        # 나누어 떨어지지 않는 경우인지 확인
        if numerator1 * denominator2 % (denominator1 * numerator2) == 0:
            continue
        
        # 기약분수로 만들기 (문제 자체는 기약분수여야 깔끔함)
        gcd1 = gcd(numerator1, denominator1)
        numerator1 //= gcd1
        denominator1 //= gcd1
        
        gcd2 = gcd(numerator2, denominator2)
        numerator2 //= gcd2
        denominator2 //= gcd2
        
        # 분자와 분모가 같으면 스킵 (1/1, 2/2 방지)
        if numerator1 == denominator1 or numerator2 == denominator2:
            continue
        
        # 두 분수의 분모가 서로 달라야 함 (기약분수 후에 확인)
        if denominator1 == denominator2:
            continue
        
        # 역수로 곱셈할 때 약분이 가능한지 확인
        # numerator1과 numerator2(역수의 분모)의 최대공약수
        gcd_cross1 = gcd(numerator1, numerator2)
        # denominator1과 denominator2(역수의 분자)의 최대공약수
        gcd_cross2 = gcd(denominator1, denominator2)
        
        # 최소한 하나는 약분 가능해야 함
        if gcd_cross1 > 1 or gcd_cross2 > 1:
            result = Fraction(numerator1, denominator1) / Fraction(numerator2, denominator2)
            return {
                'numerator1': numerator1,
                'denominator1': denominator1,
                'numerator2': numerator2,
                'denominator2': denominator2,
                'result': result,
                'result_num': result.numerator,
                'result_den': result.denominator
            }
    
    # 100번 시도해도 실패하면 기본 방식으로 생성 (약분 가능 보장 안됨)
    for _ in range(100):
        numerator1 = random.randint(2, 9)
        denominator1 = random.randint(2, 12)
        numerator2 = random.randint(2, 9)
        denominator2 = random.randint(2, 12)
        
        # 기약분수로 만들기
        gcd1 = gcd(numerator1, denominator1)
        numerator1 //= gcd1
        denominator1 //= gcd1
        
        gcd2 = gcd(numerator2, denominator2)
        numerator2 //= gcd2
        denominator2 //= gcd2
        
        # 분자와 분모가 같으면 스킵
        if numerator1 == denominator1 or numerator2 == denominator2:
            continue
        
        # 나누어 떨어지지 않는 경우인지 확인
        if numerator1 * denominator2 % (denominator1 * numerator2) == 0:
            continue
        
        # 두 분수의 분모가 다른지 확인
        if denominator1 == denominator2:
            continue
        
        result = Fraction(numerator1, denominator1) / Fraction(numerator2, denominator2)
        return {
            'numerator1': numerator1,
            'denominator1': denominator1,
            'numerator2': numerator2,
            'denominator2': denominator2,
            'result': result,
            'result_num': result.numerator,
            'result_den': result.denominator
        }
    
    # 최후의 수단: 간단한 기약분수 반환
    result = Fraction(2, 3) / Fraction(3, 5)
    
    return {
        'numerator1': numerator1,
        'denominator1': denominator1,
        'numerator2': numerator2,
        'denominator2': denominator2,
        'result': result,
        'result_num': result.numerator,
        'result_den': result.denominator
    }


def make_practice_problems(example_problem, n=3):
    """예시 문제와 중복되지 않고 서로 다른 연습문제 n개 생성.
    다양성을 위해 결과값이 서로 다르도록 노력합니다.
    """
    problems = []
    seen = set()
    result_values = set()
    
    # 예시 문제를 seen에 추가
    ex_key = (example_problem['numerator1'], example_problem['denominator1'], 
              example_problem['numerator2'], example_problem['denominator2'])
    seen.add(ex_key)
    result_values.add((example_problem['result_num'], example_problem['result_den']))
    
    attempts = 0
    max_attempts = 5000
    
    while len(problems) < n and attempts < max_attempts:
        p = generate_non_divisible_problem()
        key = (p['numerator1'], p['denominator1'], p['numerator2'], p['denominator2'])
        result_key = (p['result_num'], p['result_den'])
        attempts += 1
        
        # 이미 본 문제면 스킵
        if key in seen:
            continue
        
        # 결과가 너무 비슷한 문제는 70% 확률로 스킵 (다양성 추구)
        if result_key in result_values and random.random() < 0.7:
            continue
            
        # 새로운 문제 추가
        seen.add(key)
        result_values.add(result_key)
        problems.append(p)
    
    return problems

def check_answer(user_num, user_den, correct_num, correct_den):
    """사용자 답 검증"""
    # 기약분수로 변환하여 비교
    user_fraction = Fraction(user_num, user_den)
    correct_fraction = Fraction(correct_num, correct_den)
    return user_fraction == correct_fraction


def safe_rerun():
    """Streamlit 버전 차이로 인해 `experimental_rerun`이 없을 때를 대비한 안전한 재실행 함수.
    가능한 경우 `st.experimental_rerun()` 또는 `st.rerun()`을 호출하고, 둘 다 없으면
    세션 상태 플래그를 토글하고 `st.stop()`으로 현재 실행을 중단합니다.
    """
    try:
        if hasattr(st, "experimental_rerun"):
            st.experimental_rerun()
            return
    except Exception:
        pass
    try:
        if hasattr(st, "rerun"):
            st.rerun()
            return
    except Exception:
        pass
    # 최후의 수단: 세션 플래그 토글 후 실행 중단 — UI의 다음 상호작용 때 스크립트가 재실행됩니다.
    st.session_state["_rerun_flag"] = not st.session_state.get("_rerun_flag", False)
    st.stop()

# ========== 단계 1: 기초 단계 (나누어지는 분수) ==========
if st.session_state.stage == 1:
    st.subheader("📚 단계 1: 나누어지는 분수로 배우기")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"✅ 맞춘 문제: {st.session_state.correct_count}/3")
    with col2:
        if st.session_state.correct_count >= 3:
            st.success("🎉 다음 단계로 갈 준비가 됐어요!")
    
    st.write("""
    **분수의 나눗셈 - 기초 단계**
    
    이번 단계에서는 **분모끼리 나누어 떨어지는** 분수의 나눗셈을 풀어볼 거예요!
    
    예: $\\frac{6}{8} \\div \\frac{3}{4}$ → 분모 8과 4 (8÷4=2)
    
    문제를 풀고 나면 풀이과정을 배울 수 있어요! 📚
    """)
    
    # 1단계에서는 연속 3문제를 풀도록 구성
    if 'stage1_problems' not in st.session_state or len(st.session_state.get('stage1_problems', [])) < 3:
        # 3개의 서로 다른 문제를 생성 (중복 없이)
        stage1_problems = []
        seen_problems = set()
        attempts = 0
        max_attempts = 1000
        
        while len(stage1_problems) < 3 and attempts < max_attempts:
            p = generate_divisible_problem()
            problem_key = (p['numerator1'], p['denominator1'], p['numerator2'], p['denominator2'])
            attempts += 1
            
            # 이미 생성된 문제면 스킵
            if problem_key in seen_problems:
                continue
            
            # 너무 단순한 패턴 추가 체크: 결과가 1이 아닌 다양한 답이 나오도록
            # 한 문제 정도는 결과가 1이 아닌 것으로
            if len(stage1_problems) == 0 or len(stage1_problems) == 2:
                # 첫 번째, 세 번째 문제는 결과가 다양하도록
                if p['result_num'] == 1 and random.random() < 0.3:  # 30% 확률로 스킵 (결과=1인 경우)
                    continue
            elif len(stage1_problems) == 1:
                # 두 번째 문제는 결과가 1이 아닌 것으로
                if p['result_num'] == 1 and random.random() < 0.7:  # 70% 확률로 스킵
                    continue
            
            seen_problems.add(problem_key)
            stage1_problems.append(p)
        
        st.session_state.stage1_problems = stage1_problems
        st.session_state.stage1_index = 0
        st.session_state.stage1_attempts = 0

    # 문제 인덱스가 3(모두 풀음) 이상이면 바로 완료 UI를 보여주고
    # 문제 리스트에 접근하지 않도록 처리합니다 (IndexError 방지).
    if st.session_state.stage1_index >= 3:
        st.info("🚀 3문제를 모두 맞췄어요! 다음 단계로 진행해보세요.")
        if st.button("다음 단계로 이동 →"):
            st.session_state.stage = 2
            st.session_state.current_problem = None
            st.rerun()
        # 이후 코드가 문제에 접근하지 않도록 return으로 종료
        # (한 번에 하나의 Streamlit 스크립트 실행 흐름이므로 안전하게 종료)
        st.stop()

    problem_index = st.session_state.stage1_index
    problem = st.session_state.stage1_problems[problem_index]

    st.info(f"문제 {problem_index + 1} / 3")
    
    # 문제 출제
    st.write(f"""
    ### 문제
    
    다음 분수의 나눗셈을 계산하세요:
    
    $$\\frac{{{problem['numerator1']}}}{{{problem['denominator1']}}} \\div \\frac{{{problem['numerator2']}}}{{{problem['denominator2']}}}$$
    """)
    
    # 힌트 표시 (풀이 과정은 숨김)
    with st.expander("💡 힌트 보기"):
        st.write(f"""
        **분모끼리 어떤 관계가 있을까요?**
        
        분모1: {problem['denominator1']}
        분모2: {problem['denominator2']}
        
        한쪽 분모가 다른 쪽 분모로 나누어떨어져요!
        {problem['denominator1']} ÷ {problem['denominator2']} = {problem['denominator1'] // problem['denominator2']}
        
        정답을 맞춘 후에 풀이 과정을 배워볼 수 있어요! 🎯
        """)
    
    # 답 입력
    st.write("### 답을 입력하세요")
    col1, col2 = st.columns(2)
    with col1:
        user_denominator = st.number_input("분모", min_value=1, value=1, key=f"den_stage1_{problem_index}")
    with col2:
        user_numerator = st.number_input("분자", min_value=1, value=1, key=f"num_stage1_{problem_index}")
    
    # 답 제출
    if st.button("✓ 답 제출", key="submit_stage1"):
        # 정답 검사
        if check_answer(user_numerator, user_denominator, 
                       problem['result_num'], problem['result_den']):
            st.success("🎉 정답입니다!")
            st.session_state.correct_count += 1
            st.session_state.problem_history.append({
                'stage': 1,
                'problem': problem,
                'correct': True
            })

            # 다음 문제로 이동
            st.session_state.stage1_index += 1
            st.session_state.stage1_attempts = 0

            if st.session_state.stage1_index >= 3:
                st.info("🚀 3문제를 모두 맞췄어요! 다음 단계로 진행해보세요.")
                if st.button("다음 단계로 이동 →"):
                    st.session_state.stage = 2
                    # 정리
                    st.session_state.current_problem = None
                    st.rerun()
            else:
                st.write(f"다음 문제로 넘어갑니다: {st.session_state.stage1_index + 1}번 문제")
                if st.button("다음 문제", key="next_stage1"):
                    st.rerun()
        else:
            # 오답 처리: 첫 번째 오답일 때는 정답을 숨기고, 두 번째 오답부터 정답을 보여줌
            st.session_state.stage1_attempts += 1
            attempts = st.session_state.stage1_attempts
            if attempts == 1:
                st.error("❌ 틀렸어요. 힌트를 확인하고 다시 시도해보세요!")
                if st.button("다시 풀기", key="retry_stage1_a"):
                    st.rerun()
            else:
                st.error("❌ 또 틀렸어요. 아래에 정답을 참고하세요.")
                st.write(f"정답: {problem['result_num']}/{problem['result_den']}")
                if st.button("다시 풀기", key="retry_stage1_b"):
                    st.rerun()

# ========== 단계 2: 심화 단계 (나누어지지 않는 분수) ==========
elif st.session_state.stage == 2:
    st.subheader("🚀 단계 2: 더 어려운 분수로 배우기")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"✅ 총 맞춘 문제: {st.session_state.correct_count}개")
    with col2:
        if st.button("🔄 처음부터 다시 시작", key="stage2_restart"):
            st.session_state.stage = 1
            st.session_state.correct_count = 0
            st.session_state.current_problem = None
            st.session_state.problem_history = []
            for k in list(st.session_state.keys()):
                if k.startswith('stage2_'):
                    del st.session_state[k]
            st.rerun()
    
    # 개념 이해 여부 확인
    if 'stage2_concept_understood' not in st.session_state:
        st.session_state.stage2_concept_understood = False
    
    # 개념 설명 단계
    if not st.session_state.stage2_concept_understood:
        st.write("""
        **분수의 나눗셈 - 심화 단계**
        
        이제는 **분모끼리 나누어 떨어지지 않는** 분수의 나눗셈을 배워볼 거예요!
        """)
        
        # 예시 문제 생성 (한 번만)
        if 'stage2_example' not in st.session_state:
            st.session_state.stage2_example = generate_non_divisible_problem()
        
        example = st.session_state.stage2_example
        
        st.write(f"""
        ### 📚 개념 설명: 역수를 이용한 분수의 나눗셈
        
        **예시 문제를 함께 풀어볼게요!**
        
        $$\\frac{{{example['numerator1']}}}{{{example['denominator1']}}} \\div \\frac{{{example['numerator2']}}}{{{example['denominator2']}}}$$
        
        분모끼리 나누어떨어지지 않아서 단계 1 방법으로는 풀기 어려워요.
        하지만 **역수**를 이용하면 쉽게 풀 수 있어요! 🎯
        """)
        
        st.write("---")
        
        st.write("""
        ### 🔑 핵심 개념: 역수
        
        **역수란?** 분자와 분모를 뒤집은 분수예요.
        
        - $\\frac{3}{4}$의 역수 → $\\frac{4}{3}$
        - $\\frac{2}{5}$의 역수 → $\\frac{5}{2}$
        
        **분수의 나눗셈 = 역수의 곱셈** ✨
        
        분수를 나누는 것은 역수를 곱하는 것과 같아요!
        """)
        
        st.write("---")
        
        st.write(f"""
        ### 📖 풀이 과정
        
        $$\\frac{{{example['numerator1']}}}{{{example['denominator1']}}} \\div \\frac{{{example['numerator2']}}}{{{example['denominator2']}}}$$
        
        **Step 1:** 두 번째 분수의 역수를 구해요
        
        $$\\frac{{{example['numerator2']}}}{{{example['denominator2']}}} \\text{{의 역수}} = \\frac{{{example['denominator2']}}}{{{example['numerator2']}}}$$
        
        **Step 2:** 나눗셈을 역수의 곱셈으로 바꿔요
        
        $$\\frac{{{example['numerator1']}}}{{{example['denominator1']}}} \\div \\frac{{{example['numerator2']}}}{{{example['denominator2']}}} = \\frac{{{example['numerator1']}}}{{{example['denominator1']}}} \\times \\frac{{{example['denominator2']}}}{{{example['numerator2']}}}$$
        
        **Step 3:** 분자끼리, 분모끼리 곱해요
        
        $$= \\frac{{{example['numerator1']} \\times {example['denominator2']}}}{{{example['denominator1']} \\times {example['numerator2']}}} = \\frac{{{example['numerator1'] * example['denominator2']}}}{{{example['denominator1'] * example['numerator2']}}}$$
        
        **Step 4:** 약분하면 최종 답!
        
        $$= \\frac{{{example['result_num']}}}{{{example['result_den']}}}$$
        """)
        
        st.write("---")
        
        st.success("""
        ✨ **정리**
        
        분수의 나눗셈 = 두 번째 분수를 뒤집어서 곱하기!
        
        $\\frac{a}{b} \\div \\frac{c}{d} = \\frac{a}{b} \\times \\frac{d}{c}$
        """)
        
        st.write("")
        if st.button("✅ 이해했어요! 연습문제 풀러 가기 →", key="understand_concept"):
            st.session_state.stage2_concept_understood = True
            st.rerun()
        
        st.stop()
    
    # 연습문제 단계
    st.write("""
    **분수의 나눗셈 - 연습문제**
    
    역수를 이용하면 어떤 분수든 나눌 수 있어요! 💪
    이제 3문제를 풀어보세요!
    """)
    
    # 2단계에서는 연속 3문제를 풀도록 구성
    if 'stage2_problems' not in st.session_state or len(st.session_state.get('stage2_problems', [])) < 3:
        # 예시 문제와 중복되지 않는 3개의 연습 문제 생성
        example = st.session_state.get('stage2_example', generate_non_divisible_problem())
        st.session_state.stage2_problems = make_practice_problems(example, 3)
        st.session_state.stage2_index = 0
        st.session_state.stage2_attempts = 0
    
    # 3문제를 모두 풀었는지 확인
    if st.session_state.stage2_index >= 3:
        st.balloons()
        st.success("🎉🎉🎉 축하합니다! 분수의 나눗셈 학습을 완료했어요!")
        st.write(f"""
        ### 🏆 학습 완료!
        
        총 **{st.session_state.correct_count}문제**를 맞추셨어요!
        
        ✅ 단계 1: 나누어지는 분수로 기초 다지기
        ✅ 단계 2: 역수를 이용한 분수의 나눗셈 완벽 마스터
        
        분수의 나눗셈을 모두 정복하셨어요! 👏
        """)
        
        st.info("더 많은 문제를 연습하고 싶다면 아래 버튼을 클릭하세요!")
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🔄 처음부터 다시 하기", key="stage2_restart_all"):
                st.session_state.stage = 1
                st.session_state.correct_count = 0
                st.session_state.current_problem = None
                st.session_state.problem_history = []
                for k in list(st.session_state.keys()):
                    if k.startswith('stage1_') or k.startswith('stage2_'):
                        del st.session_state[k]
                st.rerun()
        with col_b:
            if st.button("➕ 추가 연습하기", key="stage2_more_practice"):
                # 새로운 문제 세트 생성
                example = generate_non_divisible_problem()
                st.session_state.stage2_example = example
                st.session_state.stage2_problems = make_practice_problems(example, 3)
                st.session_state.stage2_index = 0
                st.session_state.stage2_attempts = 0
                st.rerun()
        st.stop()
    
    problem_index = st.session_state.stage2_index
    problem = st.session_state.stage2_problems[problem_index]
    
    st.info(f"문제 {problem_index + 1} / 3")
    
    # 문제 출제
    st.write(f"""
    ### 문제
    
    다음 분수의 나눗셈을 계산하세요:
    
    $$\\frac{{{problem['numerator1']}}}{{{problem['denominator1']}}} \\div \\frac{{{problem['numerator2']}}}{{{problem['denominator2']}}}$$
    """)
    
    # 힌트 표시
    with st.expander("💡 힌트 보기"):
        st.write(f"""
        **분수의 나눗셈은 역수를 이용해요!**
        
        1. 두 번째 분수를 뒤집어요 (역수)
        2. 나눗셈을 곱셈으로 바꿔요
        3. 분자끼리, 분모끼리 곱해요
        4. 약분해요
        
        두 번째 분수: $\\frac{{{problem['numerator2']}}}{{{problem['denominator2']}}}$ → 역수: $\\frac{{{problem['denominator2']}}}{{{problem['numerator2']}}}$
        """)
    
    # 답 입력
    st.write("### 답을 입력하세요")
    col1, col2 = st.columns(2)
    with col1:
        user_denominator = st.number_input("분모", min_value=1, value=1, key=f"den_stage2_{problem_index}")
    with col2:
        user_numerator = st.number_input("분자", min_value=1, value=1, key=f"num_stage2_{problem_index}")
    
    # 답 제출
    if st.button("✓ 답 제출", key="submit_stage2"):
        if check_answer(user_numerator, user_denominator, 
                       problem['result_num'], problem['result_den']):
            st.success("🎉 정답입니다!")
            st.session_state.correct_count += 1
            st.session_state.problem_history.append({
                'stage': 2,
                'problem': problem,
                'correct': True
            })
            
            # 풀이과정 표시
            st.write("### 📖 풀이과정")
            st.write(f"""
            **Step 1:** 두 번째 분수의 분자와 분모를 뒤집어요 (역수)
            
            $$\\frac{{{problem['numerator2']}}}{{{problem['denominator2']}}} \\rightarrow \\frac{{{problem['denominator2']}}}{{{problem['numerator2']}}}$$
            
            **Step 2:** 나눗셈을 곱셈으로 바꿔 계산해요
            
            $$\\frac{{{problem['numerator1']}}}{{{problem['denominator1']}}} \\times \\frac{{{problem['denominator2']}}}{{{problem['numerator2']}}} = \\frac{{{problem['numerator1'] * problem['denominator2']}}}{{{problem['denominator1'] * problem['numerator2']}}}$$
            
            **Step 3:** 약분하면
            
            $$= \\frac{{{problem['result_num']}}}{{{problem['result_den']}}}$$
            """)
            
            # 다음 문제로 이동
            st.session_state.stage2_index += 1
            st.session_state.stage2_attempts = 0
            
            if st.session_state.stage2_index >= 3:
                st.success("🎉 3문제를 모두 완료했어요!")
                if st.button("완료", key="stage2_complete"):
                    st.rerun()
            else:
                st.write(f"다음 문제로 넘어갑니다: {st.session_state.stage2_index + 1}번 문제")
                if st.button("다음 문제", key="next_stage2"):
                    st.rerun()
        else:
            # 오답 처리
            st.session_state.stage2_attempts += 1
            attempts = st.session_state.stage2_attempts
            if attempts == 1:
                st.error("❌ 틀렸어요. 힌트를 확인하고 다시 시도해보세요!")
                if st.button("다시 풀기", key="retry_stage2_a"):
                    st.rerun()
            else:
                st.error("❌ 또 틀렸어요. 아래에 정답을 참고하세요.")
                st.write(f"정답: {problem['result_num']}/{problem['result_den']}")
                if st.button("다시 풀기", key="retry_stage2_b"):
                    st.rerun()
