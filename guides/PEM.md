# PEM Format

PEM format is [Privacy Enhanced Mail](https://en.wikipedia.org/wiki/Privacy-Enhanced_Mail).
You probably know it to look like files with content like:

```pem
-----BEGIN <CRYPTOGRAPHIC TYPE>-----
...base64 encoded binary data...
-----END <CRYPTOGRAPHIC TYPE>-----
```

- These files [Base64 encode](https://en.wikipedia.org/wiki/Base64) binary data of Cryptographics _Keys_ and _Certificates_ 
- The binary data is encoding data structures using [DER (Distinguished Encoding Rules X.690)](https://en.wikipedia.org/wiki/X.690#DER_encoding). This is widely used in X.509 for SSL/TLS certificates.
- These binary data structures are an implentation of [ASN.1 (Abstract Syntax Notation)](https://en.wikipedia.org/wiki/ASN.1) to define abstract data structures that are both machine and human readable.

# Generate RSA Key pairs

```sh
openssl genrsa -out private_key.pem 2048
openssl rsa -in private_key.pem -pubout -out public_key.pem
```

# Trim key to single line

```sh
export PRIVATE_KEY=$(cat private_key.pem | sed '/-----BEGIN .*-----/d;/-----END .*-----/d' | tr -d '\n')
export PUBLIC_KEY=$(cat public_key.pem | sed '/-----BEGIN .*-----/d;/-----END .*-----/d' | tr -d '\n')
```
