import base64
from django.conf import settings
from rest_framework import serializers
from Crypto.Cipher import AES


def encrypt(texto_plano: str) -> str:
    if not texto_plano:  # pragma: no cover
        return ''
    key = settings.KEY_ENCRY
    vector = settings.VECTOR_ENCRY
    if len(key) not in [16, 24, 32]:  # pragma: no cover
        raise serializers.ValidationError('La contraseña debe ser de 16,24 o 32 caracteres')
    if len(vector) != 16:  # pragma: no cover
        raise serializers.ValidationError('El vector debe tener 16 caracteres')
    obj = AES.new(key, AES.MODE_CFB, vector)
    ciphertext = base64.b64encode(obj.encrypt(texto_plano)).decode("utf-8")
    return ciphertext.strip()


def decrypt(enc: str) -> str:
    if not enc:  # pragma: no cover
        return ''
    key = settings.KEY_ENCRY
    vector = settings.VECTOR_ENCRY
    if len(key) not in [16, 24, 32]:  # pragma: no cover
        raise serializers.ValidationError('La contraseña debe ser de 16,24 o 32 caracteres')
    if len(vector) != 16:  # pragma: no cover
        raise serializers.ValidationError('El vector debe tener 16 caracteres')
    obj2 = AES.new(key, AES.MODE_CFB, vector)
    decrypted_text = obj2.decrypt(base64.b64decode(enc)).decode("utf-8")
    return decrypted_text
