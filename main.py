from src.AES import aes
from src import rabin as Rabin
from src import ecdh_key
import hashlib
import base64

def set_ecdh():
    a, b, p, xGen, yGen = 2, 2, 17, 5, 1
    curve = ecdh_key.EllipticCurve(a, b, p, xGen, yGen)
    curve.numOfPoints()
    return curve


def main():
    # Rabin's Key generation for Bob and Alice
    p_bob, q_bob, n_bob = Rabin.generate_keys_for_rabin()
    p_alice, q_alice, n_alice = Rabin.generate_keys_for_rabin()

    # Generate shared public key between Bob and Alice
    curve = set_ecdh()
    alpha_alice = curve.generatePrivateKey()
    beta_bob = curve.generatePrivateKey()

    alice_pub = ecdh_key.generatePublicKey(alpha_alice, curve)
    bob_pub = ecdh_key.generatePublicKey(beta_bob, curve)

    alice_shared = ecdh_key.generateSharedKey(bob_pub, alpha_alice, curve)
    alice_shared = str(alice_shared)
    alice_shared = hashlib.md5(alice_shared.encode('utf-8')).hexdigest()
    bob_shared = ecdh_key.generateSharedKey(alice_pub, beta_bob, curve)
    bob_shared = str(bob_shared)
    bob_shared = hashlib.md5(bob_shared.encode('utf-8')).hexdigest()



    # AES object for each client
    bob_aes = aes.AES(str(bob_shared))
    alice_aes = aes.AES(str(alice_shared))


    # **********   Bob  **********
    bob_msg = 'Hello world'
    bob_msg_hashed = hashlib.sha224(bob_msg.encode('utf-8')).hexdigest()
    sig_bob, pad_num = Rabin.sing_msg(bob_msg_hashed, p_bob, q_bob)
    msg_encrypted = bob_aes.encrypt_text(bob_msg)

    # What Bob send
    print("The message before encryption:\n{msg}\n".format(msg=bob_msg))
    base64_bytes = base64.b64encode(msg_encrypted)
    base64_message = base64_bytes.decode('ascii')
    print("The encrypted message is (in base64):\n{msg}".format(msg=base64_message))
    print("The signature is:\n{sig}\nThe padding is: {pad}\n".format(sig=sig_bob, pad=pad_num))


    # **********   Alice  **********
    msg_decrypted = alice_aes.decrypt_text(msg_encrypted)
    alice_msg_hashed = hashlib.sha224(msg_decrypted.encode('utf-8')).hexdigest()
    assert Rabin.verify(alice_msg_hashed, sig_bob, pad_num, n_bob) is True
    print("The message that received is (after decryption):\n{}".format(msg_decrypted))


main()
