from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/validate', methods=['POST'])
def validate():
    # Parse the incoming AdmissionReview request
    req = request.get_json()
    if not req or 'request' not in req:
        return jsonify({"error": "Invalid request"}), 400

    admission_review = req['request']
    uid = admission_review['uid']
    object_meta = admission_review['object'].get('metadata', {})
    labels = object_meta.get('labels', {})

    # Validation Logic: Require 'billing-team' label
    allowed = True
    message = "Pod validation successful."

    if 'billing-team' not in labels:
        allowed = False
        message = "Validation failed: All pods must have the 'billing-team' label."

    # Construct the AdmissionResponse
    response = {
        "apiVersion": "admission.k8s.io/v1",
        "kind": "AdmissionReview",
        "response": {
            "uid": uid,
            "allowed": allowed,
            "status": {
                "message": message
            }
        }
    }
    
    return jsonify(response)

if __name__ == '__main__':
    # OpenShift will mount auto-generated TLS certs to this path via a Secret
    cert_path = '/tmp/k8s-webhook-server/serving-certs/tls.crt'
    key_path = '/tmp/k8s-webhook-server/serving-certs/tls.key'
    
    # Run on port 8443 (standard for webhooks)
    app.run(host='0.0.0.0', port=8443, ssl_context=(cert_path, key_path))
