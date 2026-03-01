import os
import ssl

print("Hello from cx_Freeze")
print(ssl.__name__, ssl.OPENSSL_VERSION)
ssl_paths = ssl.get_default_verify_paths()
print(ssl_paths.openssl_cafile)
print(os.environ.get("SSL_CERT_FILE"))
