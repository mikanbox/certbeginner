# certbeginner
display cert info simply





# Usage
## Setup
### Install from 'setup.py'
pip install setup.py

### Install from LocalFile to Test
pip install --editable .  


## Sample


## Todo
RFC 5280 の Section 4.1 から抜粋した、証明書構造定義における　signatureValue　の取得方法を見つける.
これを取得しないと Verifyができない
```
    Certificate  ::=  SEQUENCE  {
        # tbsCertificate       TBSCertificate,
        # signatureAlgorithm   AlgorithmIdentifier,
        # signatureValue       BIT STRING  }
```


