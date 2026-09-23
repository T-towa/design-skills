# 公開デザインシステム・仕様書 リファレンス集

調査日: 2026-09-23 / 目的: 業務用フロントエンド向け anti-slop デザインskill（Next.js + React + shadcn/ui 風、配色調整可能）の方向性決め

凡例: **スタック**＝公開実装の有無（`React` / `WC`=Web Components / `Figma`=Figmaのみ / `Doc`=ドキュメントのみ / `—`=未確認）
**密度**＝情報密度の傾向（高=データ密・業務向け、中、低=余白多め）

---

## A. 静謐・モノクロ・ミニマル（開発者ツール系）
shadcn/ui との親和性が最も高い系統。色を極力使わず、階調・罫線・タイポで構造を作る。

| 名前 | 運営 | URL | スタック | 密度 | 感性メモ |
|---|---|---|---|---|---|
| Geist | Vercel | https://vercel.com/geist/introduction | Doc（React内部） | 中 | グレースケール10段＋機能色。Geist Sans/Mono。shadcn/ui の源流的な美意識 |
| Linear Brand | Linear | https://linear.app/brand | Doc（ブランドのみ） | 高 | 公式DSは非公開。低彩度インディゴ、背景の輝度レイヤリング、Inter の字形設定 |
| Supabase Design System | Supabase | https://supabase.com/design-system | React | 中 | ほぼモノクロ＋エメラルド1色。ダーク基調の開発者向けUI |
| shadcn/ui Theming | shadcn | https://ui.shadcn.com/docs/theming | React | 中 | CSS変数＋OKLCHのトークン設計。今回の実装基盤 |
| GitHub Primer | GitHub | https://primer.style/ | React | 高 | 機能色の意味体系（fg/bg/border × role）が秀逸。コード・一覧中心UIの手本 |

## B. 堅実エンタープライズ・高密度（データ／管理画面）
業務UIの「型」を学ぶ系統。テーブル、フォーム、フィルタ、空状態などのパターン文書が厚い。

| 名前 | 運営 | URL | スタック | 密度 | 感性メモ |
|---|---|---|---|---|---|
| Carbon | IBM | https://carbondesignsystem.com/ | React / WC | 高 | 2x Grid、IBM Plex、角丸ゼロ。硬質で理知的。データ可視化ガイドも充実 |
| Cloudscape | AWS | https://cloudscape.design/ | React | 高 | AWSコンソールの基盤。業務パターン（テーブル・ウィザード・分割ビュー）の文書が最も実践的 |
| Atlassian Design System | Atlassian | https://atlassian.design/ | React | 中〜高 | トークン命名体系・エレベーション定義が参考になる |
| Ant Design | Alibaba | https://ant.design/ | React | 高 | 中国圏業務UIの標準。網羅性は最強だが「Antっぽさ」が出やすい点は反面教師にも |
| Semi Design | ByteDance | https://semi.design/ | React | 高 | Ant の対抗。テーマ生成（DSM）で配色カスタムを前提にした設計 |
| Elastic UI (EUI) | Elastic | https://eui.elastic.co/ | React | 高 | ログ・検索・ダッシュボード特化。密度調整の知見 |
| Salesforce Lightning | Salesforce | https://www.lightningdesignsystem.com/ | Doc / WC | 高 | CRMの王道。デザイントークンという概念の元祖 |
| Grafana Saga | Grafana Labs | https://grafana.com/developers/saga/ | React | 高 | 監視ダッシュボード。ダークテーマ前提の配色設計 |
| DRUIDS | Datadog | https://druids.datadoghq.com/ | — | 高 | 大量メトリクス表示の密度感 |
| Helios | HashiCorp | https://helios.hashicorp.design/ | Ember | 中 | インフラ管理UIのパターン文書（Patterns章）が丁寧 |
| Pajamas | GitLab | https://design.gitlab.com/ | Vue | 高 | 文言（Voice & tone）・UIテキストのガイドが詳細 |
| Fluent 2 | Microsoft | https://fluent2.microsoft.design/ | React | 中 | Office/Teams 系。業務ツールの王道 |

## C. 日本の業務SaaS（和文組版・日本の業務慣習）
日本語UIの行間・字間・フォント選定、和文の文言ルールが学べる。業務フロントエンドなら最重要カテゴリ。

