# Ionic Client SDK Changelog for Python on Windows
Generated on 2020-04-01 09:55:49 EDT.

This project follows [semantic versioning] (http://semver.org/).

<br/>

## Version 1.8.0

#### Release
- Release

#### Added
- Add documentation for Windows-specific DllMain usage limitation
- Verify agent.clone() implemented in wrappers
- new Agent constructor passing 1 String argument (SEP JSON)
- KNS - Lookup by domain provided by caller
- KNS - Add method to change active profiles server URL
- Doc - Sample to show KNS/HTTP use cases
- core SDK wrappers - new Agent constructor passing 1 String argument (SEP JSON)

#### Changed
- Move buffer-safe functions like is_strcpy (ISCryptoDLL.cpp) to common module
- Remove deprecated code from 'C' lib and have the 'C' lib link directly to the 'C++' lib instead of ISAgentSDKInternal
- Core/Wrappers: Update Log Config Example docs to be language-specific
- internal refactoring in anticipation of alternate KeyServices implementation
- IonicException improvements

#### Fixed
- Make CSV ignore minor version number changes
- Add Python SDK ionicsdk.__version__ info
- Bring consistency to ISFileCryptoCiphers with respect to encrypting already encrypted file/buffers
- Core: ISLogConfig 'maxAgeSeconds' field name is too limited
- SDK version is not present in Python SDK documentation
- Error Code 10004
- Windows HTTP library fails on non-utf8 (really non-ascii) get/post
- Python: Documentation Issues
- Enrollment on a new machine fails when the proper directories do not exist
- ionicsdk does not handle SEPs with trailing slash
- C++: Persistor/KeyVault Locking is leaving stale .lock files
- ISAgent.getKeyspace() shouldn't require an active (or any) profile
- CPP: intermittent segfault when server returns 502
- CPP: retcode 32766 on getDecryptStream on Mac
- Python: Constructors not Documented
- Whitespace at top of docs page
- Update boost library consumed by SDK and published with SDKInternal to one that is tested compatible with VS2015
- create crypto function to check available entropy
- Generic v1.3 ability to truncate a file
- Add Keepalive option to curl implementation of ISHTTP
- Update copyright block in SDK
- Python agent saveprofiles(..) function has inconsistent error handling
- More optimization work needed for Generic v1.3 fstream mode (read/write)
- Improve handling of entropy exhaustion
- Doc - Need to specify default cipher for chunkcipher
- Python Doxygen files parity with other language wrappers

#### Removed
- Remove ISCryptoSecureContainer class and ISCryptoScopedSecureClearer

## Version 1.7.2

#### Added
- New SEO header HTML in the Core SDK wrapper libraries

#### Fixed
- Doc footer copyright year
- Inconsistent Meta Description SEO values for .NET and Python

## Version 1.7.0

#### Added
- ISFileCryptoCipherOpenXML interface for cover page marking
- Custom Encrypted File test for C++ Key Vaults
- Max Age Limit - ISO 8601 duration - ISLog JSON configuration
- Random seek encrypt/decrypt in Generic 1.3 file cipher
- External signature for SDK library file hash
- ISFileCryptoCipherPdf interface for cover page marking

#### Changed
- Limit size/age of SDK log file set
- ISLog help updated with options for controlling file space and age
- Update ISLog documentation JSON examples and tables for latest features

#### Fixed
- Expose ProfilePersistor v1.1 to wrapped SDKs
- Issue accessing cryptoutils from old installations of Python
- PDF cipher error on GetFileInfo when the PDF file has external PDF Encryption
- C++ - Error logged - stream not reset on getFileInfo clear XLSX input
- OpenXML file encryption should set fail bit on output stream when a temp RAM buffer fills
- Generic v1.3 - Error when using the read/write IO interface and reading past an encryption block
- ISKeyVaultBase logic error
- FileCryptoCipherOpenXml to write temp files into platform temp directory
- CSV decryption fails on a certain size file
- Generic v1.3 - preserve write timestamp on file read
- Generic v1.3 - ability to force flush to file

## Version 1.6.1

## Version 1.6.0

#### Added
- SDK Key Services support automatic SEP lookup for non-active keyspace
- Added TLS error codes on requests that fail due to TLS errors
- SDK Documentation update for 1000 key request limit
- SDK Log callback mechanism added
- Added method to detect and destroy corrupted key vaults
- New Persistor format containing optional SALT
- New create key simulation mode
- Streamable Generic Cipher
- Streamable CSV Cipher
- New Generic Stream Cipher version 1_3
- Streamable PDF Cipher
- Streamable OpenXML Cipher
- Default Windows persistor Roaming support
- Migrate custom doc properties in OpenXML

#### Fixed
- SDK getFileInfo consumes memory
- Error when requesting multiple updates on same key id

## Version 1.5.0

#### Added
- Documentation updates across all sdk languages.

#### Changed
- Modified ISCryptoBytes to derive from new SecureAllocator class to fix bugs in heap management

#### Fixed
- Api calls now reset stream pointers on error
- Python SDK fails to encrypt non-ASCII filenames on Windows
- SDK generated temporary files no longer use tilde due to incompatibility with network based storage
- Missing Access Denied cover pages for CSV

## Version 1.4.0

#### Added
- Add support for mutable key attributes in the SDK (Python).
- Add support for external-id in the SDK (Python).
- Provide an indication of SDK version with all communications between SDK and Ionic.com.
- Custom Cover Pages - Python.
- SecretShare Persistor in Python.
- Expose key vault interfaces in Python SDK.

## Version 1.3.0

#### Added
- Added Python File/Chunk Key Services.
- Added 'Obligations' support to the GetKey and CreateKey response objects.
- Added 'Origin' support to the GetKey and CreateKey response objects.

#### Fixed
- Fixed issue with using wide characters or non-ascii as key attribute values.
- Fixed issue with encrypting large file sizes now return proper value and log an error.

## Version 1.2.1

## Version 1.2.0

#### Added
- The SDK now supports non-persistent  VDI.  Previously, the default SEP storage mechanism did not function in these environments.

#### Fixed
- An issue with parsing encrypted PDFs which have had their XMP attributes modified has been fixed.

## Version 1.0.0

#### Changed
- The Ionic SDK has been incremented to Version 1.0.0!

## Version 0.5.0

## Version 0.4.0

## Version 0.3.1

## Version 0.3.0

## Version 0.2.0

## Version 0.1.1

## Version 0.1.0
