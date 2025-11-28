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
    # 목표: 첫 번째 분수의 분자와 분모가 각각 두 번째 분수의 값보다 '크게' 생성되도록 함
    # 여러번 시도해서 조건을 만족하는 조합을 찾음
    for _ in range(100):
        denominator1 = random.randint(2, 12)

        # 두 번째 분수는 분모가 첫 번째 분모의 약수이되, 작도록(strictly smaller) 선택
        divisors = [i for i in range(1, denominator1) if denominator1 % i == 0]
        if not divisors:
            continue
        denominator2 = random.choice(divisors)

        # denominator2의 홀짝에 맞는 numerator2 선택
        if denominator2 % 2 == 0:
            numerator2 = random.choice([2,4,6,8])
        else:
            numerator2 = random.choice([1,3,5,7,9])

        # denominator1의 홀짝에 맞는 numerator1 후보들
        if denominator1 % 2 == 0:
            candidates = [2,4,6,8]
        else:
            candidates = [1,3,5,7,9]

        # strictly greater 인 후보들
        larger = [c for c in candidates if c > numerator2]
        if not larger:
            # 조건을 만족하는 분자가 없으면 다른 분모로 재시도
            continue

        numerator1 = random.choice(larger)

        # 조건을 만족하면 결과 계산 후 반환
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

    # 실패 시(희박) 기존 방식으로 하나 생성(동일하거나 큰 경우 허용)
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
    larger_or_equal = [c for c in candidates if c >= numerator2]
    numerator1 = random.choice(larger_or_equal) if larger_or_equal else max(candidates)
    
    # 실제 나눗셈 결과 계산
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
    """나누어지지 않는 분수 문제 생성 (단계 2)"""
    numerator1 = random.randint(1, 9)
    denominator1 = random.randint(2, 12)
    numerator2 = random.randint(1, 9)
    denominator2 = random.randint(2, 12)
    
    # 나누어 떨어지지 않는 경우를 확보
    while numerator1 * denominator2 % (denominator1 * numerator2) == 0:
        numerator2 = random.randint(1, 9)
        denominator2 = random.randint(2, 12)
    
    # 실제 나눗셈 결과 계산
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

