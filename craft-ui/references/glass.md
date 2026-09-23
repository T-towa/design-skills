# 素材：ガラス（Liquid Glass・すりガラス・Acrylic）

ユーザーがガラスの質感を求めたときだけ使う。根拠は Apple Human Interface Guidelines の Materials（Liquid Glass）と、Fluent 2 の Material（Acrylic / Mica / Smoke）。

## どこに使うか
- ガラスは **操作とナビゲーションの層** だけに使う：上部バー、タブバー、浮かぶ操作バー、コマンドパレット、クイックビュー、ポップオーバー。
- 表・フォーム・本文・活動履歴などの **内容の層** は、不透明（`bg-card`）のままにする。
- ガラスの上にガラスを重ねない。ガラスの中に置くタブ・入力欄・カードは不透明の面にする。
- 長く表示される土台（サイドバー全体、ページの地）は不透明にする。一時的に出るもの（ポップオーバー、パレット、クイックビュー）は、不透明度を上げた厚いガラスにする。
- モーダルの背後は、暗い半透明の幕（`bg-black/30`、ダークは `/50`）で覆い、下を操作できないことを示す。
- 色付きのガラスは 1 か所だけ（例：ナビゲーションのレールをブランド色で着色）。主ボタンは不透明の `bg-primary` のまま。

## 値
```css
.glass {
  background:
    linear-gradient(180deg, rgb(255 255 255 / .38), transparent 46%),   /* 上部の反射 */
    color-mix(in srgb, var(--card) 56%, transparent);                    /* 不透明度 56% 以上 */
  backdrop-filter: blur(22px) saturate(170%);
  -webkit-backdrop-filter: blur(22px) saturate(170%);
  border: 1px solid rgb(255 255 255 / .72);
  box-shadow: inset 0 1px 0 rgb(255 255 255 / .9), 0 10px 30px rgb(0 0 0 / .14);
}
.glass-thick { background: linear-gradient(180deg, rgb(255 255 255 / .38), transparent 40%), color-mix(in srgb, var(--card) 84%, transparent); }
.dark .glass {
  background: linear-gradient(180deg, rgb(255 255 255 / .07), transparent 46%), color-mix(in srgb, var(--card) 52%, transparent);
  border-color: rgb(255 255 255 / .12);
  box-shadow: inset 0 1px 0 rgb(255 255 255 / .12), 0 12px 32px rgb(0 0 0 / .45);
}
@media (prefers-reduced-transparency: reduce) {
  .glass, .glass-thick { background: var(--card); backdrop-filter: none; -webkit-backdrop-filter: none; border-color: var(--region-border); }
}
```

- ガラスの下に、ぼかしで透けて見えるもの（内容のスクロール、控えめな色の面）がないと、ガラスは灰色の板に見えるだけになる。内容がガラスの下を通り抜ける配置（上部バーの下をスクロール）にする。
- 角丸は入れ子で同心円状にそろえる：外側の角丸 = 内側の角丸 + 余白。この場合だけ、4 / 8px 以外の値（例：外側 20px）を使ってよい。audit.py の該当 ERROR は、この理由で残してよい。
- SVG の displacement を使った屈折の表現は Chromium でしか動かないので使わない。

## 確認
- ガラスの上の文字は、背景が最も明るいとき・最も暗いときの両方で 4.5:1 以上になること。足りなければ不透明度を上げる。
- OS の「透明度を下げる」設定で、不透明に切り替わること。
