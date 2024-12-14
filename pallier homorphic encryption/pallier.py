# import random

# import modarithmetic
# import rabin

# class PrivateKey:
#     """
#     PrivateKey object contains λ and μ
#     in accordance to the Paillier Cryptosystem
    
#     args:
#         p: a prime number
#         q: another prime number
#         (p and q are of equal length)
#         n: product of p and q
        
#     attributes:
#         λ: lowest common multiple of p-1 and q-1
#         ∵ p and q are of equal length we can use the simplification,
#         μ: modular multiplicative inverse of λ and n
#     """
    
#     def __init__(self, p, q, n):

#         self.λ = modarithmetic.lcm( p-1, q-1)
#         self.μ = modarithmetic.multiplicative_inverse( self.λ, n)
        
#     def __repr__(self):
#         return ("---\nPrivate Key :\nλ:\t"+str(self.λ) +"\nμ:\t"+str(self.μ) +"\n---")


# class PublicKey:
#     """
#     Public Key object contains n and g
#     in accordance to the Paillier Cryptosystem
    
#     args:
#         n: product of two equal lenght prime numbers
    
#     attributes:
#         n: product of two primes
#         g: a random number such that,
#         multiplicative order of g in n^2 is a multiple of n
        
#         ∵ p and q are of equal length we can use a simplification of g = n+1
#     """
#     def __init__(self, n):
#         self.n = n
#         self.nsq = n * n
#         self.g = n+1
    
#     def __repr__(self):
#         return ("---\nPublic Key :\nn:\t"+ str(self.n) +"\n---")


# def generate_keys(bitlen=128):
#     """
#     generate_keys( bitlen)
    
#     args:
#         bitlen: length of primes to be generated (default: 128)
    
#     returns Public Private key pair as a tuple
#     (PublicKey, PrivateKey)
#     """
    
#     p = rabin.generate_prime(bitlen)
#     q = rabin.generate_prime(bitlen)
#     n = p * q
#     return (PublicKey(n), PrivateKey(p, q, n))


# def Encrypt(public_key, plaintext):
#     """
#     Encrypt( public_key, plaintext)
    
#     args:
#         public_key: Paillier Publickey object
#         plaintext: number to be encrypted
        
#     returns:
#         ciphertext: encryption of plaintext
#         such that ciphertext = (g ^ plaintext) * (r ^ n) (mod n ^ 2)
#         where, r is a random number in n such that r and n are coprime
#     """
    
#     r = random.randint( 1, public_key.n-1)
#     while not modarithmetic.xgcd( r, public_key.n)[0] == 1:
#         r = random.randint( 1, public_key.n)
        
#     a = pow(public_key.g, plaintext, public_key.nsq)
#     b = pow(r, public_key.n, public_key.nsq)
    
#     ciphertext = (a * b) % public_key.nsq
#     return ciphertext


# def Decrypt(public_key, private_key, ciphertext):
#     """
#     Decrypt( publick_key, private_key, ciphertext)
    
#     args:
#         public_key: Paillier PublicKey object
#         private_key: Paillier PrivateKey object
#         ciphertext: Encrypted Integer which was ecnrypted using the public_key
        
#     returns:
#         plaintext: decryption of ciphertext
#         such that plaintext = L(ciphertext ^ λ) * μ (mod n ^ 2)
#         where, L(x) = (x - 1) / n
#     """
    
#     x = pow(ciphertext, private_key.λ, public_key.nsq)
#     L = lambda x: (x - 1) // public_key.n
    
#     plaintext = (L(x) * private_key.μ) % public_key.n 
#     return plaintext


# def homomorphic_add(public_key, a, b):
#     """
#     adds encrypted integer a to encrypted integer b 
    
#     args:
#         public_key
#         encryption of integer a
#         encryption of integer b
#     returns:
#         encryption of sum of a and b
#     """
#     return (a * b) % public_key.nsq


# def homomorphic_add_constant(public_key, a, k):
#     """
#     adds a plaintext k to encrypted integer a
    