| 名前 | 運営 | URL | スタック | 密度 | 感性メモ |
|---|---|---|---|---|---|
| SmartHR Design System | SmartHR | https://smarthr.design/ | React（smarthr-ui） | 中 | 国内の先駆け。基本原則・ライティングガイド・アクセシビリティまで一貫。業務SaaSの最有力参考 |
| vibes | freee | https://vibes.freee.co.jp/ | React | 中 | 会計業務UI。アクセシビリティ推進が設計の軸 |
| Money Forward Design / MFUI | マネーフォワード | https://design.moneyforward.com/ | 社内（非公開） | 高 | MFUI本体は非公開。[紹介スライド](https://speakerdeck.com/taigakiyokawa/introducing-money-forward-ui)、[MCP化の記事](https://zenn.dev/moneyforward/articles/43bcef16b033f8)が参考 |
| One Design System | Sansan | https://ui.one-design-system.sansan.com/ | — | 中 | 名刺・契約管理の複数プロダクト横断 |
| FALCON | ユーザベース（SPEEDA） | https://www.figma.com/community/file/1047401907024695662 | Figma | 高 | 経済情報プラットフォーム。高密度な表・チャート |
| sugao | カオナビ | https://www.figma.com/ja-jp/community/file/1388050089826010129/sugao | Figma | 中 | 人事管理SaaS |
| kamii | ラクスル | https://designsystem.raksul.com/ | — | 中 | 印刷EC＋業務 |
| Ubie Vitals | Ubie | https://vitals.ubie.life/ | React（Ubie UI, OSS） | 中 | 医療。トーン＆マナー、原則の言語化が明快 |
| Serendie | 三菱電機 | https://serendie.design/ | React | 中 | 大企業の横断DS。カラーテーマ切替を前提にした設計 |
| Sparkle Design | Goodpatch | https://sparkle-design.goodpatch.com/sparkle-design | Figma | 中 | デザイン会社によるテンプレート的DS |

## D. フィンテック・信頼感
「お金を扱うUI」の安心感。余白・数値表示・状態表現の扱いが緻密。

| 名前 | 運営 | URL | スタック | 密度 | 感性メモ |
|---|---|---|---|---|---|
| PayPay App Style Guide | PayPay | https://app-style-guide.paypay.ne.jp/app-styleguide | Doc | 低〜中 | 主にPayPay連携ミニアプリ開発者向け。本体DSは社内。設計思想は [Inside-Out記事](https://insideout.paypay.ne.jp/en/2021/08/03/professionals-vol13-en/) 参照 |
| Toss Design System (TDS) | Toss（韓国） | https://tossmini-docs.toss.im/tds-mobile/ | React / RN | 低〜中 | 「アジア圏で最も洗練されたフィンテックUI」とよく挙がる。タイポ主導でノイズを削る姿勢 |
| Wise Design | Wise | https://wise.design/ | Doc | 中 | 送金・為替。明快な色使いと数値表示 |
| Stripe Apps Design | Stripe | https://docs.stripe.com/stripe-apps/design | React（UI toolkit） | 中 | 本体DS（Sail）は非公開。ダッシュボード拡張のUIキットとパターンが公開 |

## E. 温かみ・フレンドリー（業務でも硬すぎない）

| 名前 | 運営 | URL | スタック | 密度 | 感性メモ |
|---|---|---|---|---|---|
| Polaris | Shopify | https://polaris-react.shopify.com/ → 現行: https://shopify.dev/docs/api/app-home/polaris-web-components | WC | 中 | 商人（非専門家）向け管理画面。業務UIの親しみやすさの基準点 |
| Braid | SEEK | https://seek-oss.github.io/braid-design-system/ | React | 中 | テーマ切替前提。レイアウトプリミティブ（Stack/Inline/Columns）設計が美しい |
| Paste | Twilio | https://paste.twilio.design/ | React | 中 | ガイドライン文章の質が高い（コンテンツ／パターン） |
| Garden | Zendesk | https://garden.zendesk.com/ | React | 中 | サポート業務UI |
| Gestalt | Pinterest | https://gestalt.pinterest.systems/ | React | 低〜中 | アクセシビリティ文書が詳細 |
| Nord | Nordhealth | https://nordhealth.design/ | WC | 中 | 医療SaaS。北欧的な抑制と温かみ |
| Seeds | Sprout Social | https://seeds.sproutsocial.com/ | React | 中 | SNS運用管理。色とイラストの柔らかさ |
| Spindle | サイバーエージェント（Ameba） | https://spindle.ameba.design/ | React | 低〜中 | 国内。ブランド表現とアクセシビリティの両立 |
| Pepabo Design (Inhouse) | GMOペパボ | https://design.pepabo.com/ | — | 中 | 国内。複数サービス横断 |
| charcoal | pixiv | https://pixiv.github.io/charcoal/ | React | 中 | 国内。クリエイター向けのやわらかさ |

