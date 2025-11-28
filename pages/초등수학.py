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
    # 분자는 1-9, 분모는 2-12 범위에서 선택
    numerator1 = random.randint(1, 9)
    denominator1 = random.randint(2, 12)
    
    # 두 번째 분수는 분모가 첫 번째 분모의 약수가 되도록
    divisors = [i for i in range(1, denominator1 + 1) if denominator1 % i == 0]
    if len(divisors) > 1:
        divisors.pop(0)  # 1 제외
    denominator2 = random.choice(divisors)
    numerator2 = random.randint(1, 9)
    
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
    
    # 새 문제 생성
    if st.session_state.current_problem is None:
        st.session_state.current_problem = generate_divisible_problem()
    
    problem = st.session_state.current_problem
    
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
        user_numerator = st.number_input("분자", min_value=1, value=1, key=f"num_stage1_{id(problem)}")
    with col2:
        user_denominator = st.number_input("분모", min_value=1, value=1, key=f"den_stage1_{id(problem)}")
    
    # 답 제출
    if st.button("✓ 답 제출", key="submit_stage1"):
        if check_answer(user_numerator, user_denominator, 
                       problem['result_num'], problem['result_den']):
            st.success("🎉 정답입니다!")
            st.session_state.correct_count += 1
            st.session_state.problem_history.append({
                'stage': 1,
                'problem': problem,
                'correct': True
            })
            st.session_state.current_problem = None
            
            # 정답 시 풀이 과정 표시
            st.write("### 📖 이렇게 풀이해요!")
            st.write(f"""
            **Step 1:** 두 번째 분수의 분자와 분모를 뒤집어요
            
            $$\\frac{{{problem['numerator2']}}}{{{problem['denominator2']}}} \\rightarrow \\frac{{{problem['denominator2']}}}{{{problem['numerator2']}}}$$
            
            **Step 2:** 뒤집은 분수를 이용해 계산을 진행해요

            $$\\frac{{{problem['numerator1']}}}{{{problem['denominator1']}}} \\div \\frac{{{problem['numerator2']}}}{{{problem['denominator2']}}} = \\frac{{{problem['numerator1']}}}{{{problem['denominator1']}}} \\times \\frac{{{problem['denominator2']}}}{{{problem['numerator2']}}}$$
            
            **Step 3:** 분자끼리, 분모끼리 곱해요
            
            $$= \\frac{{{problem['numerator1']} \\times {problem['denominator2']}}}{{{problem['denominator1']} \\times {problem['numerator2']}}} = \\frac{{{problem['numerator1'] * problem['denominator2']}}}{{{problem['denominator1'] * problem['numerator2']}}}$$
            
            **Step 4:** 약분해요
            
            $$= \\frac{{{problem['result_num']}}}{{{problem['result_den']}}}$$
            
            💡 **중요:** 분수를 차근차근 정리하고 약분하는 연습이 중요해요! ⭐
            """)
            
            if st.session_state.correct_count >= 3:
                st.info("🚀 3문제를 맞췄어요! 다음 단계로 진행해보세요.")
                if st.button("다음 단계로 이동 →"):
                    st.session_state.stage = 2
                    st.session_state.current_problem = None
                    st.rerun()
            else:
                st.write(f"앞으로 {3 - st.session_state.correct_count}문제만 더 맞추면 다음 단계로 갈 수 있어요!")
                if st.button("다음 문제", key="next_stage1"):
                    st.session_state.current_problem = None
                    st.rerun()
        else:
            st.error("❌ 틀렸어요. 다시 한 번 풀어보세요!")
            st.write(f"정답: {problem['result_num']}/{problem['result_den']}")
            if st.button("다시 풀기", key="retry_stage1"):
                st.session_state.current_problem = None
                st.rerun()

