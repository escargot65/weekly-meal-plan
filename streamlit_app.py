import streamlit as st
from openai import OpenAI
# from notion_api.create_pages import create_menu, create_plan
import form.pfc_calculator as pfc_calculator

# Show title and description.
st.title("🍽 ミールプラン作成bot 🍽")
st.write("設定した必要摂取カロリーに応じて、ミールプランを作成します。")

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("利用には、OpenAI API keyが必要です。（[こちら](https://platform.openai.com/account/api-keys)から作成可）", icon="🗝️")
else:

    # 入力方法を選択
    input_method = st.radio("入力方法を選んでください。", ("体重・活動レベル・目標から算出", "目標PFCを直接入力"))
    input_condition = ''

    # 1. 体重・活動レベル・目標から算出する場合
    if input_method == "体重・活動レベル・目標から算出":
        weight, activity_level, goal, user_input = pfc_calculator.pfc_form()  # pfc_form関数を呼び出し  
        if weight is not None:
            input_condition = '・体重' + weight + 'kg, 活動レベルが' + activity_level + ', ' + goal + 'が目標の人に適したPFCバランス'
            if user_input:
                input_condition += '・' + user_input

    # 2. 目標PFCを直接入力する場合
    elif input_method == "目標PFCを直接入力":
        protein_grams, fat_grams, carb_grams, user_input = pfc_calculator.pfc_input_form()  # pfc_input_form関数を呼び出し
        if protein_grams is not None:
            input_condition = '・一日の摂取PFCバランスが、タンパク質' + protein_grams + 'g, 脂質' + fat_grams + 'g, 炭水化物' + carb_grams + 'になるようにしたい'
            if user_input:
                input_condition += '・' + user_input

    # notionページ作成
    # menu = create_menu()
    # # st.write(menu)
    # plan = create_plan(menu["id"])
    # # st.write(plan)

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    # for message in st.session_state.messages:
    #     with st.chat_message(message["role"]):
    #         st.markdown(message["content"])

    # 最新のメッセージのみを表示
    if st.session_state.messages:
        last_message = st.session_state.messages[-1]
        if last_message["role"] == "assistant":
            st.markdown(last_message["content"])
            # st.write(last_message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if input_condition:

        content = """
        あなたは優秀な管理栄養士です。後述の条件を加味して、1週間分の献立を作成してください。
        ・和食中心
        ・脂質は削りすぎない
        ・食物繊維は必要充分な量を摂取する
        """ + input_condition + """
        作成した献立について、下記情報も記載してください。
        ・必要な食材およびグラム数
        ・1食ごとのPFCパランス
        """

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": content})

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})