## F. 公共・アクセシビリティ最優先
「装飾を削っても伝わる」基準。anti-slop の最低ラインを決めるのに有効。

| 名前 | 運営 | URL | スタック | 密度 | 感性メモ |
|---|---|---|---|---|---|
| デジタル庁デザインシステム | デジタル庁 | https://design.digital.go.jp/dads/ | Figma / HTML | 中 | CC BY 4.0 で誰でも利用可。和文タイポ・カラー・フォームの規定が日本語で最も体系的 |
| GOV.UK Design System | 英国政府 | https://design-system.service.gov.uk/ | HTML/Nunjucks | 低 | 「フォームは1画面1問」など、実証ベースのパターン。装飾ゼロの美学 |
| USWDS | 米国政府 | https://designsystem.digital.gov/ | HTML | 中 | カラートークンの「グレード」体系（コントラスト保証）が配色設計の参考になる |

## G. プラットフォーム基盤（参照規範）

| 名前 | 運営 | URL | スタック | 感性メモ |
|---|---|---|---|---|
| Human Interface Guidelines | Apple | https://developer.apple.com/jp/design/human-interface-guidelines/ | Doc | 階層・余白・モーションの原則 |
| Material 3 | Google | https://m3.material.io/ | Doc / Web | 動的カラー（HCT色空間）による配色生成ロジック。「Materialっぽさ」は避けたいが理論は有用 |
| Spectrum | Adobe | https://spectrum.adobe.com/ | React | プロ向けツールの高密度UI、カラーシステムの科学的設計 |

## H. 個性派・エディトリアル（刺激用）

| 名前 | 運営 | URL | 感性メモ |
|---|---|---|---|
| Base | Uber | https://base.uber.com/ | 黒白の強いコントラスト。React実装（baseui）あり |
| Washington Post DS | Washington Post | https://build.washingtonpost.com/ | 新聞的タイポグラフィ。データ表示の品位 |
| BBC GEL | BBC | https://www.bbc.co.uk/gel/guidelines | 報道UIの明快さ |
| Mozilla Protocol | Mozilla | https://protocol.mozilla.org/ | オープンな空気感 |
| Momentum | Cisco | https://momentum.design/en/ | 会議・コラボ系 |
| LINE Design System | LINE | https://designsystem.line.me/ | アジア圏メッセンジャーの親しみ |
| 一休 Design Guideline | 一休 | https://www.ikyu.co.jp/design_guideline | 国内高級予約。上質さの言語化 |
| Duolingo Brand | Duolingo | https://design.duolingo.com/ | 対極の「遊び」。業務には使わないが境界確認用 |

---

## 配色調整・skill構築の周辺ツール

| 名前 | URL | 用途 |
|---|---|---|
| tweakcn | https://tweakcn.com/ | shadcn/ui 用ビジュアルテーマエディタ（OKLCH / Tailwind v4 対応） |
| Radix Colors | https://www.radix-ui.com/colors | 12段階スケール＋用途定義。shadcn配色の下地に最適 |
| awesome-design-md (VoltAgent) | https://github.com/voltagent/awesome-design-md | 有名サイトのデザインを DESIGN.md 化したエージェント向け集。**既存skillが「AIっぽい」理由の研究材料にも** |
| awesome-claude-design (VoltAgent) | https://github.com/VoltAgent/awesome-claude-design | 同上、Claude向け |
| ソシオメディア HIG | https://www.sociomedia.co.jp/category/shig | 日本語の UI 原則コラム集（OOUI など業務UI設計論） |

## まとめ記事（追加で漁る場合）
- [デザインシステム・ガイドライン集 2026（Zenn）](https://zenn.dev/15/articles/1899635124a266)
- [コンポーネントが公開されている日本のデザインシステムまとめ 2025（note）](https://note.com/kerm/n/n583d691437fd)
- [日本・海外のデザインシステム総まとめ 56事例（note）](https://note.com/akane_desu/n/n2e564f6561b4)
- [日本発の「いけてる」デザインシステム事例10選（Goodpatch）](https://goodpatch.com/blog/2024-07-10cooldesignsystems)
- [実装が公開されているデザインシステム一覧（Zenn）](https://zenn.dev/hiromichinomata/articles/da75218fa8e8ab)

## 調査上の注意
- **PayPay**: 公開されているのは連携開発者向けスタイルガイド。PayPayアプリ本体のDSは社内のみ。
- **Linear / Stripe / マネーフォワード**: 本体DSは非公開。ブランドページ・周辺キット・登壇資料から読み解く必要あり。
- スタック欄の「—」は今回未確認。skill化の段階で個別に確認する。
