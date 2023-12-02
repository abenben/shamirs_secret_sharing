import functools

# 有限体上の演算
def _extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = _extended_gcd(b % a, a)
        return g, x - (b // a) * y, y

def _mod_inverse(a, m):
    g, x, _ = _extended_gcd(a, m)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    else:
        return x % m

# 秘密の復元
def recover_secret(points, prime=2**127 - 1):
    def _lagrange_interpolate(x, points):
        total = 0
        for i, (xi, yi) in enumerate(points):
            prod = functools.reduce(lambda a, b: a * b,
                                    (x - xj for j, (xj, _) in enumerate(points) if i != j), 1)
            total += yi * _mod_inverse(prod, prime) * prod
        return total % prime

    return _lagrange_interpolate(0, points)

# シェアファイルを読み込む
def load_shares(file_paths):
    shares = []
    for file_path in file_paths:
        with open(file_path, 'rb') as share_file:
            share_data = share_file.read()
            idx = int(file_path.split('_')[-1].split('.')[0])
            share = int.from_bytes(share_data, byteorder='big')
            shares.append((idx, share))
    return shares

# 使用するシェアファイルのパス
file_paths = ['./works/share_1.txt', './works/share_2.txt', './works/share_3.txt']

# シェアファイルからシェアを読み込む
shares = load_shares(file_paths)

# 秘密を復元
recovered_secret = recover_secret(shares)

# 復元された秘密をバイトデータに変換
recovered_data = recovered_secret.to_bytes((recovered_secret.bit_length() + 7) // 8, byteorder='big')

# バイナリデータを文字列に変換
try:
    recovered_text = recovered_data.decode('utf-8')
    print(recovered_text)
except UnicodeDecodeError:
    print("データはテキストではないか、無効なエンコーディングです。")

# 結果の表示（またはファイルへの書き込み）
print(recovered_data)
# オプション：復元されたデータをファイルに保存する場合
# with open('recovered_memo.txt', 'wb') as file:
#     file.write(recovered_data)