# ========== 단계 2: 심화 단계 (나누어지지 않는 분수) ==========
elif st.session_state.stage == 2:
    st.subheader("🚀 단계 2: 더 어려운 분수로 배우기")
    
    st.write("""
    **분수의 나눗셈 - 심화 단계**
    
    이제는 **분모끼리 나누어 떨어지지 않는** 분수를 풀어볼 거예요!
    
    하지만 걱정하지 마세요. 방법은 같아요:
    
    ### 핵심: 나눗셈을 곱셈으로 바꿔요! 
    
    $$\\frac{a}{b} \\div \\frac{c}{d} = \\frac{a}{b} \\times \\frac{d}{c}$$
    
    두 번째 분수의 **분자와 분모를 뒤집으면** 곱셈이 돼요!
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"✅ 맞춘 문제: {st.session_state.correct_count - 3}문제")
    with col2:
        if st.button("🔄 처음부터 다시 시작"):
            st.session_state.stage = 1
            st.session_state.correct_count = 0
            st.session_state.current_problem = None
            st.session_state.problem_history = []
            st.rerun()
    
    # 새 문제 생성
    if st.session_state.current_problem is None:
        st.session_state.current_problem = generate_non_divisible_problem()
    
    problem = st.session_state.current_problem
    
    # 문제 출제
    st.write(f"""
    ### 문제
    
    다음 분수의 나눗셈을 계산하세요:
    
    $$\\frac{{{problem['numerator1']}}}{{{problem['denominator1']}}} \\div \\frac{{{problem['numerator2']}}}{{{problem['denominator2']}}}$$
    """)
    
    # 풀이 과정 - 단계별 유도
    with st.expander("💡 단계별 풀이 과정"):
        st.write(f"""
        **🔑 핵심: 나눗셈은 곱셈으로 바뀌어요!**
        
        **Step 1:** 두 번째 분수를 뒤집어요 (역수)
        
        $$\\frac{{{problem['numerator2']}}}{{{problem['denominator2']}}} \\rightarrow \\frac{{{problem['denominator2']}}}{{{problem['numerator2']}}}$$
        
        **Step 2:** ÷ 기호를 × 기호로 바꿔요
        
        $$\\frac{{{problem['numerator1']}}}{{{problem['denominator1']}}} \\div \\frac{{{problem['numerator2']}}}{{{problem['denominator2']}}} = \\frac{{{problem['numerator1']}}}{{{problem['denominator1']}}} \\times \\frac{{{problem['denominator2']}}}{{{problem['numerator2']}}}$$
        
        **Step 3:** 분자끼리, 분모끼리 곱해요
        
        $$= \\frac{{{problem['numerator1']} \\times {problem['denominator2']}}}{{{problem['denominator1']} \\times {problem['numerator2']}}} = \\frac{{{problem['numerator1'] * problem['denominator2']}}}{{{problem['denominator1'] * problem['numerator2']}}}$$
        
        **Step 4:** 약분해요 (최대공약수로 나누기)
        
        약분 과정:
        - 분자: {problem['numerator1'] * problem['denominator2']}
        - 분모: {problem['denominator1'] * problem['numerator2']}
        - 최대공약수: {gcd(problem['numerator1'] * problem['denominator2'], problem['denominator1'] * problem['numerator2'])}
        
        $$= \\frac{{{problem['result_num']}}}{{{problem['result_den']}}}$$
        
        **중요:** 나눗셈을 곱셈으로 바꾸는 것이 분수 나눗셈의 비결이에요! 🌟
        """)
    
    # 답 입력
    st.write("### 답을 입력하세요")
    col1, col2 = st.columns(2)
    with col1:
        user_numerator = st.number_input("분자", min_value=1, value=1, key=f"num_stage2_{id(problem)}")
    with col2:
        user_denominator = st.number_input("분모", min_value=1, value=1, key=f"den_stage2_{id(problem)}")
    
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
            st.session_state.current_problem = None
            if st.button("다음 문제", key="next_stage2"):
                st.rerun()
        else:
            st.error("❌ 틀렸어요. 다시 한 번 생각해보세요!")
            st.write(f"정답: {problem['result_num']}/{problem['result_den']}")
            
            with st.expander("다시 풀이 과정을 봐볼래요?"):
                st.write(f"""
                **올바른 풀이:**
                
                $$\\frac{{{problem['numerator1']}}}{{{problem['denominator1']}}} \\div \\frac{{{problem['numerator2']}}}{{{problem['denominator2']}}}$$
                
                두 번째 분수를 뒤집고 ÷를 ×로 바꿔요:
                
                $$= \\frac{{{problem['numerator1']}}}{{{problem['denominator1']}}} \\times \\frac{{{problem['denominator2']}}}{{{problem['numerator2']}}}$$
                
                $$= \\frac{{{problem['numerator1'] * problem['denominator2']}}}{{{problem['denominator1'] * problem['numerator2']}}}$$
                
                $$= \\frac{{{problem['result_num']}}}{{{problem['result_den']}}}$$
                """)
            
            if st.button("다시 풀기", key="retry_stage2"):
                st.session_state.current_problem = None
                st.rerun()

# 하단 정보
st.divider()
st.write("### 📖 학습 팁")
st.write("""
- **분수의 나눗셈 = 역수와의 곱셈**
- 두 번째 분수의 분자와 분모를 바꾸는 것이 핵심이에요!
- 항상 약분을 잊지 말아요!
- 천천히 단계별로 풀어보세요! 🌟
""")
