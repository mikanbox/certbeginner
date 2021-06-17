#!/usr/bin/env python
import argparse
import socket
from OpenSSL import SSL
from OpenSSL import crypto
import certifi
from pprint import pprint
import json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode',help='Mode')
    parser.add_argument('arg1',help='URL to connect')
    args = parser.parse_args()
    print('arg1='+args.arg1)
    print('mode='+args.mode)

    certs = get_server_certificates("www.google.com")



# https://www.pyopenssl.org/en/stable/api/crypto.html#x509-objects
    for (idx, cert) in certs:
        # print(type(cert))
        print(crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode('utf-8'))

        print ("version", cert.get_version())
        print ("シリアル番号", cert.get_serial_number())
        print ("署名アルゴリズム", cert.get_signature_algorithm())
        print ("発行者", cert.get_issuer().commonName)
        print ("有効期限開始日", cert.get_notBefore())
        print ("有効期限終了日", cert.get_notAfter())
        print ("サブジェクト", cert.get_subject().commonName)
        print ("公開鍵", cert.get_pubkey())
        print ("署名以外の部分の証明書から作成したダイジェスト（ハッシュ）",cert.digest("sha256"))



# ref : https://www.pyopenssl.org/en/stable/api/crypto.html#x509extension-objects
        extensions = (cert.get_extension(i) for i in range(cert.get_extension_count()))
        extension_data = {}
        for e in extensions:
            # print(str(e) + "\n")
            # print(e.get_short_name().decode('utf-8'),",",e.get_data())
            # print(e.get_short_name().decode('utf-8'),",")
            # print(e.__str__())

            extension_data.update({e.get_short_name().decode('utf-8'):e.__str__()})
        pprint(extension_data)
        print(json.dumps(extension_data, ensure_ascii=False, indent=2))

        print("============================")

    
# どうやら、Pythonだと、証明書に含まれる署名を出すのは面倒臭そう
# openssl x509 -text -noout -in test.crt として末尾に出てくる署名をPythonで取得したいが、一旦オブジェクトに変換すると厳しそう
# algorithm https://ja.wikipedia.org/wiki/X.509

# メッセージのハッシュ + 署名からダイジェスト作成
# つまり　print ("署名以外の部分の証明書から作成したダイジェスト（ハッシュ）",cert.digest("sha256"))　と　署名部分からverifyした値が一致すればOK



def get_server_certificates(hostname):
    context = SSL.Context(method=SSL.TLSv1_2_METHOD)
    context.load_verify_locations(cafile=certifi.where())
    conn = SSL.Connection(context, socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    conn.settimeout(5)
    conn.connect((hostname, 443))
    conn.setblocking(1)
    conn.do_handshake()
    conn.set_tlsext_host_name(hostname.encode())
    certs = enumerate(conn.get_peer_cert_chain())
    conn.close()
    return certs




if __name__ == "__main__":
    main()