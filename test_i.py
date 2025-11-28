import pyvisa
import time

# あなたの 6221 の GPIB アドレスに書き換えてください
ADDR_6221 = "GPIB0::18::INSTR"

# 設定したい電流値 [A]
TARGET_CURRENT = 1e-6   # 1 µA

rm = pyvisa.ResourceManager()

try:
    # 6221 を開く
    src = rm.open_resource(ADDR_6221)
    src.timeout = 5000  # ms

    # 接続確認
    print("IDN:", src.query("*IDN?").strip())

    # 初期化（安全のため）
    src.write("*RST")          # リセット
    src.write("*CLS")          # ステータスクリア
    src.write(":SOUR:FUNC CURR")          # 電流ソース
    src.write(":SOUR:CURR:MODE FIX")      # DC 固定電流
    src.write(":SOUR:CURR:RANG:AUTO ON")  # レンジ自動
    src.write(":SOUR:CURR:COMP 10")       # コンプライアンス電圧 = 10 V

    # 出力 OFF の状態で電流指定
    src.write(":OUTP OFF")
    src.write(f":SOUR:CURR {TARGET_CURRENT}")

    # 出力 ON
    src.write(":OUTP ON")
    print(f"電流を {TARGET_CURRENT} A に設定しました")

    # 1秒だけ待つ（装置の動作確認用）
    time.sleep(10)

    # 出力 OFF（安全のため）
    src.write(":OUTP OFF")
    print("出力を OFF にしました")

finally:
    try:
        src.close()
    except:
        pass

