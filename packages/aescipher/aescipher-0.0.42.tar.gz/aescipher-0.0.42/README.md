# AES Cipher

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
# gZ46WXSNkc9isggV31YQ0YKwT3luFvgYwzetERtTW2g=
print(plaintext == AESCipher(key).decrypt(ciphertext))
# True
```

## shell
```shell script
rem aescipher.exe {e|d} <key> {<plaintext>|<ciphertext>}
aescipher.exe e "abc" "abc"
aescipher.exe d "abc" "gZ46WXSNkc9isggV31YQ0YKwT3luFvgYwzetERtTW2g="
```
