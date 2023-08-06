kpsh-menu
=========

kpsh-menu allows access to kpsh run in daemon mode (`kpsh -d`) via menu-like
programs, like dmenu, rofi or fzf. It is optimized for programs which read their
stdin asynchronously, e.g. `rofi -async-pre-read=0` or dmenu with "non-blocking
stdin" patch: it quickly displays menu and feeds it with entries when they
become available (e.g. when database is unlocked).

For kpsh-menu to be useful one must first run kpsh in daemon (server) mode by
adding `-d` switch to its commandline options and optionally `-s <PATH>` to
change the default path to the socket through which kpsh-menu communicates with
server (kpsh-menu also allows changing socket path via `-s` option). kpsh-menu
by itself doesn't offer any way to open KeePass database, so one must be opened
via other server's options and/or kpsh-client. For example:

    $ kpsh -d --keyfile /path/to/keyfile --pw-cmd password-command /path/to/db.kdbx
    $ kpsh-menu

See `kpsh --help` for further informations regarding running kpsh.

You can change used menu program (which is rofi by default) with `-m` switch:

    $ kpsh-menu -m dmenu
    $ kpsh-menu -m fzf

It can be any shell command:

    $ kpsh-menu -m "dmenu -p '>'"

kpsh-menu will forward any server's password requests through pinentry
programs. By default it'll use /usr/bin/pinentry, but it can be changed with
`--pinentry` option. Please note that kpsh server also has `--pinentry` option
which has a preference over kpsh-menu one.

kpsh-menu first displays a list of all entries in currently opened database.
When one is selected, it then requests from kpsh server to perform any command
on it. By default it tries to autotype it with a default sequence, but
additional commands can be specified with `-c` options.

When used more than once these options will be displayed in a menu after entry
selection. They have the following format:

    DisplayName::Command::Flags

- DisplayName is any human-friendly string displayed in menu. It is mandatory
  part.
- Command is any kpsh command. It might contain a placeholder `{}` which will
  be replaced with selected entry path. It is mandatory part.
- Flags is a set of flags used to modify behavior of kpsh-menu after selected
  command is executed (see flags section). It is optional

Example:

    $ kpsh-menu -c "Autotype::autotype '{}'" 
                -c "Username::autotype '{}' -s {USERNAME}::ln"
                -c "Password::autotype '{}' -s {PASSWORD}::ln"
                -c "Type TAB::autotype '{} -s {TAB}::l'"
                -c "Type ENTER::autotype '{} -s {ENTER}::l'"
                -c "Show::show '{}'"
                -c "Lock database::lock"
                -n "notify-send kpsh-menu 'Executed command {cmd}'"

## Flags

The following flags can be used for commands:

- `l`: when set, kpsh-menu will loop, i.e. will be re-display command selection
  screen. This allows performing several separate actions on a selected entry,
  e.g. first typing a username, then password, which might be useful e.g. on
  some websites which show separate screens for login and password.
- `n`: after command is executed a notification program specified with `-n`
  option will be run.
