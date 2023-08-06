import os
from cryptography.fernet import Fernet


homedir_path = os.getenv('HOME')
folder_path = homedir_path + '/.ezissue/'
hub_path = folder_path + 'hub'
lab_path = folder_path + 'lab'


def create_secure_key():
    """
    Creates a file with the user's secure key for encription purposes.
    """
    check_folder_structure(folder_path)
    path = folder_path + 'key.key'

    if os.path.isfile(path):        # this can be bugged
        return False
    else:
        key = Fernet.generate_key()
        file = open(path, 'wb+')
        file.write(key)
        file.close()
        return True


def get_key():
    """
    Gets the user's encription key from filesystem.
    """
    file = open(folder_path + 'key.key', 'rb')
    k = file.readline()
    return k


def check_folder_structure(full_path):
    """
    Creates the HOMEDIR folders if they do not exists. If they exists, it does
    nothing.
    """
    if not os.path.exists(full_path):
        os.makedirs(full_path)


def encrypt(line):
    """
    Recieves a line and encrypts it.
    """
    k = get_key()
    f = Fernet(k)
    return f.encrypt(line)


def decrypt_token(encrypted_line):
    """
    Recieves a encrypted line and decrypts it.
    """
    k = get_key()
    f = Fernet(k)
    return f.decrypt(encrypted_line)


def write_tokens(github_key, gitlab_key):
    """
    Writes user's github and gitlab access keys as encrypted content on a file.
    Returns if the operation was 'bueno' or 'no bueno'.
    """
    fp = hub_path
    fp2 = lab_path

    check_folder_structure(folder_path)

    enc_gh = encrypt(github_key.encode())
    enc_gl = encrypt(gitlab_key.encode())

    try:
        file = open(fp, "wb+")
        file2 = open(fp2, "wb+")
        file.write(enc_gh)
        file2.write(enc_gl)
    finally:
        file.close()
        file2.close()

    return (os.path.isfile(fp) and os.path.isfile(fp2))


def get_token(repo_manager):
    """
    Gets the user's access token from the filesystem given the repo manager
    he's trying to access.
    """
    enc = ''
    token = ''
    file = ''

    if repo_manager == 'github':
        file = open(hub_path, 'rb')
    elif repo_manager == 'gitlab':
        file = open(lab_path, 'rb')
    # else:
        # it would be nice to raise an exception here btw

    enc = file.read()
    token = decrypt_token(enc)
    return token.decode()
