import base64
import random
import string
from typing import Dict, List

from .fixtures import walletclient  # noqa: F401


def random_walletname() -> str:
    choices = string.ascii_letters + string.digits
    return "".join(random.choice(choices) for i in range(40))


def random_passphrase() -> str:
    return "".join(
        "".join(
            random.choice(req)
            for i in range(5)
        )
        for req in [
            string.ascii_uppercase,
            string.ascii_lowercase,
            string.digits,
            string.punctuation
        ]
    )


def random_metadata() -> List[Dict[str, str]]:
    return [
        {
            "key": "".join(
                random.choice(string.ascii_uppercase)
                for i in range(10)),
            "value": "".join(
                random.choice(string.ascii_lowercase)
                for i in range(10))
        }
    ]


def test_walletclient(walletclient):  # noqa: F811
    walletname = random_walletname()
    passphrase = random_passphrase()

    # Create wallet
    r = walletclient.create(walletname, passphrase)
    assert r.status_code == 200
    j = r.json()
    assert "token" in j, "Bad response: {}".format(j)

    # Log out
    r = walletclient.logout()
    assert r.status_code == 200
    j = r.json()
    assert "success" in j, "Bad response: {}".format(j)
    assert j["success"] is True

    # Log in
    r = walletclient.login(walletname, passphrase)
    assert r.status_code == 200
    j = r.json()
    assert "token" in j, "Bad response: {}".format(j)

    # Generate keypair
    meta = random_metadata()
    r = walletclient.generatekey(passphrase, meta)
    assert r.status_code == 200
    j = r.json()
    assert "key" in j, "Bad response: {}".format(j)
    k = j["key"]
    assert len(k["pub"]) == 64  # ED25519 pubKey is 32 bytes

    # List keypairs
    r = walletclient.listkeys()
    assert r.status_code == 200
    j = r.json()
    assert "keys" in j, "Bad response: {}".format(j)
    assert len(j["keys"]) == 1

    # Get one keypair
    r = walletclient.getkey(k["pub"])
    assert r.status_code == 200
    j = r.json()
    assert "key" in j, "Bad response: {}".format(j)
    k2 = j["key"]
    assert k2 == k

    # Sign tx
    blob = b"abc123"
    tx = base64.b64encode(blob).decode("ascii")
    r = walletclient.signtx(tx, k["pub"])
    assert r.status_code == 200
    j = r.json()
    assert "signedTx" in j, "Bad response: {}".format(j)
    signedTx = j["signedTx"]
    assert signedTx["pubKey"] == k["pub"]
    assert signedTx["data"] == tx
    # TODO: check signature

    # Update key metadata
    meta2 = random_metadata()
    r = walletclient.updatekeymetadata(k["pub"], passphrase, meta2)
    assert r.status_code == 200
    j = r.json()
    assert "success" in j, "Bad response: {}".format(j)
    assert j["success"] is True

    # Get one keypair, again
    r = walletclient.getkey(k["pub"])
    assert r.status_code == 200
    j = r.json()
    assert "key" in j, "Bad response: {}".format(j)
    k3 = j["key"]
    assert k3["meta"] == meta2

    # Taint key
    r = walletclient.taintkey(k["pub"], passphrase)
    assert r.status_code == 200, "Bad response: {}".format(r.text)
    j = r.json()
    assert "success" in j, "Bad response: {}".format(j)
    assert j["success"] is True
