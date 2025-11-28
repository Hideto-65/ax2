import pyvisa

rm = pyvisa.ResourceManager()

print("Detected resources:")
for r in rm.list_resources():
    print("  ", r)

# Optional: 各デバイスにIDN?を送る
for r in rm.list_resources():
    inst = rm.open_resource(r)
    try:
        print(r, " → ", inst.query("*IDN?"))
    except:
        print(r, " → 応答なし")
    finally:
        inst.close()
