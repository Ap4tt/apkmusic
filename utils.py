def input_integer(prompt, min_val):
    while True:
        try:
            val = int(input(prompt))
            if val < min_val:
                print(f"  [!] Invalid: Angka minimal adalah {min_val}.")
                continue
            return val
        except ValueError:
            print("  [!] Invalid: Masukkan format angka yang benar.")

def input_string(prompt):
    while True:
        val = input(prompt).strip()
        if not val:
            print("  [!] Invalid: Input tidak boleh kosong.")
            continue
        return val