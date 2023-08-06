"""The module that implements block encryption according to GOST 34.12-2015
   ('Kuznechik' and 'Magma').

   Author: Evgeny Drobotun (c) 2020
   License: MIT

"""

from struct import pack

from gostcrypto.utils import add_xor
from gostcrypto.utils import zero_fill
from gostcrypto.utils import S_BOX
from gostcrypto.utils import S_BOX_REVERSE

__all__ = ['GOST34122015Kuznechik', 'GOST34122015Magma']

_BLOCK_SIZE_KUZNECHIK = 16
_BLOCK_SIZE_MAGMA = 8
_KEY_SIZE = 32

#Constants for linear transformation in the 'Kuznechik' cipher
_L = bytearray([
    0x01, 0x94, 0x20, 0x85, 0x10, 0xc2, 0xc0, 0x01,
    0xfb, 0x01, 0xc0, 0xc2, 0x10, 0x85, 0x20, 0x94,
])

#Constants for nonlinear bijective transformation in the 'Magma' cipher
_S_BOX_MAGMA = (
    (0x0c, 0x04, 0x06, 0x02, 0x0a, 0x05, 0x0b, 0x09,
     0x0e, 0x08, 0x0d, 0x07, 0x00, 0x03, 0x0f, 0x01,),
    (0x06, 0x08, 0x02, 0x03, 0x09, 0x0a, 0x05, 0x0c,
     0x01, 0x0e, 0x04, 0x07, 0x0b, 0x0d, 0x00, 0x0f,),
    (0x0b, 0x03, 0x05, 0x08, 0x02, 0x0f, 0x0a, 0x0d,
     0x0e, 0x01, 0x07, 0x04, 0x0c, 0x09, 0x06, 0x00,),
    (0x0c, 0x08, 0x02, 0x01, 0x0d, 0x04, 0x0f, 0x06,
     0x07, 0x00, 0x0a, 0x05, 0x03, 0x0e, 0x09, 0x0b,),
    (0x07, 0x0f, 0x05, 0x0a, 0x08, 0x01, 0x06, 0x0d,
     0x00, 0x09, 0x03, 0x0e, 0x0b, 0x04, 0x02, 0x0c,),
    (0x05, 0x0d, 0x0f, 0x06, 0x09, 0x02, 0x0c, 0x0a,
     0x0b, 0x07, 0x08, 0x01, 0x04, 0x03, 0x0e, 0x00,),
    (0x08, 0x0e, 0x02, 0x05, 0x06, 0x09, 0x01, 0x0c,
     0x0f, 0x04, 0x0b, 0x00, 0x0d, 0x0a, 0x03, 0x07,),
    (0x01, 0x07, 0x0e, 0x0d, 0x00, 0x05, 0x08, 0x03,
     0x04, 0x0f, 0x0a, 0x06, 0x09, 0x0c, 0x0b, 0x02,)
)

