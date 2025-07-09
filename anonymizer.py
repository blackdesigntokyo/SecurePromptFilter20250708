import regex as re
import json
import random
import os

def load_anonymization_config(config_path="anonymization_config.json"):
    """
    匿名化設定ファイルを読み込む
    """
    if not os.path.exists(config_path):
        print(f"エラー: 設定ファイル '{config_path}' が見つかりません。")
        print("指定されたパスに 'anonymization_config.json' を配置してください。")
        exit()
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    print(f"✅ 設定ファイル '{config_path}' を読み込みました。")
    return config

def anonymize_prompt(prompt_text: str, config: dict) -> str:
    """
    プロンプト内のセキュアな情報をダミーに置き換える
    """
    anonymized_text = prompt_text

    # 1. 固定置換を最優先で適用
    if "fixed_replacements" in config:
        for original, dummy in config["fixed_replacements"].items():
            anonymized_text = anonymized_text.replace(original, dummy)

    # 2. 正規表現パターンによる置換を適用
    if "patterns" in config:
        for p in config["patterns"]:
            regex = p["regex"]
            replacements = p["replacements"]
            
            # 正規表現オブジェクトをコンパイル
            compiled_regex = re.compile(regex)

            # マッチした部分をランダムなダミーに置き換える関数
            def replace_match(match):
                dummy_word = random.choice(replacements)
                
                # 会社名パターンとその他のパターンでロジックを分岐
                # 会社名タイプの場合、マッチした会社名全体をダミーに置き換える
                # (例: "田中工業株式会社" を "企業X" に置き換える)
                if p["type"] == "company_jp_prefix" or p["type"] == "company_jp_suffix":
                    return dummy_word
                else:
                    # その他のタイプはマッチ全体をダミーに置き換え (メール、電話、氏名など)
                    return dummy_word

            anonymized_text = compiled_regex.sub(replace_match, anonymized_text)
            
    return anonymized_text

def main():
    # 設定ファイルの読み込み
    config = load_anonymization_config()

    print("\n--- プロンプト匿名化ツール ---")
    print("プロンプトを入力してください。終了するには 'exit' または '終了' と入力してください。")

    while True:
        user_input = input("\nあなたのプロンプト: ")

        if user_input.lower() in ["exit", "終了"]:
            print("ツールを終了します。")
            break

        if not user_input.strip():
            continue

        # プロンプトを匿名化
        anonymized_prompt = anonymize_prompt(user_input, config)

        print("\n--- 匿名化されたプロンプト ---")
        print(anonymized_prompt)
        print("----------------------------")

if __name__ == "__main__":
    main()