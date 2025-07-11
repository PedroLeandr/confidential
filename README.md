🔐 Encryption Workflow
Don't push anything unless it's encrypted. Seriously.

This repo uses a simple encryption system to keep files secure.
Follow the instructions below — no shortcuts.



🔓 Decrypt files
bash:

-- py encrypter/encrypter.py decrypt {path_name} {code}

Replace {code} with the encryption code you got when the files were encrypted.

Example: py encrypter/encrypter.py encrypt example/ 00000000

This will decrypt everything that was previously encrypted.



🔒 Encrypt files
bash:

--  py encrypter/encrypter.py encrypt {path_name}

Replace {path_name} with the root path you want to encrypt (as seen in the repo).

Example: py encrypter/encrypter.py encrypt example/

Only encrypt the root of what you want — no need to go deeper.

Encrypt before every push.

THE CODE CHANGE FOR ANY ENCRYPT... SAVE IT!



⚠️ Important
Save the encryption code. You won't be able to decrypt anything without it.

No backups. No second chances.

Encrypt. Push. Done.



-- soo... --

1. dont push if u dont encrypt;
2. use 'py encrypter/encrypter.py decrypt {path name} {code}' to decrypt files;
3. SAVE THE ENCRYPTION CODE;
4. use 'py encrypter/encrypter.py encrypt {path name}' to encrypt files, (encrypt the "root path", i mean the path on repositorie);
5. SAVE THE ENCRYPTION CODE;
