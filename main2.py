import random
import functools
from binascii import hexlify

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

def _eval_poly(poly, x, prime):
    return sum((coef * pow(x, power, prime)) for power, coef in enumerate(poly)) % prime

# 秘密の分割
def split_secret(secret, shares, threshold, prime=2**127 - 1):
    if threshold > shares:
        raise ValueError("Threshold must be less than or equal to the number of shares")

    poly = [secret] + [random.randint(0, prime - 1) for _ in range(threshold - 1)]
    points = [(i, _eval_poly(poly, i, prime)) for i in range(1, shares + 1)]
    return points

# ファイルから秘密を読み込み
with open('memo.txt', 'rb') as file:
    file_data = file.read()
# バイナリデータを整数に変換
secret = int.from_bytes(file_data, byteorder='big')

shares = 5
threshold = 3

# 秘密を分割
parts = split_secret(secret, shares, threshold)

# 分割されたシェアをファイルに保存
for idx, share in parts:
    with open(f'./works/share_{idx}.txt', 'wb') as share_file:
        share_file.write(share.to_bytes((share.bit_length() + 7) // 8, byteorder='big'))
        print(f"Index #{idx}: {hexlify(share.to_bytes((share.bit_length() + 7) // 8, byteorder='big'))}")
