import streamlit as st

# 体重・活動レベル・目標からPFCを算出するフォーム
def pfc_form():
    # st.subheader("目標PFCを算出するための情報")

    # 体重の入力
    weight = st.number_input("体重 (kg)", min_value=30, max_value=200, step=1, placeholder=60, value=None)

    # 活動レベルの選択
    activity_level = st.selectbox("活動レベルを選択", ["低活動", "普通", "高活動"])

    # 目標の選択
    goal = st.selectbox("目標を選択", ["維持", "減量", "増量"])

    user_input = st.text_input("追加要望があれば入力してください。", placeholder='ex.) セロリが苦手、洋食多め、etc...')

    # 送信ボタンが押されたときの処理
    if st.button("送信"):
        if weight and activity_level and goal:
            return str(weight), activity_level, goal, user_input
        else:
            st.error("全ての項目を入力してください。")
    return None, None, None, None

# PFCの計算を行う関数
def calculate_macros(calories, protein_percentage, fat_percentage, carb_percentage):
    protein_grams = (calories * (protein_percentage / 100)) / 4
    fat_grams = (calories * (fat_percentage / 100)) / 9
    carb_grams = (calories * (carb_percentage / 100)) / 4
    
    return protein_grams, fat_grams, carb_grams

# 目標PFCを直接入力するフォーム
def pfc_input_form():
    # st.subheader("1日あたりの目標PFCを直接入力")

    # カロリーの入力
    calories = st.number_input("総カロリー (kcal)", min_value=0, step=10, key="calories")

    # タンパク質、脂質、炭水化物のパーセンテージの入力
    cols1, cols2, cols3 = st.columns(3)

    with cols1:
        protein_percentage = st.number_input("タンパク質 (%)", min_value=0.0, max_value=100.0, step=0.1, key="protein_percentage")
    with cols2:
        fat_percentage = st.number_input("脂質 (%)", min_value=0.0, max_value=100.0, step=0.1, key="fat_percentage")
    with cols3:
        carb_percentage = st.number_input("炭水化物 (%)", min_value=0.0, max_value=100.0, step=0.1, key="carb_percentage")

    # 計算結果をリアルタイムで表示
    if calories > 0:
        protein_grams, fat_grams, carb_grams = calculate_macros(calories, protein_percentage, fat_percentage, carb_percentage)

        # 結果を横一列で表示
        st.markdown(f"**タンパク質:** {protein_grams:.2f}g | "
                    f"**脂質:** {fat_grams:.2f}g | "
                    f"**炭水化物:** {carb_grams:.2f}g")

    user_input = st.text_input("追加要望があれば入力してください。", placeholder='ex.) セロリが苦手、洋食多め、etc...')

    # 送信ボタンが押されたときの処理
    if st.button("送信"):
        # 合計パーセンテージのチェック
        total_percentage = protein_percentage + fat_percentage + carb_percentage
        if calories > 0 and total_percentage == 100:
            return f"{round(protein_grams, 2):.2f}", f"{round(fat_grams, 2):.2f}", f"{round(carb_grams, 2):.2f}", user_input
        st.error("タンパク質、脂質、炭水化物の合計を100%にしてください。")
    return None, None, None, None