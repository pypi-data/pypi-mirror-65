import time
import os
import unittest
import shutil
import jwt
from iot_gw.device import Device
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.backends import default_backend as crypto_default_backend


temp_dir="./.workdir"

class TestDevice(unittest.TestCase):

    def setUp(self):
        #create temporary folder
        shutil.rmtree(temp_dir,ignore_errors=True)
        os.mkdir(temp_dir)

    def tearDown(self):
        shutil.rmtree(temp_dir,ignore_errors=True)
    
    def test_get_token(self):
        device = Device('device_id')
        # check token is well-formatted
        token = device.get_token('project_id',1)
        self.assertIsNotNone(token)
        decodedToken = jwt.decode(
            token,
            device.get_public_key(),
            algorithms='RS256',
            options={'verify_aud': False}
        )
        self.assertEqual(decodedToken['aud'],'project_id')
        self.assertEqual(decodedToken['exp'] - decodedToken['iat'], 60)
        # check token is not generated each time
        token2 = device.get_token('project_id')
        self.assertEqual(token,token2)
        
    
    def test_get_token_expired(self):
        device = Device('device_id')
        token = device.get_token('project_id',minutes=0,seconds=1)
        # check a new token is generated when the previous is expired
        time.sleep(2)
        token2 = device.get_token('project_id')
        self.assertNotEqual(token,token2)

    def test_get_token_with_key_pair_provided(self):
        key = rsa.generate_private_key(
            backend=crypto_default_backend(),
            public_exponent=65537,
            key_size=2048
        )
        public_key = key.public_key().public_bytes(
            crypto_serialization.Encoding.PEM,
            crypto_serialization.PublicFormat.PKCS1
        )
        private_key = key.private_bytes(
            crypto_serialization.Encoding.PEM,
            crypto_serialization.PrivateFormat.PKCS8,
            crypto_serialization.NoEncryption()
        )
        with open(os.path.join(temp_dir,'project_id_private.pem'),'wb') as private_key_file:
            private_key_file.write(private_key)
        with open(os.path.join(temp_dir,'project_id_public.pem'),'wb') as public_key_file:
            public_key_file.write(public_key)
        device = Device('project_id',temp_dir)
        token = device.get_token('project_id',1)
        self.assertIsNotNone(token)
        decodedToken = jwt.decode(
            token,
            public_key,
            algorithms='RS256',
            options={'verify_aud': False}
        )
        self.assertEqual(decodedToken['aud'],'project_id')
        self.assertEqual(decodedToken['exp'] - decodedToken['iat'], 60)

    def test_dump(self):
        device = Device('test_dump')
        device.dump(temp_dir)
        for file in ['test_dump_private.pem','test_dump_public.pem']:
            self.assertTrue(os.path.isfile(os.path.join(temp_dir,file)))

    def test_fetch(self):
        key = rsa.generate_private_key(
            backend=crypto_default_backend(),
            public_exponent=65537,
            key_size=2048
        )
        public_key = key.public_key().public_bytes(
            crypto_serialization.Encoding.PEM,
            crypto_serialization.PublicFormat.PKCS1
        )
        private_key = key.private_bytes(
            crypto_serialization.Encoding.PEM,
            crypto_serialization.PrivateFormat.PKCS8,
            crypto_serialization.NoEncryption()
        )
        with open(os.path.join(temp_dir,'test_fetch_private.pem'),'wb') as private_key_file:
            private_key_file.write(private_key)
        with open(os.path.join(temp_dir,'test_fetch_public.pem'),'wb') as public_key_file:
            public_key_file.write(public_key)
        device = Device('test_fetch')
        device.fetch(temp_dir)
        self.assertEqual(public_key,device.get_public_key())
        self.assertEqual(private_key,device.get_private_key())





        

if __name__ == '__main__':
    unittest.main()
