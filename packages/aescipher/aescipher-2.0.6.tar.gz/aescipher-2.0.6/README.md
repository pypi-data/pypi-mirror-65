# AES Cipher

<badges>[![version](https://img.shields.io/pypi/v/aescipher.svg)](https://pypi.org/project/aescipher/)
[![license](https://img.shields.io/pypi/l/aescipher.svg)](https://pypi.org/project/aescipher/)
[![pyversions](https://img.shields.io/pypi/pyversions/aescipher.svg)](https://pypi.org/project/aescipher/)  
[![donate](https://img.shields.io/badge/Donate-Paypal-0070ba.svg)](https://paypal.me/foxe6)
[![powered](https://img.shields.io/badge/Powered%20by-UTF8-red.svg)](https://paypal.me/foxe6)
[![made](https://img.shields.io/badge/Made%20with-PyCharm-red.svg)](https://paypal.me/foxe6)
</badges>

<i>Use AES-256 to encrypt everything with ease!</i>

# Hierarchy

```
aescipher
'---- AESCipher()
    |---- encrypt()
    '---- decrypt()
```

# Example

## python
```python
from aescipher import *
key = "abc" or b"abc"
plaintext = "abc" or b"abc"
ciphertext = AESCipher(key).encrypt(plaintext)
print(ciphertext)
# ZxFrL1kMlMc/7TWrMiSS3gyZCikhvVhoXxChFdKKlf0=
print(plaintext == AESCipher(key).decrypt(ciphertext))
# True
```

## shell
```shell script
rem aescipher.exe {e|d} <key> {<plaintext in string>|<ciphertext in b64>}
aescipher.exe e "abc" "abc"
aescipher.exe d "abc" "ZxFrL1kMlMc/7TWrMiSS3gyZCikhvVhoXxChFdKKlf0="
```
