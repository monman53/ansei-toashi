# 安政遠足侍マラソン 参加者名簿

「安政遠足侍マラソン」の参加者名簿を閲覧するウェブアプリです。

## 機能

- 氏名・よみがな検索
- 性別・都道府県・コース・仮装でフィルタ
- 知り合いフラグ（★）をブラウザに保存
- 複数年度対応

## 開発

```bash
npm install
npm run dev
```

## ビルド・ローカル確認

```bash
npm run build
npm run preview -- --host --port 3001
```

## 年度データの追加

1. `scripts/{year}/` に抽出スクリプトと PDF を配置
2. `python scripts/{year}/extract_pdf.py` を実行
3. `public/data/index.json` に年度エントリを追加
4. `main` に push → GitHub Pages へ自動デプロイ
