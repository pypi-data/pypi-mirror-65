# kpsh
kpsh, or KeePass Shell, is an interactive shell for working directly with
KeePass database files.

## Features

- open, lock and unlock databases
- list contents of database
- show contents of database entries and filter them by fields
- autotype usernames and passwords or any sequences of entry fields.
- access all commands non-interactively via `-c` switch or by piping commands
  directly to kpsh
- tab-completion in interactive mode
- daemon mode: open and unlock your database once and then quickly access
  its contents from kpsh-client.
- several built-in ways to obtain a password, which can be passed by argument,
  typed directly to kpsh or through pinentry program program or fetched from a
  provided command output
- ships with highly customizable kpsh-menu script which performs any kpsh
  command on entries selected by dmenu/rofi/fzf (e.g. autotype passwords
  selected in dmenu/rofi)

# Usage examples

Typical session:

```
$ kpsh passwords.kdbx

passwords.kdbx> ls
Password: ********
personal/bank
personal/login
personal/website
work/login

passwords.kdbx> show work/login
path: work/login
username: John Doe
password: jsdf7y8h8349yhj3h42
```

Get a password from gpg-encrypted file (trailing newline, which isn't a part
of password is trimmed):

```
$ gpg --encrypt -o masterpass.gpg -r mymail@example.com
<type type type>
^D
$ kpsh passwords.kdbx --pw-cmd "gpg --decrypt masterpass.gpg | tr -d '\n'"
```

... or from a keyring:

```
$ secret-tool store --label='keepass' database passwords.kdbx
$ kpsh passwords.kdbx --pw-cmd "secret-tool lookup database passwords.kdbx"
```

Autotype a user/password sequence:

```
$ kpsh passwords.kdbx --pw-cmd "secret-tool lookup database passwords.kdbx"
                      -c autotype entry1
```

... or just a password, but a little faster:

```
$ kpsh passwords.kdbx --pw-cmd "secret-tool lookup database passwords.kdbx"
                      -c "autotype -s {PASSWORD} -D 12 entry1"
```

Run as daemon (`-d`):

```
$ kpsh passwords.kdbx -d --pw-cmd "secret-tool lookup database passwords.kdbx" &
$ kpsh-client ls
entry1
entry2
$ kpsh-client autotype entry1
```

Use pinentry to get a password when database will be unlocked:

```
$ kpsh passwords.kdbx --pinentry /usr/bin/pinentry
```

## Installation

```
$ pip install --user kpsh
```
