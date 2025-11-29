import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage,HumanMessage,AIMessage
from dotenv import load_dotenv

load_dotenv()

# 専門家の種類と対応するシステムメッセージを定義
EXPERTS = {
    "医療アドバイザー": "あなたは経験豊富な医療アドバイザーです。健康、医療、栄養に関する質問に対して、科学的根拠に基づいた分かりやすいアドバイスを提供します。ただし、診断や治療については専門医への相談を促してください。",
    "プログラミングメンター": "あなたは熟練したプログラミングメンターです。プログラミングに関する質問に対して、コードの書き方、ベストプラクティス、デバッグ方法などを分かりやすく説明します。初心者にも理解しやすい言葉で教えてください。",
    "ビジネスコンサルタント": "あなたはビジネス戦略の専門家です。経営、マーケティング、組織運営に関する質問に対して、実践的なアドバイスと戦略的な提案を提供します。具体的な事例や方法論を交えて説明してください。"
}

def get_llm_response(expert_type: str, user_input: str) -> str:
    """
    選択された専門家タイプとユーザー入力を受け取り、LLMからの回答を返す
    
    Args:
        expert_type: 専門家の種類（医療アドバイザー、プログラミングメンター、ビジネスコンサルタント）
        user_input: ユーザーからの質問テキスト
    
    Returns:
        LLMからの回答テキスト
    """
    # LLMを初期化
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
    
    # 専門家タイプに応じたシステムメッセージを取得
    system_message = EXPERTS.get(expert_type, "あなたは親切なアシスタントです。")
    
    # メッセージリストを作成
    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=user_input)
    ]
    
    # LLMを実行して回答を取得
    result = llm.invoke(messages)
    return result.content

# Streamlit UIの構築
st.title("AI専門家アシスタント")

st.markdown("""
### このアプリについて
このアプリでは、異なる分野の専門家AIに質問することができます。
質問したい分野を選択し、質問を入力して送信ボタンを押してください。

### 利用可能な専門家
- **医療アドバイザー**: 健康、医療、栄養に関する質問にお答えします
- **プログラミングメンター**: プログラミングの学習や技術的な質問にお答えします
- **ビジネスコンサルタント**: 経営戦略やビジネスに関する質問にお答えします

### 使い方
1. 相談したい専門家をラジオボタンで選択
2. 質問内容をテキストボックスに入力
3. 「回答を取得」ボタンをクリック
4. AI専門家からの回答が表示されます
""")

st.divider()

# 専門家選択のラジオボタン
expert_type = st.radio(
    "相談したい専門家を選択してください:",
    options=list(EXPERTS.keys()),
    help="選択した専門家の分野に応じた回答が得られます"
)

# 質問入力欄
user_input = st.text_area(
    "質問を入力してください:",
    height=100,
    placeholder="ここに質問を入力してください..."
)

# 回答取得ボタン
if st.button("回答を取得", type="primary"):
    if user_input.strip():
        with st.spinner(f"{expert_type}が回答を考えています..."):
            try:
                # LLMから回答を取得
                response = get_llm_response(expert_type, user_input)
                
                # 回答を表示
                st.success(f"**{expert_type}からの回答:**")
                st.write(response)
            except Exception as e:
                st.error(f"エラーが発生しました: {str(e)}")
    else:
        st.warning("質問を入力してください。")