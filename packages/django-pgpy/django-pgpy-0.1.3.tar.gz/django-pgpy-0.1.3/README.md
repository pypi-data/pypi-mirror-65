django-pgpy
===========

django-pgpy is a Django app for the implementation of PGP encryption/decryption in Django web applications. It provides a secure fallback mechanism to restore the user's private keys.


Requirements
============

* Python 3.7+
* Django 2+
* pgpy

Installation
=============
    pip install django-pgpy

Configuration
=============

TBD
<!-- There are simple templates files in `templates/`.  You will need to add Django's
egg loader to use the templates as is, that would look something like this:

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': '/path/to/my/templates',
            'OPTIONS': {
                 'loaders': (
                      'django.template.loaders.filesystem.Loader',
                      'django.template.loaders.app_directories.Loader',
                  ),
             }
        },
    ]

Add the project `softdelete` to your `INSTALLED_APPS` for
through-the-web undelete support.

    INSTALLED_APPS = (
    ...
        'django.contrib.contenttypes',
        'softdelete',
    ) -->

How It Works
============

In the "Identity" model, a PGP-compatible asymmetric key pair (public and private keys) is stored in the database. The private key can (and should) be encrypted with a password. If the password is lost, the private key can no longer be used. Therefore, a secure and defined fallback mechanism has been implemented to reopen the private key. 
The private key is encrypted by a hash created from the user's password. To recover the private key in case of a forgotten password, the application can define "Identity" objects that can also open the private key. 


django-pgpy make use of the standard password hashers form django. It's very important to use a secure hasher that uses salts. The private key will also encrypted by all users that are marked as fallback encrypter and a the system encrapters.

* It's not possible for a system administor or a hacker how have control over the database to use private keys and decrypt PGP messages. The password of a user/restorer is always neccessary.
* It's safe to craete database backups. The encrypted data is safe

Models
------
~~~~
class Identity:
    public_key_blob = TextField()
    private_key_blob = TextField()
    secret_blob = TextField() 

    encrypters = ManyToManyField(Identity)


class RequestKeyRecovery:
    uid = ForeignKey(Identity)
    
    recovered_by = ForeignKey(Identity, null=True)

    secret_blob = BlobField() 
~~~~



Create keys
-----------
~~~~
public_key, private_key = create_key_pair()

secert = hash(password)
private_key_protected = private_key.portect(secert)
secret_encrypted = encrypt(secret, list_of_restore_public_keys)

uid = Identity(public_key, private_key_protected, secret_encrypted)
persist(uid)
~~~~

The private key is always encrypted with the user's password. The password is only available immediately after login. The simple solution is to implement an own LoginBackend, which creates the openPGP key and encrypts it with the password. 

* No keys can be created when logging in using an API key.
* f a user does not have a key, it is not possible to create anonymous reports that can be decrypted by that user.

Encrypt message
---------------

~~~~
function encrypt(text, uids: List[Identity])
    
    message = PGPMessage(text, uids)
    for uid in uid:
        message = uid.public_key.encrypt(message)
    
    persist(message)
~~~~

Decrypt message
---------------

~~~~
function decrypt(uid: Identity, password: str, encrypted_message: PGPMessage)
    
    secert = hash(password)
    uid.private_key.unlock(secert)

    text = encrypted_message.decrypt(uid.private_key)
    
    return text
~~~~

Change password
---------------

~~~~
function change_password(uid: Identity, old_password: str, new_password: str)
    
    old_secert = hash(old_password)
    uid.private_key.unlock(old_secert)

    new_secert = hash(new_password)
    uid.private_key.protect(new_secert)

    uid.secret_encrypted = encrypt(secret, list_public_keys_to_restore)
    
    persist(uid)
~~~~

* The users enters the old and the new password
* The standard django "change password view" is used to change the password
* django-pgpy hooks in after the password is changed successfully
  * The private key is decrypted by using the old password
  * The private key is encratped by using the new password
  * The encrypted private key is stored in the database

Restore password
----------------

Initiate "reset password" by a user
~~~~
function reset_password(uid: Identity, new_password: str)
    
    new_secert = hash(new_password)
    new_secert_encrypted = encrypt(new_secert, list_of_recovering_uids)

    request = RequestKeyRecovery.create(uid, new_secert_encrypted)
    send_mail("Please recover private key", list_of_recovering_uids) 
~~~~

~~~~
function recover_key(request_key_recovery, recovering_uid, password_of_recovering_uid):
    old_secret = recovering_uid.encrypt(request_key_recovery.uid.secret_blob, password_of_recovering_uid)
    request_key_recovery.uid.private_key.unlock(old_secret)      

    secret = decrypt(request_key_recovery.secert_encrypted, uid)

    request_key_recovery.uid.private_key.protect(secret)
~~~~
