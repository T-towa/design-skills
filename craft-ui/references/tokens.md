# トークンと実装の土台

## 1. 配色を作る

```bash
python3 <skill>/scripts/palette.py --brand "#0b63c5" > /tmp/tokens.css   # 報告は標準エラーに出る
python3 <skill>/scripts/palette.py --brand "#0b63c5" --brand-dark "#70adff" # ダークのブランド色を指定する場合
```

出力は 3 ブロック：`:root`（ライト）、`.dark`（ダーク）、`@theme inline`（Tailwind のクラス対応）。globals.css の既存の `:root` / `.dark` / `@theme inline` を置き換える（`@import "tailwindcss";` などの読み込み行は残す）。

ブランド色は 1 つだけ渡す。灰色（背景・面・線・文字）はブランド色へ数 % 寄せて自動で作られるので、どのブランド色でも地とぶつからない。ブランド色を変えるときはスクリプトを再実行するだけ。

`FAIL` が出たら、その色は使えない組み合わせ。明るすぎるブランド色（黄色など）は、主ボタンの文字が自動で暗い色になり、フォーカスの枠は同じ色相の濃い色が作られる。それでも失敗する場合は、`--brand-dark` を指定するか、ブランド色を少し濃くする。

## 2. トークン一覧（shadcn/ui 互換＋追加分）

| トークン | Tailwind | 役割 |
|---|---|---|
| `background` | `bg-background` | 地。region の外側 |
| `card` | `bg-card` | region の面（ヘッダー、サイドバー、パネル、LP のセクション帯） |
| `muted` | `bg-muted` | 表の見出し行、控えめな面 |
| `secondary` | `bg-secondary` | ホバー・中立の選択 |
| `foreground` / `muted-foreground` / `subtle-foreground` | `text-*` | 本文 / 補助 / 最小ラベル（すべて 4.5:1 以上） |
| `border` | `border-border` | item の区切り線 |
| `region-border` | `border-region-border` | region の境界線（`border` より少し濃い） |
| `input` | `border-input` | 入力欄の枠 |
| `primary` / `primary-foreground` | `bg-primary text-primary-foreground` | **action**：主ボタン、進捗の現在地 |
| `accent` / `accent-foreground` | `bg-accent text-accent-foreground` | **location**：選択中のナビ・行・タブ |
| `inverse` / `inverse-foreground` | `bg-inverse text-inverse-foreground` | **toggle**：押し込まれた切替 |
| `ring` | `ring-ring` | フォーカスの枠（背景に対して 3:1 以上） |
| `status-{info,progress,success,warning,danger}`（＋`-foreground`） | `bg-status-info text-status-info-foreground` | 状態。info＝進行中、progress＝最終段階・レビュー中、success＝完了、warning＝リスク・停滞、danger＝失敗・期限切れ |
| `category-1`〜`6`（＋`-foreground`） | `bg-category-1 text-category-1-foreground` | 分類：人、種類、タグ。1 つの画面で同じ分類に同じ番号を使う |
| `destructive` | `bg-destructive` | 削除など取り消せない操作のボタン |

状態の色と分類の色はブランド色から独立している。ブランド色を変えても意味は変わらない。

## 3. フォント（Next.js）

```tsx
// app/layout.tsx
import { Noto_Sans_JP, Noto_Sans } from "next/font/google";

const jp = Noto_Sans_JP({ weight: ["400", "500", "700"], subsets: ["latin"], variable: "--font-jp", display: "swap", preload: false });
const num = Noto_Sans({ weight: ["500", "700"], subsets: ["latin"], variable: "--font-num-src", display: "swap" });

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ja" className={`${jp.variable} ${num.variable}`} suppressHydrationWarning>
      <body className="bg-background font-sans text-base leading-relaxed text-foreground antialiased">{children}</body>
    </html>
  );
}
```

```css
/* globals.css に追加 */
@layer base {
  h1, h2, h3 { font-feature-settings: "palt"; letter-spacing: .02em; line-height: 1.35; font-weight: 700; }
}
@utility num { font-family: var(--font-num); font-variant-numeric: tabular-nums; }
```

金額・件数・日付・時刻には `num` を付ける。

Next.js 以外では、Google Fonts から `Noto+Sans+JP:wght@400;500;700` と `Noto+Sans:wght@500;700` を読み込み、`--font-jp` と `--font-num-src` に割り当てる。

## 4. 文字サイズの対応

| px | クラス | 主な用途 |
|---|---|---|
| 12 | `text-xs` | 補助ラベル、表の見出し、タグ、キー表示 |
| 14 | `text-sm` | 業務アプリの本文、ボタン、表のセル |
| 16 | `text-base` | LP・モバイルの本文、セクションの見出し、モバイルの入力欄 |
| 20 | `text-xl` | 画面タイトル、ダイアログのタイトル |
| 28 | `text-display-sm` | 2 番目に大きい数字、LP の小見出し |
| 40 | `text-display` | focal point の数字、LP のセクション見出し |
| 56 / 72 | `text-display-lg` / `text-display-xl` | LP のヒーローだけ |

`text-lg` `text-2xl` `text-3xl` などの既定サイズは使わない（audit.py が ERROR にする）。

## 5. shadcn/ui のコンポーネントの調整

palette.py の `@theme inline` で、`rounded-md` と `rounded-xl` はどちらも 8px になる。既存コンポーネントの角丸は書き換えなくてよい。次の 4 か所だけ直す。

- **Card**：`shadow-sm` を外し、枠を `border-region-border` にする。Card は region にだけ使う。item を Card で包まない。
- **Button**：主ボタン（`default`）は画面に 1 つだけにする。それ以外は `outline` / `ghost` / `secondary` を使う。
- **Badge**：状態を表すときは `variant` の代わりに `bg-status-* text-status-*-foreground` を使う。
- **Sidebar / Tabs / NavigationMenu の選択中**：`data-[active=true]:bg-accent data-[active=true]:text-accent-foreground`（shadcn の Sidebar は既定でこの形）。
- **Toggle / ToggleGroup の押下中**：`data-[state=on]:bg-inverse data-[state=on]:text-inverse-foreground`。

## 6. ダークモード

palette.py の `.dark` ブロックがそのまま使える。`next-themes` などで `html` に `class="dark"` を付ける。ダークでも役割は変わらない。影はほぼ効かないので、重なるもの（ダイアログなど）には `ring-1 ring-region-border` を足す。
