import pyvisa

# あなたの 2110 の USB アドレスに置き換えてください
ADDR_2110 = "USB0::0x05E6::2110::1234567::INSTR"

rm = pyvisa.ResourceManager()

try:
    # 計測器を開く
    dmm = rm.open_resource(ADDR_2110)
    dmm.timeout = 5000  # ms

    # 接続確認
    print("IDN:", dmm.query("*IDN?").strip())

    # 初期化
    dmm.write("*RST")      # リセット
    dmm.write("*CLS")      # ステータスクリア

    # DC 電圧測定モードに設定
    dmm.write(":SENS:FUNC 'VOLT:DC'")
    dmm.write(":SENS:VOLT:DC:RANG:AUTO ON")   # レンジ自動

    # 1 回だけ測定
    dmm.write(":TRIG:COUN 1")      # トリガ回数 1
    dmm.write(":SAMP:COUN 1")      # サンプル数 1

    # 測定実行
    voltage_str = dmm.query(":READ?")
    voltage = float(voltage_str)

    print(f"測定された電圧: {voltage} V")

finally:
    # セッションを閉じる
    try:
        dmm.close()
    except:
        pass