def check_answer(user_num, user_den, correct_num, correct_den):
    """사용자 답 검증"""
    # 기약분수로 변환하여 비교
    user_fraction = Fraction(user_num, user_den)
    correct_fraction = Fraction(correct_num, correct_den)
    return user_fraction == correct_fraction

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
        st.session_state.stage1_problems = [generate_divisible_problem() for _ in range(3)]
        st.session_state.stage1_index = 0
        st.session_state.stage1_attempts = 0

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
        user_numerator = st.number_input("분자", min_value=1, value=1, key=f"num_stage1_{problem_index}")
    with col2:
        user_denominator = st.number_input("분모", min_value=1, value=1, key=f"den_stage1_{problem_index}")
    
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

    # 안내 및 초기 상태
    st.write("**분수의 나눗셈 - 심화 단계**\n\n이제는 분모끼리 나누어 떨어지지 않는 분수를 다뤄볼게요. 먼저 문제를 보고 '풀 수 있다' 또는 '풀 수 없다'를 골라보세요.")

    col1, col2 = st.columns(2)
    with col1:
        st.info(f"✅ 1단계 맞힘: {st.session_state.correct_count} 문제")
    with col2:
        if st.button("🔄 처음부터 다시 시작", key="stage2_restart"):
            st.session_state.stage = 1
            st.session_state.correct_count = 0
            st.session_state.current_problem = None
            st.session_state.problem_history = []
            # clear stage2 state
            for k in ['stage2_problem','stage2_choice','stage2_attempts']:
                if k in st.session_state:
                    del st.session_state[k]
            st.rerun()

    # 초기 문제 준비
    if 'stage2_problem' not in st.session_state:
        st.session_state.stage2_problem = generate_non_divisible_problem()
        st.session_state.stage2_choice = None
        st.session_state.stage2_attempts = 0

    problem = st.session_state.stage2_problem

    # 문제 표시
    st.write(f"### 예시 문제\n\n$$\\frac{{{problem['numerator1']}}}{{{problem['denominator1']}}} \\div \\frac{{{problem['numerator2']}}}{{{problem['denominator2']}}}$$")

    # 선택: 풀 수 있다 / 풀 수 없다
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("풀 수 있다", key="can_solve"):
            st.session_state.stage2_choice = 'can'
            st.session_state.stage2_attempts = 0
            st.experimental_rerun()
    with col_b:
        if st.button("풀 수 없다", key="cannot_solve"):
            st.session_state.stage2_choice = 'cannot'
            st.experimental_rerun()

    # 사용자가 '풀 수 있다'를 선택한 경우: 답 입력 허용
    if st.session_state.get('stage2_choice') == 'can':
        st.write("### 답을 입력하세요")
        c1, c2 = st.columns(2)
        with c1:
            user_n = st.number_input("분자", min_value=1, value=1, key="stage2_user_num")
        with c2:
            user_d = st.number_input("분모", min_value=1, value=1, key="stage2_user_den")

        if st.button("✓ 답 제출", key="stage2_submit"):
            if check_answer(user_n, user_d, problem['result_num'], problem['result_den']):
                st.success("🎉 정답입니다!")
                st.session_state.correct_count += 1
                st.session_state.problem_history.append({'stage':2,'problem':problem,'correct':True})
                # 풀이과정 표시
                st.write("### 📖 풀이과정")
                st.write(f"""
                **Step 1:** 두 번째 분수의 분자와 분모를 뒤집어요

                $$\\frac{{{problem['numerator2']}}}{{{problem['denominator2']}}} \\rightarrow \\frac{{{problem['denominator2']}}}{{{problem['numerator2']}}}$$

                **Step 2:** 나눗셈을 곱셈으로 바꿔 계산해요

                $$\\frac{{{problem['numerator1']}}}{{{problem['denominator1']}}} \\times \\frac{{{problem['denominator2']}}}{{{problem['numerator2']}}} = \\frac{{{problem['numerator1'] * problem['denominator2']}}}{{{problem['denominator1'] * problem['numerator2']}}}$$

                **Step 3:** 약분하면

                $$= \\frac{{{problem['result_num']}}}{{{problem['result_den']}}}$$
                """)
            else:
                st.error("❌ 틀렸어요. 다시 확인해보세요!")
                st.write(f"정답: {problem['result_num']}/{problem['result_den']}")

    # 사용자가 '풀 수 없다'를 선택한 경우: 개념 설명과 풀이 제공
    elif st.session_state.get('stage2_choice') == 'cannot':
        st.write("### 왜 바로 나눌 수 없을까요?")
        st.write("분자나 분모가 더 작은 수에 더 큰 수를 나누는 경우, 단순한 정수 나눗셈으로 딱 떨어지지 않을 수 있어요.")
        st.write("이럴 때는 두 번째 분수의 역수를 이용해 곱셈으로 계산하면 정확히 풀 수 있어요. 아래에서 함께 계산해볼게요.")

        # 풀이과정 보여주기
        st.write("### 📖 풀이과정 (역수 사용)")
        st.write(f"""
        문제:

        $$\\frac{{{problem['numerator1']}}}{{{problem['denominator1']}}} \\div \\frac{{{problem['numerator2']}}}{{{problem['denominator2']}}}$$

        **Step 1:** 두 번째 분수의 역수(뒤집기)

        $$\\frac{{{problem['numerator2']}}}{{{problem['denominator2']}}} \\rightarrow \\frac{{{problem['denominator2']}}}{{{problem['numerator2']}}}$$

        **Step 2:** 곱셈으로 계산

        $$\\frac{{{problem['numerator1']}}}{{{problem['denominator1']}}} \\times \\frac{{{problem['denominator2']}}}{{{problem['numerator2']}}} = \\frac{{{problem['numerator1'] * problem['denominator2']}}}{{{problem['denominator1'] * problem['numerator2']}}}$$

        **Step 3:** 약분하여 최종 답

        $$= \\frac{{{problem['result_num']}}}{{{problem['result_den']}}}$$
        """)

        # 선택지: 이제 풀 수 있다로 전환해서 답 입력 가능하도록 안내
        if st.button("이제 풀 수 있다 (답 입력)", key="stage2_switch_to_can"):
            st.session_state.stage2_choice = 'can'
            st.experimental_rerun()

# (학습 팁 섹션이 제거되었습니다)
