## このファイルについて

このファイルは Claude Code がプロジェクトを理解するための仕様書です。機能追加・変更・削除を行った際は、このファイルも同時に更新してください。

## プロジェクト概要

「安政遠足侍マラソン」の参加者名簿を閲覧するフロントエンドのみのウェブアプリケーションです。GitHub Pages で公開し、複数年度の名簿に対応します。知り合いフラグはブラウザの localStorage に保存されます。

## 技術スタック

- **フロントエンド**: Vue 3 (Composition API) + Vite 5 + Vue Router 4 (ハッシュモード)
- **ホスティング**: GitHub Pages（`/ansei-toashi/` ベースパス）
- **デプロイ**: GitHub Actions（`main` ブランチへの push で自動ビルド・デプロイ）
- **ローカル確認**: `npm run preview -- --host --port 3001`

## データ構造

年度ごとの静的JSONファイルを `public/data/` に配置する。

```
public/data/
├── index.json                 # 年度一覧
└── 2026/
    └── participants.json      # 第52回（1,478件）
```

### `public/data/index.json`

```json
[
  { "year": 2026, "label": "第52回", "file": "2026/participants.json" }
]
```

### `participants.json` のフィールド

| フィールド | 型 | 説明 |
|---|---|---|
| no | number | 参加者番号（コース内番号） |
| name | string | 氏名 |
| name_kana | string | 読み仮名（カタカナ） |
| gender | string | 男性／女性 |
| prefecture | string | 都道府県 |
| costume | string | 仮装する／仮装しない |
| times | number\|null | 参加回数 |
| course | string | 峠コース／関所・坂本宿コース |
| source_page | number | 元PDFのページ番号（21–59） |

## ファイル構成

```
├── .github/workflows/deploy.yml  # GitHub Pages 自動デプロイ
├── public/data/                  # 静的参加者データ
├── src/
│   ├── App.vue                   # ナビゲーション・年度セレクタ・グローバルCSS
│   ├── main.js                   # Vueアプリ初期化（ハッシュモードルーター）
│   ├── pages/ViewPage.vue        # 参加者一覧ページ
│   └── components/SortIcon.vue  # ソートアイコン
├── vite.config.js                # base='/ansei-toashi/'、allowedHosts: true
└── package.json                  # 依存: vue, vue-router（バックエンド依存なし）
```

## 機能仕様

### 閲覧ページ（ViewPage.vue）

- 年度データを初回1回フェッチし、以降のフィルタ・ソートはクライアント側 `computed` で即時処理
- **フィルター**: 氏名・読み検索、性別、都道府県、コース、仮装、知り合いのみ
- **ソート**: No、氏名（読み順）、回数、コース
- **知り合いフラグ**: ★/☆ボタンでトグル、`localStorage` キー `ansei-toashi-friends-{year}` に `"{course}:{no}"` の配列として保存
- **行番号**: 現在の表示順で左端に表示

### App.vue（年度管理）

- `public/data/index.json` から年度一覧を取得
- 年度セレクタ（複数年度ある場合のみ表示）
- 選択中の年度を `localStorage` キー `ansei-toashi-selected-year` に保存
- 選択年度の `yearMeta` を `ViewPage` に props で渡す

## 起動方法

### 開発

```bash
npm run dev     # Vite devサーバー（http://localhost:5173/ansei-toashi/）
```

### ローカル本番確認

```bash
npm run build
npm run preview -- --host --port 3001
# → http://localhost:3001/ansei-toashi/
# → http://<LAN-IP>:3001/ansei-toashi/
```

### GitHub Pages デプロイ

`main` ブランチに push すると GitHub Actions が自動でビルド・デプロイ。
Settings → Pages → Source: GitHub Actions を有効にすること。

## 年度データの追加手順

1. `scripts/{year}/` ディレクトリを作成し、抽出スクリプトと PDF を配置
2. `python scripts/{year}/extract_pdf.py` を実行 → `public/data/{year}/participants.json` が生成される
3. 必要に応じて `name_kana` を OCR 等で補完
4. `public/data/index.json` に年度エントリを追加
5. `main` に push → 自動デプロイ

### スクリプト構成

```
scripts/
└── 2026/
    ├── extract_pdf.py   # PDF → JSON 抽出（pdfplumber 使用）
    └── program2026.pdf  # 元PDF（.gitignore 対象、リポジトリ外管理）
```

`extract_pdf.py` は `scripts/{year}/` から実行。出力先は `public/data/{year}/participants.json`。

## UI設計方針

- 色数を最小限に（CSS変数: `--primary: #2A2A2A`、`--friend-color: #B03030`）
- 絵文字を使わない
- スマホ対応（仮装列・コース列などを `hidden-sm` で非表示）
- テーブルの sticky ヘッダーは `border-collapse: separate` + スクロールコンテナで実現
