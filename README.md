# cripty
## The personal vault on your computer

![alt text](resources/icon_128x128.png)

A personal safe where you can insert files and keep them encrypted and secure. Everything stored locally on your machine

### Vaults
A Vault is a folder in your computer where your secret files are stored.
These files are encrypted, so you can't open them.<br/>
By default, vaults are stored in /home/$USER/.cripty/ (For Linux). You can't change a vault path (function still not implemented)

### Usage

Use

    python3 main.py

to run cripty. If no vault is found, the program will open the "Vault setup wizard", which guides you creating a vault. <br/> 
Else, it will ask you to log in into your vault, with vault name and password.
