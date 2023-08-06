# AES Cipher

<i>Use AES-256 to encrypt everything with ease!</i>

# Hierarchy

```
aes_cipher
'---- AESCipher()
    |---- encrypt()
    '---- decrypt()
```

# Example

## python
```python
from aes_cipher import *
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
rem aes_cipher.exe {e|d} <key> {<plaintext>|<ciphertext>}
aes_cipher.exe e "abc" "abc"
aes_cipher.exe d "abc" "gZ46WXSNkc9isggV31YQ0YKwT3luFvgYwzetERtTW2g="
```
