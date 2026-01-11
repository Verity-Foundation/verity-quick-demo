"""
"""
import types
from src.middleware.claim_utils import create_claim, sign_claim, store_claim


def test_end_to_end_create_sign_store(monkeypatch):
    # Create a claim from message
    issuer = "did:example:org1"
    claim = create_claim(message="end-to-end test",issuer_did=issuer)

    # Sign with fake private key -- monkeypatch sign implementation to avoid using eth_account
    def fake_sign(priv, payload):
        return "sig-fake-123"

    import src.middleware.claim_utils as claim_utils
    monkeypatch.setattr(claim_utils, "sign", fake_sign)
    claim = sign_claim(claim, "0xdeadbeef")

    # Mock middleware.store via monkeypatching the underlying function used by store_claim
    fake_resp = types.SimpleNamespace(cid="fakecid123")

    def fake_store(c):
        # assert that c is the claim (or dictlike)
        return fake_resp

    import src.middleware.claim_utils as claim_utils
    monkeypatch.setattr(claim_utils, "store", fake_store)

    cid = store_claim(claim)
    assert cid == "fakecid123"
