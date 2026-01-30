# Business Intel Scraper (Powered by Gemini 2.5)

## 概要 / Overview
指定したキーワードに基づいてWeb上の最新情報を収集し、**Google Gemini 2.5 (最新AIモデル)** を用いてビジネス向けレポートを自動生成するインテリジェンス・ツールです。
手動でのリサーチ時間を90%削減し、意思決定に必要な重要インサイトを瞬時に抽出します。

## 主な機能 / Features
* **Automated Research:** DuckDuckGo検索により、国・地域を指定した高精度な情報収集（日本国内の最新事例に特化）。
* **AI Analysis:** 最新鋭の `Gemini 2.5 Flash` を採用し、記事の要約・メリット・リスクを論理的に構造化。
* **Fallback System:** 検索エラーやAPI制限時にも動作を保証する堅牢なエラーハンドリング（デモモード搭載）。
* **Security:** 環境変数によるAPIキー管理で、セキュアな運用が可能。

## 技術スタック / Tech Stack
* **Language:** Python 3.10+
* **AI Engine:** Google Gemini 2.5 Flash (via REST API direct implementation)
* **Libraries:** `requests`, `beautifulsoup4`, `duckduckgo-search`

## 出力サンプル / Sample Report
[実際の生成レポートはこちら (sample_report.md)](./sample_report.md)

## 開発者 / Developer
**Ichinokura-Dev**
* "Technology meets Literature" - 論理的実装と文脈理解を融合させたソリューションを提供します。