#     args:
#         public_key
#         encryption of integer a
#         plaintext k
#     returns:
#         encryption of sum of a and k
#     """
#     return a * pow( public_key.g, k, public_key.nsq) % public_key.nsq


# def homomorphic_mult_constant(public_key, a, k):
#     """
#     multiplies a plaintext k to encrypted integer a
    
#     args:
#         public_key
#         encryption of integer a
#         plaintext k
#     returns:
#         encryption of product of a and k
#     """
#     return pow(a, k, public_key.nsq)
import random
import modarithmetic
import rabin

# Define the PrivateKey and PublicKey classes
class PrivateKey:
    def __init__(self, p, q, n):
        self.λ = modarithmetic.lcm(p - 1, q - 1)
        self.μ = modarithmetic.multiplicative_inverse(self.λ, n)
        
    def __repr__(self):
        return f"---\nPrivate Key :\nλ: {self.λ}\nμ: {self.μ}\n---"

class PublicKey:
    def __init__(self, n):
        self.n = n
        self.nsq = n * n
        self.g = n + 1
    
    def __repr__(self):
        return f"---\nPublic Key :\nn: {self.n}\n---"

# Key Generation
def generate_keys(bitlen=128):
    p = rabin.generate_prime(bitlen)
    q = rabin.generate_prime(bitlen)
    n = p * q
    return (PublicKey(n), PrivateKey(p, q, n))

# Encryption Function with Modulo 256 to keep values in range
def Encrypt(public_key, plaintext):
    r = random.randint(1, public_key.n - 1)
    while not modarithmetic.xgcd(r, public_key.n)[0] == 1:
        r = random.randint(1, public_key.n)
    
    # Encrypt with Paillier encryption formula
    a = pow(public_key.g, plaintext, public_key.nsq)
    b = pow(r, public_key.n, public_key.nsq)
    
    # Apply modulo 256 to ensure the values do not exceed 256
    a = a % 256
    b = b % 256
    
    ciphertext = (a * b) % public_key.nsq
    # Ensure the ciphertext is within the 256 range
    ciphertext = ciphertext % 256
    return ciphertext

# Decryption Function
def Decrypt(public_key, private_key, ciphertext):
    x = pow(ciphertext, private_key.λ, public_key.nsq)
    L = lambda x: (x - 1) // public_key.n
    
    plaintext = (L(x) * private_key.μ) % public_key.n
    return plaintext % 256  # Ensure the result is within the range [0, 255]

# Homomorphic Addition
def homomorphic_add(public_key, a, b):
    return (a * b) % public_key.nsq

# Homomorphic Multiplication
def homomorphic_mult_constant(public_key, a, k):
    return pow(a, k, public_key.nsq)

# Set up the example with two larger pixel values
pixel1 = 350  # A larger pixel value
pixel2 = 500  # Another larger pixel value

# Generate public and private keys
public_key, private_key = generate_keys(bitlen=128)

# Encrypt the pixel values
encrypted_pixel1 = Encrypt(public_key, pixel1)
encrypted_pixel2 = Encrypt(public_key, pixel2)

# Perform homomorphic addition
encrypted_sum = homomorphic_add(public_key, encrypted_pixel1, encrypted_pixel2)
decrypted_sum = Decrypt(public_key, private_key, encrypted_sum)

# Perform homomorphic multiplication (pixel1 * 2)
encrypted_mult = homomorphic_mult_constant(public_key, encrypted_pixel1, 2)
decrypted_mult = Decrypt(public_key, private_key, encrypted_mult)

# Print results
print(f"Encrypted Pixel 1: {encrypted_pixel1}")
print(f"Encrypted Pixel 2: {encrypted_pixel2}")
print(f"Encrypted Sum: {encrypted_sum}")
print(f"Decrypted Sum (mod 256): {decrypted_sum}")
print(f"Encrypted Multiplication (Pixel 1 * 2): {encrypted_mult}")
print(f"Decrypted Multiplication Result (mod 256): {decrypted_mult}")
