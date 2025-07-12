from flask import Flask, request, jsonify
import bitcoin
import binascii

app = Flask(__name__)

@app.route('/scan', methods=['POST'])
def scan():
    try:
        keys = request.json.get("keys", [])
        results = []

        for key_hex in keys:
            try:
                key_hex = key_hex.lower()
                privkey_bytes = binascii.unhexlify(key_hex)
                if len(privkey_bytes) != 32:
                    raise Exception("Invalid length")
                pubkey = bitcoin.privkey_to_pubkey(privkey_bytes)
                address = bitcoin.pubkey_to_address(pubkey)
                results.append({ "key": key_hex, "address": address })
            except:
                results.append({ "key": key_hex, "error": "Invalid format or processing error" })

        return jsonify({ "results": results })
    except Exception as e:
        return jsonify({ "error": str(e) }), 400

if __name__ == '__main__':
    app.run(debug=True)
