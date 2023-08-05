"""Various cryptographics functions.
"""
import ionicsdk._private as _private

def sha256(inbytes):
    """!Generate a SHA256 hash code
        
    @param
        inbytes (bytes): The data to hash
        
    @return
        (bytes) The 256 bit hash as a byte array
    """
    # inputs
    cInputData = _private.CMarshalUtil.bytesToC(inbytes)

    # outputs
    cOutputLen = 32
    cOutputData = _private.POINTER(_private.ARRAY(_private.c_ubyte, cOutputLen))()
    cOutputData.contents = (_private.c_ubyte * cOutputLen)()

    
    # call into C library to perform the work
    _private.cLib.ionic_crypto_sha256(
          cInputData,
          _private.cast(cOutputData, _private.POINTER(_private.c_ubyte)),
          cOutputLen)

    # marshal C outputs to Python
    return _private.string_at(cOutputData, cOutputLen)

def hmac_sha256(inbytes, keybytes):
    """!Generate a HMAC_SHA256 hash code
        
    @param
        inbytes (bytes): The data to hash
    @param 
        keybytes (bytes): The key bytes
        
    @return
        (bytes) The 256 bit hash as a byte array
    """

    # inputs
    cInputData = _private.CMarshalUtil.bytesToC(inbytes)
    cKeyBytes = _private.CMarshalUtil.bytesToC(keybytes)

    # outputs
    cOutputLen = 32
    cOutputData = _private.POINTER(_private.ARRAY(_private.c_ubyte, cOutputLen))()
    cOutputData.contents = (_private.c_ubyte * cOutputLen)()

    
    # call into C library to perform the work
    _private.cLib.ionic_crypto_hmac_sha256(
        cInputData,
        cKeyBytes,
        _private.cast(cOutputData, _private.POINTER(_private.c_ubyte)),
        cOutputLen)

    # marshal C outputs to Python
    return _private.string_at(cOutputData, cOutputLen)
    
def sha512(inbytes):
    """!Generate a SHA512 hash code
        
    @param
        inbytes (bytes): The data to hash
        
    @return
        (bytes) The 256 bit hash as a byte array
    """

    # inputs
    cInputData = _private.CMarshalUtil.bytesToC(inbytes)

    # outputs
    cOutputLen = 64
    cOutputData = _private.POINTER(_private.ARRAY(_private.c_ubyte, cOutputLen))()
    cOutputData.contents = (_private.c_ubyte * cOutputLen)()

    
    # call into C library to perform the work
    _private.cLib.ionic_crypto_sha512(
        cInputData,
        _private.cast(cOutputData, _private.POINTER(_private.c_ubyte)),
        cOutputLen)

    # marshal C outputs to Python
    return _private.string_at(cOutputData, cOutputLen)

def hmac_sha512(inbytes, keybytes):
    """!Generate a HMAC_SHA512 hash code
        
    @param
        inbytes (bytes): The data to hash
    @param
        keybytes (bytes): The key bytes
        
    @return
        (bytes) The 256 bit hash as a byte array
    """

    # inputs
    cInputData = _private.CMarshalUtil.bytesToC(inbytes)
    cKeyBytes = _private.CMarshalUtil.bytesToC(keybytes)

    # outputs
    cOutputLen = 64
    cOutputData = _private.POINTER(_private.ARRAY(_private.c_ubyte, cOutputLen))()
    cOutputData.contents = (_private.c_ubyte * cOutputLen)()

    
    # call into C library to perform the work
    _private.cLib.ionic_crypto_hmac_sha512(
        cInputData,
        cKeyBytes,
        _private.cast(cOutputData, _private.POINTER(_private.c_ubyte)),
        cOutputLen)

    # marshal C outputs to Python
    return _private.string_at(cOutputData, cOutputLen)
    
def pbkdf2(inbytes, saltbytes, iterations, hashlen):
    """!Performs the PBKDF2 key derivation algorithm on provided input bytes and optional salt
    
    @param
        inbytes (bytes): The data to hash
    @param
        saltbytes (bytes): The salt bytes
    @param
        iterations (int): The number of iterations (must be greater than zero)
    @param
        hashlen (int): The length of the desired output hash length, which must be greater than
            zero. The computed hash will be this length.
    
    @return
        (bytes) The output bytes
    """

    # inputs
    cInputData = _private.CMarshalUtil.bytesToC(inbytes)
    cSaltBytes = _private.CMarshalUtil.bytesToC(saltbytes)
    cIterations = iterations
    
    # outputs
    cOutputLen = hashlen
    cOutputData = _private.POINTER(_private.ARRAY(_private.c_ubyte, cOutputLen))()
    cOutputData.contents = (_private.c_ubyte * cOutputLen)()

    
    # call into C library to perform the work
    _private.cLib.ionic_crypto_pbkdf2(
        cInputData,
        cSaltBytes,
        cIterations,
        _private.cast(cOutputData, _private.POINTER(_private.c_ubyte)),
        cOutputLen,
        cOutputLen)

    # marshal C outputs to Python
    return _private.string_at(cOutputData, cOutputLen)
    
