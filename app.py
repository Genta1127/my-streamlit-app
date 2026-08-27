import streamlit as st

# ページ設定
st.set_page_config(
    page_title="直観的解説アプリ",
    page_icon="💡",
    layout="centered"
)

# セッション状態（ページインデックス）の初期化
if "page_index" not in st.session_state:
    st.session_state.page_index = 0

# コンテンツデータの定義（直観的な例えのリスト）
contents = [
    {
        "title": "1. 変数（Variable）とは？",
        "analogy_title": "💡 直観的な例え：名前ラベルを貼った「箱」",
        "analogy_text": """
        プログラミングの「変数」は、**名前が書かれたシール（ラベル）が貼られた箱**のようなものです。

        - 箱の中に数値や文字などのデータ（値）を入れることができます。
        - シール（変数名）を見ることで、中身を探さなくてもすぐに取り出せます。
        - 中身は後から自由に入れ替える（更新する）ことができます。
        """,
        "detail": "コード例：`x = 10` （xという名前の箱に数値10を入れる）"
    },
    {
        "title": "2. 関数（Function）とは？",
        "analogy_title": "💡 直観的な例え：自動販売機",
        "analogy_text": """
        プログラミングの「関数」は、**お金やボタン（入力）を入れるとジュース（出力）が出てくる自動販売機**のようなものです。

        - **入力（引数）**：コインを入れる・ボタンを押す操作
        - **内部処理**：お金を計算して自動で商品を落とす仕組み
        - **出力（戻り値）**：出てきたジュース
        """,
        "detail": "コード例：`def make_juice(fruit): return fruit + 'ジュース'`"
    },
    {
        "title": "3. 条件分岐（If文）とは？",
        "analogy_title": "💡 直観的な例え：信号機のルール",
        "analogy_text": """
        プログラミングの「条件分岐」は、**信号機の色によって進むか止まるかを判断するルール**のようなものです。

        - 「もし信号が青なら（条件） ➔ 進む」
        - 「そうではなく赤なら ➔ 止まる」
        - 状況に応じて処理を切り替えます。
        """,
        "detail": "コード例：`if signal == 'green': walk()`"
    },
    {
        "title": "4. 繰り返し（Loop / For文）とは？",
        "analogy_title": "💡 直観的な例え：工場のベルトコンベア",
        "analogy_text": """
        プログラミングの「繰り返し」は、**ベルトコンベアで流れてくる製品にハンコを押し続ける作業**のようなものです。

        - たくさんあるデータ（リスト）を1つずつ取り出して同じ操作を行います。
        - 何度も同じコードを書く必要がなくなり、自動化できます。
        """,
        "detail": "コード例：`for item in items: print(item)`"
    }
]

total_pages = len(contents)
current_content = contents[st.session_state.page_index]

# スタイリング（直観的な例えカードのデザイン）
st.markdown("""
<style>
    .analogy-card {
        background-color: #f0f4f9;
        border-left: 6px solid #3182ce;
        padding: 24px;
        border-radius: 8px;
        margin-bottom: 8px;
    }
    .analogy-title {
        color: #2b6cb0;
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 12px;
    }
    .analogy-text {
        font-size: 1.05rem;
        line-height: 1.7;
        color: #2d3748;
    }
</style>
""", unsafe_allow_html=True)

# アプリヘッダー
st.title("💡 直観的に理解するプログラミング概念")
st.subheader(current_content["title"])

# ---- 「直観的な例え」セクション ----
st.markdown(f"""
<div class="analogy-card">
    <div class="analogy-title">{current_content["analogy_title"]}</div>
    <div class="analogy-text">{current_content["analogy_text"]}</div>
</div>
""", unsafe_allow_html=True)

# ---- 直観的な例えの「右下」に配置されるナビゲーションボタン ----
# カラム比率を設定してボタン群を右側に寄せる
col_space, col_prev, col_next = st.columns([5, 2.5, 2.5])

with col_prev:
    prev_disabled = (st.session_state.page_index == 0)
    if st.button("⬅️ 前へ", use_container_width=True, disabled=prev_disabled, key="btn_prev"):
        st.session_state.page_index -= 1
        st.rerun()

with col_next:
    next_disabled = (st.session_state.page_index == total_pages - 1)
    if st.button("次へ ➡️", use_container_width=True, disabled=next_disabled, key="btn_next"):
        st.session_state.page_index += 1
        st.rerun()

st.divider()

# 補足・詳細コード
st.info(current_content["detail"])

# ページ数のインジケーター表示
st.caption(f"ページ {st.session_state.page_index + 1} / {total_pages}")
