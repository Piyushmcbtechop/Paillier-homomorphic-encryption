
from PIL import Image
import numpy as np
import pickle

import pallier

def ImgEncrypt(public_key, plainimg):
    """
    args:
        public_key: Paillier PublicKey object
        plainimg: PIL Image object
        
    returns:
        cipherimg: Encryption of plainimg
    Encrypts an image
    """
    cipherimg = np.asarray(plainimg)
    shape = cipherimg.shape
    cipherimg = cipherimg.flatten().tolist()
    cipherimg = [pallier.Encrypt(public_key, pix) for pix in cipherimg]
    
    return np.asarray(cipherimg).reshape(shape)

def ImgDecrypt(public_key, private_key, cipherimg):
    """
    args:
        public_key: Paillier PublicKey object
        private_key: Paillier PrivateKey object
        cipherimg: encryption of Image
        
    returns:
        Image object which is the decryption of cipherimage
    Decrypts encrypted image
    """
    shape = cipherimg.shape
    plainimg = cipherimg.flatten().tolist()
    plainimg = [pallier.Decrypt(public_key, private_key, pix) for pix in plainimg]
    plainimg = [pix if pix < 255 else 255 for pix in plainimg]
    plainimg = [pix if pix > 0 else 0 for pix in plainimg]
    
    return Image.fromarray(np.asarray(plainimg).reshape(shape).astype(np.uint8))

def homomorphicBrightness(public_key, cipherimg, factor):
    """
    args:
        public_key: Paillier PublicKey object
        cipherimg: n dimensional array containing encryption of image pixels
        factor: Amount of brightness to be added (-ve for decreasing brightness)
    
    returns:
        n dimensional array containing encryption of image pixels with brightness adjusted
    
    Function to demonstrate homomorphism
    Performs brightness adjust operation on the encrypted image
    """
    shape = cipherimg.shape
    brightimg = cipherimg.flatten().tolist()
    brightimg = [pallier.homomorphic_add_constant(public_key, pix, factor) for pix in brightimg]
    
    return np.asarray(brightimg).reshape(shape)

def saveEncryptedImg(cipherimg, filename):
    """
    args:
        cipherimg: Encryption of an image
        filename: filename to save encryption (saved under encrypted-images directory)
        
    saves Encryption of image into a file
    """
    filename = "encrypted-images/" + filename
    fstream = open(filename, "wb")
    pickle.dump(cipherimg, fstream)
    fstream.close()

def loadEncryptedImg(filename):
    """
    args:
        filename: filename of the Encrypted object under encrypted-images directory
        
    returns:
        n-dimensional array containing encryption of image
    loads Encrypted image object from file
    """
    filename = "encrypted-images/" + filename    
    fstream = open(filename, "rb")
    cipherimg = pickle.load(fstream)
    fstream.close()
    return cipherimg

def isEncrypted(cipherimg):
    """
    args:
        cipherimg: n-dimensional array (possibly encrypted image)
    
    returns:
        Boolean indicating whether the image is encrypted
    """
    try:
        # Check if the first pixel is an encrypted object
        if isinstance(cipherimg.flatten()[0], pallier.EncryptedNumber):
            return True
        else:
            return False
    except AttributeError:
        # If the structure doesn't support flattening or indexing, it's not encrypted
        return False


if __name__ == "__main__":
    image_path = r"C:\Users\Nishant\OneDrive\Attachments\Desktop\paliier homorphic encryption\images\horizonzerograyscale.bmp"
    
    # Load and convert image to grayscale
    plain_img = Image.open(image_path).convert("L")
    print("Original image loaded.")
    
    # Generate keys
    public_key, private_key = pallier.generate_keys(bitlen=128)
    print("Keys generated successfully.")
    
    # Encrypt the image
    cipher_img = ImgEncrypt(public_key, plain_img)
    print("Image encrypted. First few encrypted values:", cipher_img.flatten()[:10])
    
    # Save the encrypted image (as a debug visualization, not actual encryption)
    debug_encrypted_img = np.vectorize(lambda x: x % 256)(cipher_img)
    Image.fromarray(debug_encrypted_img.astype(np.uint8)).save("encrypted_image_debug.bmp")
    
    # Decrypt the image
    decrypted_img = ImgDecrypt(public_key, private_key, cipher_img)
    print("Image decrypted.")
    
    # Save and display the decrypted image
    decrypted_img.save("decrypted_image.bmp")
    decrypted_img.show()

