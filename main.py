import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
import os

st.set_page_config(page_title="데이터 대시보드", layout="wide")
st.title("데이터 대시보드")

# 한글 폰트 설정 (Windows: Malgun Gothic)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 1. 데이터셋 업로드
data_file = st.file_uploader("CSV 파일 업로드", type=["csv"])

if data_file is not None:
    df = pd.read_csv(data_file)
    st.subheader("데이터 미리보기")
    st.dataframe(df)

    st.subheader("기본 정보")
    st.write(f"행 개수: {df.shape[0]}, 열 개수: {df.shape[1]}")
    st.write(df.describe())
    st.write("결측치 개수:")
    st.write(df.isnull().sum())

    # 2. 전처리: 결측치 처리
    st.subheader("결측치 처리")
    if st.button("결측치 모두 제거"):
        df = df.dropna()
        st.success("결측치가 제거되었습니다.")
        st.dataframe(df)

    # 3. 컬럼 선택
    st.subheader("컬럼 선택 및 시각화")
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    selected_col = st.selectbox("시각화할 수치형 컬럼 선택", numeric_cols)

    if selected_col:
        st.write(f"선택한 컬럼: {selected_col}")
        fig, ax = plt.subplots(1, 2, figsize=(12, 4))
        sns.histplot(df[selected_col], kde=True, ax=ax[0])
        ax[0].set_title("히스토그램")
        sns.boxplot(y=df[selected_col], ax=ax[1])
        ax[1].set_title("박스플롯")
        st.pyplot(fig)

    # 4. 상관관계 히트맵
    st.subheader("상관관계 히트맵")
    if st.button("상관관계 보기"):
        corr = df.corr(numeric_only=True)
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)
else:
    st.info("CSV 파일을 업로드해주세요.")
