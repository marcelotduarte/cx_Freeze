from Crypto.PublicKey import RSA

secret_code = "Unguessable"  # noqa: S105
key = RSA.generate(2048)
encrypted_key = key.export_key(
    passphrase=secret_code, pkcs=8, protection="scryptAndAES128-CBC"
)

with open("rsa_key.bin", "wb") as file_out:
    file_out.write(encrypted_key)

print(key.publickey().export_key().decode())
