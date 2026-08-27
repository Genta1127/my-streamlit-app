import streamlit as st
import pandas as pd
import random

# ページ設定
st.set_page_config(
    page_title="Salesforce Admin 100単語マスター",
    page_icon="☁️",
    layout="centered"
)

# カスタムCSS（例えボックスやカードのデザイン）
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f4f8;
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 20px;
    }
    .card-title {
        color: #00A1E0;
        font-size: 28px;
        font-weight: bold;
    }
    .analogy-box {
        background-color: #FFF3CD;
        border-left: 5px solid #FFC107;
        padding: 12px;
        border-radius: 6px;
        margin-top: 10px;
        color: #856404;
    }
</style>
""", unsafe_allow_html=True)

# 100単語のデータセット（単語, 正式な定義, 直感的な例え）
@st.cache_data
def load_data():
    terms = [
        ("Account", "取引先。企業や組織などの情報を管理するオブジェクト。", "会社や取引先の『プロフィール帳』"),
        ("Contact", "取引先責任者。個人のコンタクト情報を管理するオブジェクト。", "名刺ファイルに挟んである『担当者名刺』"),
        ("Opportunity", "商談。売上見込みや進行状況を管理するオブジェクト。", "案件ごとの『見積書・案件メモ』"),
        ("Lead", "リード（見込み客）。まだ取引先化されていない顧客情報。", "イベントで集めた『名刺の山（未検証）』"),
        ("Case", "ケース。顧客からの問い合わせやサポートリクエスト。", "サポート窓口の『問い合わせ受付票』"),
        ("Task", "ToDo（タスク）。実行すべき具体的な作業項目。", "付箋に書いた『今日やることリスト』"),
        ("Event", "行動（イベント）。カレンダーに登録する会議や訪問などの予定。", "手帳の『スケジュール帳』"),
        ("User", "ユーザー。Salesforceにログインして利用する個人。", "オフィスに入るための『社員証を持つ人』"),
        ("Role", "ロール。組織階層に基づいたデータへのアクセス権限（レコードアクセス権）を制御。", "会社の『役職・組織図』"),
        ("Profile", "プロファイル。ユーザーの機能権限（システム権限やオブジェクト権限）を制御。", "部署ごとの『業務アクセスカード』"),
        ("Permission Set", "権限セット。プロファイルを変更せずに特定のユーザーに追加権限を付与する機能。", "特定の人だけに渡す『期間限定の鍵』"),
        ("Permission Set Group", "権限セットグループ。複数の権限セットをまとめて一括割り当てする機能。", "鍵をジャラジャラまとめた『マスターキーリング』"),
        ("Object", "オブジェクト。データを保持するデータベースのテーブルに相当するもの。", "Excelの『シート（バインダー）』"),
        ("Standard Object", "標準オブジェクト。Salesforceに標準で用意されているオブジェクト（Account等）。", "最初から備え付けられている『既製品バインダー』"),
        ("Custom Object", "カスタムオブジェクト。ユーザーが独自に作成するオブジェクト。", "自分の業務に合わせて自作した『オリジナルバインダー』"),
        ("Field", "項目（フィールド）。オブジェクト内のデータ項目（テーブルの列に相当）。", "Excelシートの『列（項目名）』"),
        ("Standard Field", "標準項目。標準で用意されている項目。", "最初から印字されている『記入欄』"),
        ("Custom Field", "カスタム項目。ユーザーが独自に追加する項目。", "自分で線を引いて増やした『自由記入欄』"),
        ("Data Type", "データ型。項目の種類（テキスト、数値、日付、参照関係など）。", "マス目のルール（数字専用、日付専用など）"),
        ("Formula Field", "数式項目。他の項目の値や関数を使って自動計算される読み取り専用項目。", "Excelの『自動計算セル(=A1+B1)』"),
        ("Roll-Up Summary Field", "積み上げ集計項目。主従関係の従オブジェクトのデータを集計する項目。", "子シートの合計を親シートに全自動で出す機能"),
        ("Lookup Relationship", "参照関係。オブジェクト同士をゆるやかに結合するリレーション。", "付箋で『関連ページ参照』と貼るゆるい関係"),
        ("Master-Detail Relationship", "主従関係。親（主）と子（従）が強く結びつくリレーション。", "親が消えたら子も一緒に破棄される『親分と子分』"),
        ("Junction Object", "ジャンクションオブジェクト。多対多のリレーションを実現するための連結オブジェクト。", "両方を結ぶ『仲介役の掲示板』"),
        ("Page Layout", "ページレイアウト。レコード詳細画面の項目の配置や表示・非表示を制御。", "書類の『項目配置デザイン』"),
        ("Lightning App Builder", "Lightningアプリバディ。Lightningページのレイアウトやコンポーネントを設計。", "ドラッグ＆ドロップできる『画面模様替えツール』"),
        ("Compact Layout", "コンパクトレイアウト。ハイライトパネルやモバイルで優先表示される主要項目。", "スマホ画面用の『要約サマリーカード』"),
        ("Record Type", "レコードタイプ。ビジネスプロセスやプロファイルごとに異なるページレイアウトや選択肢を提供。", "『新卒用』と『中途用』で分けた応募フォーム"),
        ("Business Process", "ビジネスプロセス。リード、商談、ケースなどのフェーズ/ステータス遷移の定義。", "進捗を進める『スタンプラリーの順番』"),
        ("Validation Rule", "入力規則。入力データが条件を満たしているかチェックし、エラーを表示する機能。", "未記入があると弾く『厳格な受付チェック』"),
        ("Default Value", "初期値。新規レコード作成時に項目に自動設定されるデフォルト値。", "あらかじめ印刷されている『初期の選択肢』"),
        ("Field-Level Security", "項目レベルセキュリティ。特定のプロファイル/権限セットに対して項目の表示・編集を制限。", "特定の項目に貼る『黒塗り（モザイク）』"),
        ("Org-Wide Defaults (OWD)", "組織の共有設定。オブジェクト全体のデフォルトのアクセス権限を設定。", "会社の『基本セキュリティルール（非公開か全公開か）』"),
        ("Sharing Rule", "共有ルール。OWDより広いアクセス権を例外的に特定ユーザーに付与するルール。", "ルールを破らず特定チームへ開ける『抜け道』"),
        ("Manual Sharing", "手動共有。レコード所有者が個別ユーザーに一時的にアクセス権を付与。", "『これ見ておいて』と直接書類を手渡すこと"),
        ("Implicit Sharing", "暗黙の共有。親レコードや子レコードの所有権に伴い自動的に付与されるアクセス権。", "親会社を見られる人は子会社も自然と見える仕組み"),
        ("Public Group", "公開グループ。共有ルールなどで指定するためのユーザーやロールの集合体。", "部署をまたいだ『プロジェクトチームのメンバーリスト』"),
        ("Queue", "キュー。リードやケースなどを複数ユーザー（チーム）で所有・共有するための仕組み。", "銀行の『番号札を待つ共通トレイ』"),
        ("Flow", "フロー。画面操作やバックグラウンド処理を自動化する強力なローコードツール。", "全自動で動く『ピタゴラスイッチ』"),
        ("Screen Flow", "画面フロー。ユーザーに入力フォームなどを提示して対話的に処理を進めるフロー。", "画面指示に従う『対話型入力ウィザード』"),
        ("Record-Triggered Flow", "レコードトリガフロー。レコードの作成・更新・削除時に自動実行されるフロー。", "『保存』を押した瞬間に作動する仕掛け罠"),
        ("Autolaunched Flow", "自動起動フロー。他のプロセスやボタン等からバックグラウンドで起動されるフロー。", "裏で静かに作動する『自動化プログラム』"),
        ("Workflow Rule", "ワークフロールール。従来の自動化機能（現在はフローへの移行が推奨）。", "一世代前の『全自動ロボット』"),
        ("Process Builder", "プロセスビルダー。従来のグラフィカルな自動化機能（現在はフローへ移行）。", "フローの前身となる『フローチャート自動化』"),
        ("Assignment Rule", "割り当てルール。リードやケースを自動的に適切なユーザーやキューに割り当てる。", "振り分け担当の『全自動仕分けロボ』"),
        ("Auto-Response Rule", "自動応答ルール。Webからのリードやケース作成時に自動でメール返信。", "問い合わせ直後の『自動返信メール』"),
        ("Escalation Rule", "エスカレーションルール。ケースが放置された場合に上位者へ通知・割り当て変更。", "放置された案件を『上司へアラーム通知』"),
        ("Approval Process", "承認プロセス。申請・承認・却下の業務フローを自動化する機能。", "電子化された『回覧板・稟議書』"),
        ("Email Template", "メールテンプレート。自動送信や通知で使用する定型メール。", "あらかじめ用意した『定型文シート』"),
        ("Outbound Message", "アウトバウンドメッセージ。外部システムにWebサービスメッセージを送信する機能。", "外部システムへ送る『全自動ファックス』"),
        ("Data Loader", "データローダ。大量のデータ（最大500万件）を一括処理（挿入・更新・削除等）するツール。", "大量の荷物を運ぶ『大型トラック』"),
        ("Data Import Wizard", "データインポートウィザード。ブラウザ上で最大5万件までのデータを一括取り込みするツール。", "手軽に積める『小型軽トラック』"),
        ("Export", "エクスポート。Salesforce内のデータをCSV等で外部に抽出すること。", "データを『持ち出し用ファイルに出力』"),
        ("UPSERT", "アップサート。既存レコードの更新(Update)と新規挿入(Insert)を同時に行う処理。", "『無ければ新規作成、あれば上書き更新』"),
        ("External ID", "外部ID。外部システムのキー情報を保持し、データ連携やUPSERTに使用する項目。", "他社システムと共通で使う『管理ID』"),
        ("Duplicate Rule", "重複ルール。重複レコードの作成を防ぐ、または警告を出すルール。", "二重登録を防ぐ『名刺ダブり防止センサー』"),
        ("Matching Rule", "一致ルール。重複ルールにおいてどの項目で重複とみなすか条件を定義。", "『名前と電話番号が同じなら同一人物』という判定基準"),
        ("Recycle Bin", "ごみ箱。削除されたレコードが一時的に保管される場所（通常15日間保存）。", "PCの『ごみ箱（保管庫）』"),
        ("Mass Delete", "一括削除。条件を指定して複数のレコードをまとめて削除する機能。", "要らない資料の『一括シュレッダー』"),
        ("Report", "レポート。目的のデータを検索・集計し表やグラフで表示する機能。", "条件で集計した『データ集計表』"),
        ("Dashboard", "ダッシュボード。複数のレポートのグラフィック表示を1つの画面にまとめたもの。", "車のダッシュボードのような『一目で見えるメーター集』"),
        ("Report Type", "レポートタイプ。レポートの作成基準となるオブジェクトとそのリレーションの定義。", "レポートを作るための『型紙（デザインテンプレート）』"),
        ("Standard Report Type", "標準レポートタイプ。標準オブジェクトや関連オブジェクト用に事前に用意された型。", "最初から用意されている『既製型紙』"),
        ("Custom Report Type", "カスタムレポートタイプ。複雑なオブジェクト構造を分析するために作成する独自の型。", "オリジナルで作った『特注の型紙』"),
        ("Summary Report", "サマリーレポート。グループ化（行のグループ化）を行って集計するレポート。", "小計（部署別など）ごとにまとめた表"),
        ("Matrix Report", "マトリックスレポート。行と列の両方でグループ化して集計するレポート。", "縦軸と横軸で集計する『クロス集計表』"),
        ("Joined Report", "結合レポート。異なるレポートタイプのブロックを並べて表示するレポート。", "複数の表を1つに並べた『マルチ集計表』"),
        ("Dashboard Component", "ダッシュボードコンポーネント。グラフ、表、メトリクスなど個々の表示要素。", "ダッシュボードに配置する『個々のメーター部品』"),
        ("Running User", "実行ユーザー。ダッシュボードに表示されるデータのセキュリティ権限の基準となるユーザー。", "『誰の権限メガネでデータを見るか』の基準人物"),
        ("Dynamic Dashboard", "動的ダッシュボード。閲覧しているユーザー自身の権限に基づいてデータが表示される機能。", "見る人によって表示内容が変わる『可変ダッシュボード』"),
        ("Bucket Field", "バケット項目。レポート内で数値を範囲ごとに分類したり項目値をグループ分けする機能。", "データを『Aランク・Bランクのバケツに分類』"),
        ("Cross Filter", "クロスフィルタ。関連オブジェクトの有無（〜を持つ/持たない）でレポートを絞り込む。", "『未購入の顧客だけ』を炙り出す絞り込み器"),
        ("AppLauncher", "アプリ起動ツール。利用可能なアプリやオブジェクトにアクセスするメニュー。", "スマホの『ホーム画面アイコン一覧』"),
        ("Lightning Experience (LEX)", "Lightning Experience。Salesforceの現代的でモダンなUI環境。", "新しく使いやすくなった『モダン新画面』"),
        ("Salesforce Classic", "Salesforce Classic。従来の古いインターフェース。", "昔ながらの『クラシック旧画面』"),
        ("Global Search", "グローバル検索。画面上部の検索バーから組織全体を一括検索。", "Googleのような『社内全検索バー』"),
        ("List View", "リストビュー。オブジェクトのレコード一覧をフィルタ・並び替えして表示。", "フィルター付きの『一覧表示リスト』"),
        ("Kanban View", "看板ビュー。フェーズやステータスごとに視覚的にボード形式でレコードを表示。", "付箋を貼って動かす『かんばんボード』"),
        ("Chatter", "Chatter。Salesforceに統合された社内SNS・コミュニケーションツール。", "社内で使う『LINEやSlackのようなSNS』"),
        ("Company Information", "組織情報。組織名、ライセンス数、主要言語、タイムゾーンなどの基本情報。", "会社の『登記簿・基本プロフィール』"),
        ("Fiscal Year", "事業年度。会社の決算期に合わせた会計年度の設定（標準またはカスタム）。", "会社の『決算スケジュールの設定』"),
        ("Business Hours", "営業時間。サポート時間やエスカレーションルールの基準となる時間帯設定。", "店舗の『営業時間・タイマー設定』"),
        ("Holidays", "休日。営業時間から除外される祝日や会社休日の設定。", "営業カレンダーの『定休日設定』"),
        ("Currency Management", "通貨管理。マルチ通貨機能の有効化や為替レートの設定。", "外貨対応の『レジ設定』"),
        ("Sandbox", "サンドボックス。本番環境に影響を与えずに開発・テスト・研修を行うための検証環境。", "何をしても壊れない『砂場（実験場）』"),
        ("Developer Sandbox", "Developer Sandbox。開発や個別テスト用（データ量は極小）。", "自分専用の『小さな砂場』"),
        ("Full Sandbox", "Full Sandbox。本番環境の完全なコピー（データ含む）を作成できる環境。", "本番そっくりそのままの『巨大なレプリカ砂場』"),
        ("Change Set", "変更セット。Sandboxで開発・設定した内容を本番環境へ移行（デプロイ）する機能。", "作った設定を運ぶ『引越し用コンテナ』"),
        ("Deployment", "デプロイ。作成した設定やプログラムコードを別の環境へ反映させること。", "テスト環境で作ったものを『本番へ反映・開通』"),
        ("Unmanaged Package", "未管理パッケージ。コードや設定を開放・譲渡する目的で配布されるパッケージ。", "改造自由な『オープンソースキット』"),
        ("Managed Package", "管理パッケージ。AppExchange等で販売・配布される保護されたパッケージ。", "中身が保護された『製品版アプリパッケージ』"),
        ("AppExchange", "AppExchange。Salesforce向けのアプリやサードパーティ製ツールが揃うマーケットプレイス。", "Salesforce版の『App Store / Google Play』"),
        ("Multi-Factor Authentication (MFA)", "多要素認証。ログイン時にパスワードに加えて追加の認証情報を求めるセキュリティ機能。", "鍵とスマホ認証の『二重セキュリティ』"),
        ("Single Sign-On (SSO)", "シングルサインオン。1つのID/パスワードで複数のシステムにログインできる仕組み。", "1つのマスターキーで『全部の部屋が開く仕組み』"),
        ("Audit Trail", "設定変更トラッキング。管理者が組織の設定をいつ誰が変更したかの履歴ログ。", "『誰が設定を変えたか』の監視防犯カメラ"),
        ("Login History", "ログイン履歴。ユーザーのログイン日時、IPアドレス、成功/失敗ログの記録。", "会社の『入退室チェックログ』"),
        ("Health Check", "ヘルスチェック。組織のセキュリティ設定の脆弱性を一括診断・評価するツール。", "組織の『セキュリティ定期健診』"),
        ("Freeze User", "ユーザーの凍結。所有権変更の手間をかけず一時的にログインを遮断する機能。", "アカウントの『一時停止（凍結）』"),
        ("Deactivate User", "ユーザーの無効化。不要になったユーザーを無効化しライセンスを解放する処理。", "退職者の『アカウント無効化・鍵回収』")
    ]
    return pd.DataFrame(terms, columns=["Term", "Definition", "Analogy"])

df = load_data()

st.title("☁️ Salesforce Admin 100単語アプリ")
st.caption("弦太様のための認定管理者試験対策ツール（例え機能付き）")

# サイドバーによる切り替え
mode = st.sidebar.radio("学習モードを選択", ["🎴 カードめくり機能", "❓ 4択クイズ機能", "📚 単語リスト一覧"])

# --- モード1: カードめくり ---
if mode == "🎴 カードめくり機能":
    st.header("🎴 単語カード学習")
    
    if "card_index" not in st.session_state:
        st.session_state.card_index = 0
    if "show_back" not in st.session_state:
        st.session_state.show_back = False

    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅️ 前へ"):
            st.session_state.card_index = (st.session_state.card_index - 1) % len(df)
            st.session_state.show_back = False
            st.rerun()
    with col3:
        if st.button("次へ ➡️"):
            st.session_state.card_index = (st.session_state.card_index + 1) % len(df)
            st.session_state.show_back = False
            st.rerun()

    current_term = df.iloc[st.session_state.card_index]["Term"]
    current_def = df.iloc[st.session_state.card_index]["Definition"]
    current_analogy = df.iloc[st.session_state.card_index]["Analogy"]

    st.write(f"**Progress:** {st.session_state.card_index + 1} / {len(df)}")

    # カード部分
    with st.container():
        st.markdown(f'<div class="metric-card"><div class="card-title">{current_term}</div></div>', unsafe_allow_html=True)
        
        if st.session_state.show_back:
            st.info(f"💡 **概要・解説:** {current_def}")
            st.markdown(f'<div class="analogy-box">🎯 **直感的な例え:** {current_analogy}</div>', unsafe_allow_html=True)
            st.write("")
            if st.button("表面を隠す"):
                st.session_state.show_back = False
                st.rerun()
        else:
            if st.button("🔄 意味・例えを見る"):
                st.session_state.show_back = True
                st.rerun()

    if st.button("🎲 ランダムに移動"):
        st.session_state.card_index = random.randint(0, len(df) - 1)
        st.session_state.show_back = False
        st.rerun()

# --- モード2: 4択クイズ ---
elif mode == "❓ 4択クイズ機能":
    st.header("❓ 4択クイズ")

    if "quiz_question" not in st.session_state:
        st.session_state.quiz_question = None
        st.session_state.quiz_options = []
        st.session_state.correct_answer = None
        st.session_state.correct_analogy = None
        st.session_state.user_answered = False
        st.session_state.score = 0
        st.session_state.total_quiz = 0

    def generate_new_question():
        correct_row = df.sample(1).iloc[0]
        wrong_rows = df[df["Term"] != correct_row["Term"]].sample(3)
        
        options = wrong_rows["Definition"].tolist() + [correct_row["Definition"]]
        random.shuffle(options)
        
        st.session_state.quiz_question = correct_row["Term"]
        st.session_state.correct_answer = correct_row["Definition"]
        st.session_state.correct_analogy = correct_row["Analogy"]
        st.session_state.quiz_options = options
        st.session_state.user_answered = False

    if st.session_state.quiz_question is None:
        generate_new_question()

    st.subheader(f"問題: **{st.session_state.quiz_question}** の正しい説明は？")

    for i, option in enumerate(st.session_state.quiz_options):
        if st.button(f"{i+1}. {option}", key=f"opt_{i}"):
            st.session_state.user_answered = True
            st.session_state.total_quiz += 1
            if option == st.session_state.correct_answer:
                st.session_state.score += 1
                st.success(f"🎉 正解です！お見事ですわ！\n\n🎯 **例え:** {st.session_state.correct_analogy}")
            else:
                st.error(f"❌ 残念！正解は: {st.session_state.correct_answer}\n\n🎯 **例え:** {st.session_state.correct_analogy}")

    if st.session_state.user_answered:
        if st.button("次の問題へ ➡️"):
            generate_new_question()
            st.rerun()

    st.markdown("---")
    st.write(f"📊 成績: **{st.session_state.score}** / **{st.session_state.total_quiz}** 問正解")

# --- モード3: リスト一覧 ---
elif mode == "📚 単語リスト一覧":
    st.header("📚 単語100選 一覧データ（例え付き）")
    search_query = st.text_input("検索ワードを入力 (例: Flow, レポート, ロール, 砂場)")
    
    if search_query:
        filtered_df = df[
            df["Term"].str.contains(search_query, case=False) | 
            df["Definition"].str.contains(search_query, case=False) |
            df["Analogy"].str.contains(search_query, case=False)
        ]
        st.dataframe(filtered_df, use_container_width=True)
    else:
        st.dataframe(df, use_container_width=True)