import math
import random
from itertools import cycle


class Shifry:
    encodings = {
        'ru': {
            'encode': 'windows-1251',
            'decode': 'windows-1251',
        },
        'en': {
            'encode': 'ASCII',
            'decode': 'utf-8',
        }
    }
    alphabets = {
        'en': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
        'ru_short': 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ',
        'ru': 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ',
    }

    def ceaser(self, str, lang):
        str = str.upper()
        alpha = self.alphabets[lang]
        results = {}
        for key_num in range(len(alpha)):
            key = alpha[-key_num:] + alpha[:-key_num]
            cipher = {}
            for x in range(0, len(alpha)):
                cipher[key[x]] = alpha[x]

            cipher_text = ''
            for item in str:
                if item in alpha:
                    cipher_text += cipher[item]
                else:
                    cipher_text += item
            results[key_num] = cipher_text

        return results

    def tarabar(self, str, encrypt):
        str = str.upper()
        alphabet = 'БВГДЖЗКЛМН'
        key_cipher = 'ЩШЧЦЧФТСРП'
        if encrypt:
            alphabet, key_cipher = key_cipher, alphabet
        cipher = {}
        for x in range(0, len(alphabet)):
            cipher[key_cipher[x]] = alphabet[x]
        res = ''
        for item in str:
            if item in key_cipher:
                res += cipher[item]
            else:
                res += item
        return res

    def encode_vijn(self, text, key, lang):
        text = text.upper()
        key = key.upper()
        alpha = self.alphabets[lang]
        vijn_table = [alpha[i:] + alpha[:i] for i in range(len(alpha))]
        key_cipher = ''
        text_cipher = ''.join([x if x in alpha else '' for x in text])
        while len(text_cipher) > len(key_cipher):
            key_cipher += key
        key_cipher = key_cipher[:len(text_cipher)]
        res = ''.join(
            [vijn_table[alpha.index(text_cipher[x])][alpha.index(key_cipher[x])] for x in range(len(text_cipher))])
        for i in range(len(text)):
            if text[i] not in alpha:
                res = res[:i] + text[i] + res[i:]
        return res

    def decode_vijn(self, text, key, lang):
        text = text.upper()
        key = key.upper()
        alpha = self.alphabets[lang]
        vijn_table = [alpha[i:] + alpha[:i] for i in range(len(alpha))]
        key_cipher = ''
        text_cipher = ''.join([x if x in alpha else '' for x in text])
        while len(text_cipher) > len(key_cipher):
            key_cipher += key
        key_cipher = key_cipher[:len(text_cipher)]
        res = ''.join(
            [alpha[vijn_table[alpha.index(key_cipher[x])].index(text_cipher[x])] for x in range(len(text_cipher))])
        for i in range(len(text)):
            if text[i] not in alpha:
                res = res[:i] + text[i] + res[i:]
        return res

    def decode_tritemius(self, text, key, lang):
        text = text.upper()
        key = key.upper()
        alpha = self.alphabets[lang]
        key_cipher = ''
        text_cipher = ''.join([x if x in alpha else '' for x in text])
        while len(text_cipher) > len(key_cipher):
            key_cipher += key
        key_cipher = key_cipher[:len(text_cipher)]
        res = ''
        for i in range(len(text_cipher)):
            print([alpha.index(text_cipher[i]), alpha.index(key_cipher[i])])
            if alpha.index(text_cipher[i]) > alpha.index(key_cipher[i]):
                index_alpha = alpha.index(text_cipher[i]) - alpha.index(key_cipher[i])
            else:
                index_alpha = alpha.index(key_cipher[i]) - alpha.index(text_cipher[i])
            res += alpha[index_alpha - 1]
        return res

    def encode_tritemius(self, text, key, lang):
        text = text.upper()
        key = key.upper()
        alpha = self.alphabets[lang]
        key_cipher = ''
        text_cipher = ''.join([x if x in alpha else '' for x in text])
        while len(text_cipher) > len(key_cipher):
            key_cipher += key
        key_cipher = key_cipher[:len(text_cipher)]
        res = ''
        for i in range(len(text_cipher)):
            index_alpha = alpha.index(key_cipher[i]) + alpha.index(text_cipher[i])
            if index_alpha >= len(alpha) - 1:
                index_alpha -= (len(alpha))
            res += alpha[index_alpha + 1]
        return res

    def encode_gamma(self, text, key, lang):
        if len(lang) > 2:
            lang = 'ru'
        cipher_text = text.encode(self.encodings[lang]['encode']).hex()
        cipher_key = key.encode(self.encodings[lang]['encode']).hex()
        while len(cipher_text) > len(cipher_key):
            cipher_key += cipher_key
        cipher_key = cipher_key[:len(cipher_text)]
        string_xor_result = ''.join(hex(int(a, 16) ^ int(b, 16))[2:] for a, b in zip(cipher_text, cipher_key))
        cipher_result = bytes.fromhex(string_xor_result).decode(self.encodings[lang]['decode'])
        return cipher_result

    def encode_rsa(self, text, key):
        return (key[0], key[1], (text ** key[0]) % key[1])

    def decode_rsa(self, text, key):
        return text ** key[0] % key[1]

    def decode_rsa_without_private_key(self, n, e, cipher):
        factors = self.divide_on_factor(n)
        phi = 1;
        for x in factors:
            phi *= (x - 1)

        count, d = 1, -1
        while d == -1:
            if (count * e) % phi == 1:
                d = count
            count += 1

        return cipher ** d % n

    def generate_rsa_keys(self, num):
        p, q = 0, 0
        count = 2
        while num > p * q:
            if self.is_prime(count):
                p, q = q, p
                q = count
            count += 1

        phi = (p - 1) * (q - 1)
        simple_nums = self.generate_simple_nams(2, phi)
        e = random.choice([x for x in simple_nums if phi % x != 0])

        count, d = 0, -1
        while d == -1:
            if (count * e) % phi == 1:
                d = count
            count += 1

        return {'public': (e, p * q), 'private': (d, p * q)}

    def generate_simple_nams(self, start, end):
        import math
        nums = []
        for num in range(start, end):
            if all(num % i != 0 for i in range(start, int(math.sqrt(num)) + 1)):
                nums.append(num)
        return nums

    def is_prime(self, n):
        d = 2
        while n % d != 0:
            d += 1
        return d == n

    def divide_on_factor(self, n):
        res = []
        d = 2
        while d * d <= n:
            if n % d == 0:
                res.append(d)
                n //= d
            else:
                d += 1
        if n > 1:
            res.append(n)
        return res


if __name__ == '__main__':
    data = 501
    keys = Shifry().generate_rsa_keys(data)
    print(keys)
    rsa = Shifry().encode_rsa(data, keys['public'])
    print(f'зашифрованные данные({data}):  e={rsa[0]}, n={rsa[1]}, text={rsa[2]}')
    print(Shifry().decode_rsa(rsa[2], keys['private']))
    print(Shifry().divide_on_factor(501))
    print(Shifry().decode_rsa_without_private_key(133, 41, 11))
