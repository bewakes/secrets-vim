# secrets-vim

Writing/Saving secrets with ease and secrecy.

## Motivation
It all began with my sudden urge to **write a love letter**, induced when I was
reading Gabriel Garcia Marquez's *Love in the time of Cholera*. Obviously, I
want it to be very very secret. So, I can neither risk someone peeking from
behind my back(not even God) or forgetting to encrypt it when I am done with
writing.  

I want something very handy to encrypt/decrypt but also easily writeable and modifiable. I
came up with this idea - ***why not just create a vim plugin that just encrypts
the text while I am typing(that's going to be too much though) or when I save
the file?*** That sounded okay, and here it is.

## Installation
It's very easy. Install [Plug](https://github.com/junegunn/vim-plug). And in
your `vimrc` file, within `Plug` block, add `"bewakes/secrets-vim"`. Reload
vim and then run `:PlugInstall`.


## Encryption
The encryption is done using [Caesar
Cipher](https://en.wikipedia.org/wiki/Caesar_cipher). However, it is not that
weak because it uses not a single key but a phrase/string as key which makes it
hard to decipher.

## Usage
Whenever you open a file with `.sec` extension, it will automatically ask you
to enter your secret key that will encrypt/decrypt the text you'll be writing. 

When you are done with the text run `:EncryptText` and TADA!!

To Decrypt the text run `:DecryptText` and TADA!!

If you want to change the secret then run `:SetSecret`. **But** this will only
let you change if there is no encrypted text.


## TODOs
* [ ] Versioning of encryption/decryption. Because if encryption method changes,
    previous encrypted data should be decryptable.
* [ ] Make some auto commands efficient.
* [ ] Auto save on write. Make this configurable.
* [ ] Unicode Support.



## CONTRIBUTIONS
Are very welcome. But please create an issue before sending a pull request.
