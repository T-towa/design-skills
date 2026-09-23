# surface: app（業務アプリ）

管理画面・ダッシュボード・CRM・社内ツールなど、同じ人が毎日長時間使う画面。速く読めて、迷わず、長時間でも疲れないことを最優先にする。本文は `text-sm`（14px）。

## レイアウトの骨組み

```
┌ header（region: bg-card, border-b border-region-border, h-16）──────────────┐
│ ロゴ | 開いている画面のタブ | ⌘K 検索 | 通知・ユーザー                          │
├ sidebar（region: bg-card, border-r, w-72）┬ main（bg-background, p-6, gap-4）─┤
│ ナビ・ビュー（件数付き）                    │ 画面タイトル（text-xl）＋操作          │
│ 絞り込み                                   │ region（Card）を縦に積む               │
└──────────────────────────────────────────┴───────────────────────────────────┘
```

- header・sidebar・main の各 region は、面の色か境界線で必ず区切る。
- main の中は、機能ごとに Card（region）を積む。Card の中の行や項目は罫線で区切る。
- 横幅は 1280px 以上を基準にする。1024〜1279px ではサイドバーをアイコンだけ（`w-16`）にし、1023px 以下はモバイルの型（[mobile.md](mobile.md)）に切り替える。

## ナビゲーション
- 項目は `text-sm font-medium`、高さ 36〜40px、`rounded-lg`。件数は右端に `num text-muted-foreground`。
- 選択中は **location**（`bg-accent text-accent-foreground`）。左端の色帯や太字化では示さない。
- 未読・要対応の件数は `bg-status-danger text-status-danger-foreground` の小さなピル。

## 一覧（テーブル）
- 一覧全体を 1 つの region（Card）にする。見出し行は `bg-muted text-xs font-medium text-muted-foreground`、`sticky top-0`。
- 行の高さは標準 56〜64px、詰めた表示 44〜48px。行の区切りは `border-b border-border`。行を箱にはしない。
- 1 行目は主語（名前＋所属を 2 行）。数字の列は右寄せで `num`。
- 状態は **meaning** の色のタグで示す。同じ情報を 2 つの列で重ねて示さない（フェーズのタグと進み具合バーのどちらか一方）。
- 長い文字：名前は 1 行で省略（`truncate`）し、全文は `title` で見せる。説明文は 2 行まで（`line-clamp-2`）。行の高さはそろえる。
- ホバーは `hover:bg-muted`、選択中の行は `bg-accent`。
- 行全体をクリック可能にする場合は、行を `button` か `a` にして、キーボードでも開けるようにする。
- 金額の表記は、一覧では丸めた値（「480万円」）、詳細では正確な値（「¥4,800,000」）。同じ画面の中では 1 つの形式にそろえる。

## クイックビュー（一覧の文脈を残して中身を見る）
- 右からのシート（shadcn の `Sheet`、幅 480〜560px）。背後は `bg-black/30` で覆う。
- focal point は「次にやること」と、それを実行する主ボタン。名前は `text-base font-bold` に下げる。
- 中は region を 3 つまで（次の操作、基本情報、履歴）。詳細ページへの入口（「詳細を開く」）を必ず置く。

## 詳細ページ
- 先頭の region に、その画面の focal point（金額・状態・期限などの一番重要な値）を `text-display num font-bold` で置く。名前は `text-xl`。
- 進捗がある対象は、段階を横並びの帯で示す。現在地だけ `bg-primary`、完了は `bg-accent text-accent-foreground`、未着手は `bg-secondary`。帯の横に「次の段階へ進める」主ボタンを置く。
- 項目は 2 列の定義リスト（ラベル `text-xs text-subtle-foreground`、値 `text-sm font-medium`）。その場で編集できる項目には鉛筆アイコンを付ける。
- 活動の履歴は、スレッド形式の region にする。1 件ごとに人・時刻・種類（`category-*` の色）・本文を並べ、入力欄は region の下端に置く。社内メモは `bg-status-warning` の面で区別する。

## コマンドパレット（⌘K / Ctrl+K）
- どの画面からでも開ける。幅 560〜640px、画面上部 1/5 の位置、`rounded-lg shadow-lg`。
- 1 行目は入力欄（`text-base`、高さ 44px）。候補は「開く（レコード）」と「操作」の 2 つに分ける。選択中は **location**。
- ↑↓ で選び、Enter で実行、Esc で閉じる。この操作を画面下部にキー表示で案内する。

## キーボード
- 一覧：↑↓ または J / K で行を移動、Enter で開く、Esc で戻る。
- N で記録欄にフォーカス、⌘Enter で送信。
- キー表示は `rounded-sm border border-input px-1 text-xs num`。

## フィードバック
- 保存・送信・状態の変更は、トースト（左下または下中央、`bg-inverse text-inverse-foreground rounded-lg`）で知らせる。取り消せる操作には「取り消す」ボタンを付け、確認ダイアログは出さない。
- 取り消せない操作（削除など）だけ、確認ダイアログを出す。ボタンは `destructive` にし、対象の名前を文言に入れる。

## 5 つの状態
| 状態 | 見せ方 |
|---|---|
| 空 | region の中央に 1 文の説明と、次の行動のボタン 1 つ。条件で絞り込んだ結果が空なら「条件を外す」操作を出す |
| 読み込み中 | 実際のレイアウトと同じ形のスケルトン（`bg-muted animate-pulse rounded-sm`）。回転するアイコンは 1 秒を超える操作のボタンの中だけ |
| エラー | region の上端に `bg-status-danger` の帯。何が失敗したかと「再試行」ボタン。入力内容は消さない |
| 権限なし | 操作ボタンを消すのではなく無効化し、理由を補足（「編集には管理者の権限が必要です」） |
| 保存中 | 押したボタンだけ無効化して文言を「保存中…」に変える。画面全体は止めない |

## ダイアログとフォーカス
- ダイアログ・シート・パレットは、開いたらフォーカスを中に移し、Tab で外に出ないようにし、閉じたら開いた元のボタンにフォーカスを戻す（Radix / shadcn のコンポーネントは既定でこうなる。自作する場合だけ注意）。
- フォーム：ラベルは入力欄の上、必須は「必須」の文字で示す。エラーは入力欄の下に `text-status-danger-foreground`、内容は直し方まで書く。

## 密度
「標準」と「詰めた表示」の 2 段階を用意する。詰めた表示は、行の高さと縦の余白だけを減らす。文字サイズは変えない。
