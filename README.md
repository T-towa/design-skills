# design skills

業務アプリ・LP・モバイル画面のための Claude Code 用デザイン skill と、その調査・比較用のモック。

## 構成
- `craft-ui/` … skill 本体（`SKILL.md`、`references/`、`scripts/`、`assets/`）
- `claudedocs/` … 調査メモと比較モック（デザインシステム一覧、13 システムの CRM 比較、ガラス版、リロード風、業務版）

## インストール
```bash
ln -sfn "$(pwd)/craft-ui" ~/.claude/skills/craft-ui
```
新しい会話から自動で使われる。明示的に呼ぶ場合は `/craft-ui`。

## スクリプト
```bash
python3 craft-ui/scripts/palette.py --brand "#0b63c5"          # ブランド色から shadcn/ui 用の配色（ライト・ダーク）＋コントラスト検査
python3 craft-ui/scripts/audit.py src/ --surface app            # 文字サイズ・太さ・角丸・余白のスケール外れを検出（app | lp | mobile）
```