class GOST34122015Kuznechik:
    """Class that implements block encryption in accordance with GOST 34.12-2015 ('Kuznechik').

       Methods:
          :decrypt(): decrypting a block of ciphertext.
          :encrypt(): encrypting a block of plaintext.
          :clear(): Сlearing the values of iterative encryption keys.

       Attributes:
          :block_size: an integer value the internal block size of the cipher algorithm in bytes.
          :key_size: an integer value the cipher key size.
    """
    def __init__(self, key):
        """Initialize the ciphering object.

           Args:
              :key: Cipher key.
        """
        self._cipher_c = []
        self._cipher_iter_key = []
        self._cipher_get_c()
        key_1 = key[:_KEY_SIZE // 2]
        key_2 = key[_KEY_SIZE // 2:]
        internal = bytearray(_KEY_SIZE // 2)
        self._cipher_iter_key.append(key_1)
        self._cipher_iter_key.append(key_2)
        for i in range(4):
            for j in range(8):
                internal = add_xor(key_1, self._cipher_c[i * 8 + j])
                internal = GOST34122015Kuznechik._cipher_s(internal)
                internal = GOST34122015Kuznechik._cipher_l(internal)
                key_1, key_2 = [add_xor(internal, key_2), key_1]
            self._cipher_iter_key.append(key_1)
            self._cipher_iter_key.append(key_2)
        key_1 = bytearray(self.key_size // 2)
        key_2 = bytearray(self.key_size // 2)
        key = bytearray(self.key_size)

    def __del__(self):
        #Delete the ciphering object
        self.clear()

    @staticmethod
    def _cipher_s(data):
        #The S-transformation function (nonlinear bijective transformation)
        result = bytearray(_BLOCK_SIZE_KUZNECHIK)
        for i in range(_BLOCK_SIZE_KUZNECHIK):
            result[i] = S_BOX[data[i]]
        return result

    @staticmethod
    def _cipher_s_reverse(data):
        #The reverse S-transformation function (reverse nonlinear bijective transformation)
        result = bytearray(_BLOCK_SIZE_KUZNECHIK)
        for i in range(_BLOCK_SIZE_KUZNECHIK):
            result[i] = S_BOX_REVERSE[data[i]]
        return result

    @staticmethod
    def _cipher_gf(op_a, op_b):
        #The GF-transformation function
        result = 0
        for _ in range(8):
            if op_b & 1:
                result = result ^ op_a
            hi_bit = op_a & 0x80
            op_a = op_a << 1
            if hi_bit:
                op_a = op_a ^ 0x1c3
            op_b = op_b >> 1
        return result

    @staticmethod
    def _cipher_r(data):
        #The R-transformation function
        a_0 = 0
        result = bytearray(_BLOCK_SIZE_KUZNECHIK)
        for i in range(_BLOCK_SIZE_KUZNECHIK):
            result[i] = data[i - 1]
            a_0 = a_0 ^ GOST34122015Kuznechik._cipher_gf(result[i], _L[i])
        result[0] = a_0
        return result

    @staticmethod
    def _cipher_r_reverse(data):
        #The reverse R-transformation function
        a_15 = 0
        result = bytearray(_BLOCK_SIZE_KUZNECHIK)
        for i in range(_BLOCK_SIZE_KUZNECHIK - 1, -1, -1):
            result[i - 1] = data[i]
            a_15 = a_15 ^ GOST34122015Kuznechik._cipher_gf(data[i], _L[i])
        result[15] = a_15
        return result

    @staticmethod
    def _cipher_l(data):
        #The L-transformation function (linear transformation)
        result = bytearray(_BLOCK_SIZE_KUZNECHIK)
        result = data
        for _ in range(16):
            result = GOST34122015Kuznechik._cipher_r(result)
        return result

    @staticmethod
    def _cipher_l_reverse(data):
        #The reverse L-transformation function (reverse linear transformation)
        result = bytearray(_BLOCK_SIZE_KUZNECHIK)
        result = data
        for _ in range(16):
            result = GOST34122015Kuznechik._cipher_r_reverse(result)
        return result

    def _cipher_get_c(self):
        #The generate iteration constants C
        for i in range(1, 33):
            internal = bytearray(_BLOCK_SIZE_KUZNECHIK)
            internal[15] = i
            self._cipher_c.append(GOST34122015Kuznechik._cipher_l(internal))

    @property
    def block_size(self):
        """An integer value the internal block size of the cipher algorithm in bytes.
           For the 'Kuznechik' algorithm this value is 16 and the 'Magma' algorithm,
           this value is 8.
        """
        return _BLOCK_SIZE_KUZNECHIK

    @property
    def key_size(self):
        """An integer value the cipher key size.
        """
        return _KEY_SIZE

    def decrypt(self, block):
        """Decrypting a block of ciphertext.

           Args:
             :block: The block of ciphertext to be decrypted (the block size is 16 bytes).

           Return:
              The block of plaintext.
        """
        block = bytearray(block)
        block = add_xor(self._cipher_iter_key[9], block)
        for i in range(8, -1, -1):
            block = GOST34122015Kuznechik._cipher_l_reverse(block)
            block = GOST34122015Kuznechik._cipher_s_reverse(block)
            block = add_xor(self._cipher_iter_key[i], block)
        return block

    def encrypt(self, block):
        """Encrypting a block of plaintext.

           Args:
             :block: The block of plaintext to be encrypted (the block size is 16 bytes).

           Return:
              The block of ciphertext.
        """
        block = bytearray(block)
        for i in range(9):
            block = add_xor(self._cipher_iter_key[i], block)
            block = GOST34122015Kuznechik._cipher_s(block)
            block = GOST34122015Kuznechik._cipher_l(block)
        block = add_xor(self._cipher_iter_key[9], block)
        return block

    def clear(self):
        """Сlearing the values of iterative encryption keys.
        """
        for i in range(10):
            self._cipher_iter_key[i] = zero_fill(len(self._cipher_iter_key[i]))

class GOST34122015Magma:
    """Class that implements block encryption in accordance with GOST 34.12-2012 ('Magma').

       Methods:
          :decrypt(): decrypting a block of ciphertext.
          :encrypt(): encrypting a block of plaintext.
          :clear(): Сlearing the values of iterative encryption keys.

       Attributes:
          :block_size: an integer value the internal block size of the cipher algorithm in bytes.
          :key_size: an integer value the cipher key size.
    """
    def __init__(self, key):
        """Initialize the ciphering object.

           Args:
              :key: Cipher key.
        """
        self._cipher_iter_key = []
        iter_key = b''
        for j in range(8):
            iter_key = bytearray(4)
            for i in range(4):
                iter_key[i] = key[(j * 4) + i]
            self._cipher_iter_key.append(iter_key)
        for j in range(8):
            iter_key = bytearray(4)
            for i in range(4):
                iter_key[i] = key[(j * 4) + i]
            self._cipher_iter_key.append(iter_key)
        for j in range(8):
            iter_key = bytearray(4)
            for i in range(4):
                iter_key[i] = key[(j * 4) + i]
            self._cipher_iter_key.append(iter_key)
        for j in range(8):
            iter_key = bytearray(4)
            for i in range(4):
                iter_key[i] = key[28 - (j * 4) + i]
            self._cipher_iter_key.append(iter_key)
        iter_key = zero_fill(len(iter_key))
        key = zero_fill(len(key))

    def __del__(self):
        self.clear()

    @staticmethod
    def _cipher_t(data):
        #The T-transformation function
        result = bytearray(4)
        data = bytearray(data)
        for i in range(4):
            first_part_byte = data[i] & 0x0f
            sec_part_byte = (data[i] & 0xf0) >> 4
            first_part_byte = _S_BOX_MAGMA[(3 - i) * 2][first_part_byte]
            sec_part_byte = _S_BOX_MAGMA[(3 - i) * 2 + 1][sec_part_byte]
            result[i] = (sec_part_byte << 4) | first_part_byte
        return result

    @staticmethod
    def _cipher_add_32(op_a, op_b):
        #Addition operation in the residue ring modulo 32
        op_a = bytearray(op_a)
        op_b = bytearray(op_b)
        internal = 0
        result = bytearray(4)
        for i in range(3, -1, -1):
            internal = op_a[i] + op_b[i] + (internal >> 8)
            result[i] = internal & 0xff
        return result

    @staticmethod
    def _cipher_g(cipher_k, cipher_a):
        #The g-transformation function
        cipher_k = bytearray(cipher_k)
        cipher_a = bytearray(cipher_a)
        internal = bytearray(4)
        result = bytearray(4)
        result_32 = 0
        internal = GOST34122015Magma._cipher_add_32(cipher_k, cipher_a)
        internal = GOST34122015Magma._cipher_t(internal)
        result_32 = internal[0]
        result_32 = (result_32 << 8) + internal[1]
        result_32 = (result_32 << 8) + internal[2]
        result_32 = (result_32 << 8) + internal[3]
        result_32 = (result_32 << 11)|(result_32 >> 21)
        result_32 = result_32 & 0xffffffff
        result = pack('>I', result_32)
        return result

    @staticmethod
    def _cipher_g_prev(cipher_k, cipher_a):
        #The preliminary G-transform function
        cipher_k = bytearray(cipher_k)
        cipher_a = bytearray(cipher_a)
        a_0 = bytearray(4)
        a_1 = bytearray(4)
        cipher_g = bytearray(4)
        result = bytearray(_BLOCK_SIZE_MAGMA)
        a_1 = cipher_a[0:4]
        a_0 = cipher_a[4:_BLOCK_SIZE_MAGMA]
        cipher_g = GOST34122015Magma._cipher_g(cipher_k, a_0)
        cipher_g = add_xor(a_1, cipher_g)
        a_1 = a_0
        a_0 = cipher_g
        result[0:4] = a_1
        result[4:_BLOCK_SIZE_MAGMA] = a_0
        return result

    @staticmethod
    def _cipher_g_fin(cipher_k, cipher_a):
        #The final G-transform function
        cipher_k = bytearray(cipher_k)
        cipher_a = bytearray(cipher_a)
        a_0 = bytearray(4)
        a_1 = bytearray(4)
        cipher_g = bytearray(4)
        result = bytearray(_BLOCK_SIZE_MAGMA)
        a_1 = cipher_a[0:4]
        a_0 = cipher_a[4:_BLOCK_SIZE_MAGMA]
        cipher_g = GOST34122015Magma._cipher_g(cipher_k, a_0)
        cipher_g = add_xor(a_1, cipher_g)
        a_1 = cipher_g
        result[0:4] = a_1
        result[4:_BLOCK_SIZE_MAGMA] = a_0
        return result

    @property
    def block_size(self):
        """An integer value the internal block size of the cipher algorithm in bytes.
           For the 'Kuznechik' algorithm this value is 16 and the 'Magma' algorithm,
           this value is 8.
        """
        return _BLOCK_SIZE_MAGMA

    @property
    def key_size(self):
        """An integer value the cipher key size.
        """
        return _KEY_SIZE

    def decrypt(self, block):
        """Decrypting a block of plaintext.

           Args:
             :block: The block of plaintext to be encrypted (the block size is 8 bytes).

           Return:
              The block of ciphertext.
        """
        result = bytearray(_BLOCK_SIZE_MAGMA)
        result = GOST34122015Magma._cipher_g_prev(self._cipher_iter_key[31], block)
        for i in range(30, 0, -1):
            result = GOST34122015Magma._cipher_g_prev(self._cipher_iter_key[i], result)
        result = GOST34122015Magma._cipher_g_fin(self._cipher_iter_key[0], result)
        return result

    def encrypt(self, block):
        """Encrypting a block of ciphertext.

           Args:
             :block: The block of ciphertext to be decrypted (the block size is 8 bytes).

           Return:
              The block of plaintext.
        """
        result = bytearray(_BLOCK_SIZE_MAGMA)
        result = GOST34122015Magma._cipher_g_prev(self._cipher_iter_key[0], block)
        for i in range(1, 31):
            result = GOST34122015Magma._cipher_g_prev(self._cipher_iter_key[i], result)
        result = GOST34122015Magma._cipher_g_fin(self._cipher_iter_key[31], result)
        return result

    def clear(self):
        """Сlearing the values of iterative encryption keys.
        """
        for i in range(32):
            self._cipher_iter_key[i] = zero_fill(len(self._cipher_iter_key[i]))
