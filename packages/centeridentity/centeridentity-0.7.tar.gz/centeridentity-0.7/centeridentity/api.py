import requests
import binascii
import base58
import base64
import os
import hashlib
from coincurve.keys import PrivateKey
from coincurve import verify_signature


class User:
    @classmethod
    def from_dict(cls, data):
        inst = cls()
        inst.public_key = data['public_key']
        inst.username = data['username']
        inst.username_signature = data['username_signature']
        return inst


class Service(User):
    domain = 'http://0.0.0.0:8000'
    @classmethod
    def generate(cls, username):
        inst = cls()
        num = os.urandom(32).hex()
        inst.wif = cls.to_wif(num)
        inst.key = PrivateKey.from_hex(num)
        inst.public_key = inst.key.public_key
        inst.username = username
        inst.username_signature = base64.b64encode(inst.key.sign(inst.username.encode("utf-8"))).decode("utf-8")
        return inst

    @classmethod
    def revive(cls, username, wif):
        inst = cls()
        inst.wif = wif
        inst.key = PrivateKey.from_hex(binascii.hexlify(base58.b58decode(wif))[2:-10].decode())
        inst.public_key = inst.key.public_key
        inst.username = username
        inst.username_signature = inst.generate_service_username_signature()
        return inst

    def generate_service_username_signature(self):
        signature = self.key.sign(self.username.encode('utf-8'))
        return base64.b64encode(signature).decode('utf-8')

    @classmethod
    def to_wif(cls, private_key: str):
        # to wif
        private_key_static = private_key
        extended_key = "80" + private_key_static + "01"
        first_sha256 = hashlib.sha256(binascii.unhexlify(extended_key)).hexdigest()
        second_sha256 = hashlib.sha256(binascii.unhexlify(first_sha256)).hexdigest()
        final_key = extended_key + second_sha256[:8]
        return base58.b58encode(binascii.unhexlify(final_key)).decode('utf-8')

    def api_call(self, endpoint, data):
        api_token = requests.post(
            '{}{}'.format(self.domain, '/get-api-token'),
            {
                'bulletin_secret': self.username_signature
            }).json()
        if not api_token.get('api_uuid'):
            return {'status': 'error', 'message': 'api error'}
        request_signature = base64.b64encode(self.key.sign(api_token['api_uuid'].encode())).decode("utf-8")
        return requests.post(
            '{}{}'.format(self.domain, endpoint),
            data,
            headers={
                'Authorization': 'basic {}'.format(
                    base64.b64encode(
                        '{}:{}'.format(
                            self.username_signature,
                            request_signature
                        ).encode()
                    ).decode("utf-8")
                )
            }
        ).json()


class CenterIdentity:
    def __init__(self, service, username=None):
        self.service = service

    @classmethod
    def create_service(cls, username):
        return Service.generate(username)

    @classmethod
    def revive_service(cls, username, wif):
        return Service.revive(username, wif)

    @classmethod
    def revive_user(cls, data):
        return User.from_dict(data)

    def add_user(self, user):
        return self.service.api_call(
            '/add-user',
            {
                'user_public_key': user.public_key,
                'user_bulletin_secret': user.username_signature,
                'user_username': user.username,
                'service_public_key': self.service.public_key,
                'service_bulletin_secret': self.service.username_signature,
                'service_username': self.service.username
            }
        )

    def get_user(self, user):
        return self.service.api_call(
            '/get-user',
            {
                'user_public_key': user.public_key,
                'user_bulletin_secret': user.username_signature,
                'user_username': user.username,
                'service_public_key': self.service.public_key,
                'service_bulletin_secret': self.service.username_signature,
                'service_username': self.service.username
            }
        )

    def remove_user(self, user):
        return self.service.api_call(
            '/remove-user',
            {
                'user_public_key': user.public_key,
                'user_bulletin_secret': user.username_signature,
                'user_username': user.username,
                'service_public_key': self.service.public_key,
                'service_bulletin_secret': self.service.username_signature,
                'service_username': self.service.username
            }
        )

    @classmethod
    def authenticate(cls, signature, session_id, user, hash_session_id=False):
        if not isinstance(user, User):
            user = User.from_dict(user)
        if hash_session_id:
            session_id = hashlib.sha256(session_id.encode()).hexdigest()
        return verify_signature(
            base64.b64decode(signature),
            session_id.encode(),
            bytes.fromhex(user.public_key)
        )
