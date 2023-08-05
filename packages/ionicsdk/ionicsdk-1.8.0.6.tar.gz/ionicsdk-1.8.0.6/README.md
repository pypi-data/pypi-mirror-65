# Ionic Python SDK

## Overview
This module provides Python developers with access to the core services of the Ionic Platform.  At a high level, the platform provides developers with straightforward methods to
* Securely create and retrieve data protection keys
* Use these keys to encrypt or decrypt application data
* Encrypt or decrypt arbitrary files
* Enroll users and devices with the Ionic backend system.

## Quick Start
Assuming you have access to an Ionic account, the Python environment makes it very simple to access some central features of the platform.   The example below assumes you have already enrolled your system and have a default peristor.

```python
import ionicsdk                            # top level module for all Ionic classes

plaintext = "Welcome to the Python SDK"    # create some text to encrypt
agent = ionicsdk.Agent()                   # the "Agent" class provides access to several common services.

cipher = ionicsdk.ChunkCipherV1(agent)     # a "cipher" object provides "encrypt" and "decrypt" operations.
                                           # it uses the supplied "agent" to create and retrieve keys.
ciphertext = cipher.encryptstr(plaintext)
print ciphertext
decrypted = cipher.decryptstr(ciphertext)
print decrypted
```
If you don't already have access to an Ionic environment, you can enroll in a "Community Tenant" on the Ionic Developer Portal as explained in the next section.

## Additional Information
The Ionic Python SDK distribution includes online documentation for the classes and methods.   You can review this documentation by browsing to the "index.html" file within the "docs" directory.

In order to use the SDK, you will need to enroll in one or more "Ionic tenants".  If you don't already have an established tenant, Ionic provides a "Community Tenant" that you can use as you become familiar with the environment.   You can find additional information about accessing the Community Tenant and about developing for the Ionic platform [here](http://dev.ionic.com "Ionic Developer Portal").
