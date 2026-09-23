---
name: craft-ui
description: 画面の見た目を作る・直す・レビューするときに使う。業務アプリ（管理画面・ダッシュボード・一覧/詳細/フォーム）、LP・マーケティングページ、モバイル画面に対応。ブランド色からの配色生成、日本語フォント、文字サイズ・余白・角丸、shadcn/ui・Tailwind のテーマ、「AIっぽい」「垢抜けない」見た目の修正に使う。
---

# craft-ui

業務でもそのまま使える、洗練された UI を作るためのルールと道具。Next.js + React + Tailwind v4 + shadcn/ui を前提にしているが、値とルールはどの構成でも同じ。

## 手順

1. **surface を決める。** 画面ごとに `app`（業務アプリ）/ `lp`（LP・マーケティング）/ `mobile`（スマホ幅が主）のどれかを決め、該当する reference を読む。複数にまたがるなら全部読む。
   - app → [references/app.md](references/app.md)
   - lp → [references/lp.md](references/lp.md)
   - mobile → [references/mobile.md](references/mobile.md)
   - ガラス・すりガラス・Liquid Glass の素材を求められた → [references/glass.md](references/glass.md)

   完了条件：画面ごとに surface と **focal point**（その画面で一番見てほしい 1 点）を 1 文で言える。

2. **土台を用意する。**
   - プロジェクトに既存のデザインシステム（globals.css のトークン、Tailwind のテーマ、コンポーネント）があれば、それを優先する。このスキルは欠けている所だけを埋める。
   - なければ `python3 <このスキルのパス>/scripts/palette.py --brand "#RRGGBB"` を実行し、出力を globals.css に入れる。ブランド色はユーザーに聞く。聞けない場合は `#0b63c5` を使い、そのことを伝える。フォントと Tailwind の設定は [references/tokens.md](references/tokens.md) に従う。

   完了条件：palette.py が `all pairs pass` を出す（ライト・ダークの全文字色が 4.5:1 以上）。

3. **組む。** 下の「コアルール」をすべての画面に当てはめる。surface ごとの型は各 reference に従う。

4. **状態をそろえる。** データを表示する画面では、空・読み込み中・エラー・権限なし・保存中の 5 状態と、長い文字の扱い（何行まで・どこで省略）を決めて実装する。

5. **検査する。** `python3 <このスキルのパス>/scripts/audit.py <変更したファイルやディレクトリ> --surface <surface>` を実行し、ERROR を 0 にする。WARN は理由を説明できるものだけ残す。最後に [references/review.md](references/review.md) のチェックを通す。

   完了条件：audit の ERROR が 0、review.md の全項目に「はい」と答えられる。

## コアルール

### region と item
- 機能のまとまりが **region**：ヘッダー、サイドバー、一覧、フォーム、詳細の各セクション、LP の各セクション。region は面の色（`bg-card` と `bg-background` の差）と境界線（`border-region-border`）で必ず区切る。どこからどこまでが 1 つの機能か、一目でわかる状態にする。
- region の中の **item**（行・項目・設定・リスト要素）は箱にしない。罫線（`border-border`）と余白で区切る。
- 影（shadow）は、画面の上に重なるもの（ダイアログ、シート、ポップオーバー、トースト、コマンドパレット）だけに付ける。

### focal point は画面に 1 つ
その画面の focal point だけを、最大の文字サイズと最も強い色にする。2 番目以降は文字サイズを 1 段以上下げる。focal point を 2 つ置きたくなったら、画面を分けるか、どちらかを下げる。

### 値のスケール
| 項目 | 使ってよい値 | Tailwind |
|---|---|---|
| 文字サイズ | 12 / 14 / 16 / 20 / 28 / 40px（LP のみ 56 / 72 も可） | `text-xs` `text-sm` `text-base` `text-xl` `text-display-sm` `text-display`（`text-display-lg` `text-display-xl`） |
| 太さ | 400 本文 / 500 ラベル・ボタン・ナビ / 700 見出しと重要な数字 | `font-normal` `font-medium` `font-bold` |
| 角丸 | 4px タグ・キー表示 / 8px ボタン・入力・カード・ダイアログ / 丸 アバター・ピル | `rounded-sm` `rounded-lg` `rounded-full` |
| 余白 | 4 の倍数 | `p-1`〜（0.5 刻みは使わない） |
| 行間 | 本文 1.6 / 見出し 1.3〜1.4 | `leading-relaxed` など |
| 動き | 150〜250ms の短いフェードか移動。ぼかしは使わない | `prefers-reduced-motion` で止める |

### 色の役割
| 役割 | トークン | 使う場所 |
|---|---|---|
| **action** | `primary`（ブランド色の塗り） | 画面の主操作 1 つと、進捗の「現在地」だけ |
| **location** | `accent` + `accent-foreground`（ブランド色の薄い面） | 今いる場所：選択中のナビ、タブの下線、選択中の行 |
| **toggle** | `inverse` + `inverse-foreground` | 押し込まれた切替・フィルタ |
| **meaning** | `status-{info,progress,success,warning,danger}`、`category-1`〜`6` | 色が情報を運ぶ所：状態、リスク、人、種類、タグ |
| **text** | `foreground` / `muted-foreground` / `subtle-foreground` | 本文 / 補助 / 最小のラベル |

色は、役割があるときだけ使う。飾りの色面やグラデーションには使わない。意味を持たせた色は、同じ意味を文字（ラベル・アイコン）でも示す。

### 日本語の文字組み
- 書体は Noto Sans JP（本文・見出し）と Noto Sans（数字）。数字には `tabular-nums` を付けて桁をそろえる。
- 見出しだけ `font-feature-settings: "palt"` と `letter-spacing: .02em` で詰める。本文は詰めない。
- 強調は太さか色で行う。日本語に斜体は使わない。
- 本文の 1 行は全角 35〜45 字（`max-w-[40em]` 前後）に収める。

### 文言
利用者の言葉で書く。ボタンは結果を表す動詞にし（「保存」→ 完了後「保存しました」）、エラーは何が起きたかと直し方を書く。

## 参照
- [references/tokens.md](references/tokens.md)：トークン一覧、globals.css の構成、next/font、Tailwind と shadcn/ui の調整
- [references/review.md](references/review.md)：仕上げのチェックリストと、テンプレートっぽさの直し方
- [assets/example-app.html](assets/example-app.html)：全ルールを当てた業務アプリのモック。見た目の基準がほしいときだけ開く
