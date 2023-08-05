from ionicsdk._common import *

cLib.ionic_crypto_sha256.argtypes = [POINTER(CBytes), POINTER(c_ubyte), c_size_t]
cLib.ionic_crypto_sha256.restype = c_int
cLib.ionic_crypto_sha256.errcheck = ctypesFunctionErrorCheck

cLib.ionic_crypto_sha512.argtypes = [POINTER(CBytes), POINTER(c_ubyte), c_size_t]
cLib.ionic_crypto_sha512.restype = c_int
cLib.ionic_crypto_sha512.errcheck = ctypesFunctionErrorCheck

cLib.ionic_crypto_hmac_sha256.argtypes = [POINTER(CBytes), POINTER(CBytes), POINTER(c_ubyte), c_size_t]
cLib.ionic_crypto_hmac_sha256.restype = c_int
cLib.ionic_crypto_hmac_sha256.errcheck = ctypesFunctionErrorCheck

cLib.ionic_crypto_hmac_sha512.argtypes = [POINTER(CBytes), POINTER(CBytes), POINTER(c_ubyte), c_size_t]
cLib.ionic_crypto_hmac_sha512.restype = c_int
cLib.ionic_crypto_hmac_sha512.errcheck = ctypesFunctionErrorCheck

cLib.ionic_crypto_pbkdf2.argtypes = [POINTER(CBytes), POINTER(CBytes), c_size_t, POINTER(c_ubyte), c_size_t, c_size_t]
cLib.ionic_crypto_pbkdf2.restype = c_int
cLib.ionic_crypto_pbkdf2.errcheck = ctypesFunctionErrorCheck
