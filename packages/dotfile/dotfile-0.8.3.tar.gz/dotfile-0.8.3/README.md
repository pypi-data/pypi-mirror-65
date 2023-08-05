
```
┌───────────────────────────────────────────────────────┐                       
│ `dot` is an elegant git wrapper for managing dotfiles │
└───────────────────────────────────────────────────────┘
https://github.com/kylepollina/dot
```

`dot` is an easy to use dotfile manager. It wraps git, so all valid git 
commands/arguments work with `dot`. Just call `dot` with the git command 
you would like to use. If you know how to use git, then you already know 
how to use `dot`.

The basics of `dot` is that it runs this git command: 

    git --git-dir=$HOME/.dotfiles --work-tree=$HOME 

You can easily specify where your git-dir is and what your work-tree is with `dot`.

#### Why use `dot` instead of aliasing this command?
`dot` comes with a few handy custom git commands that are specific with managing dotfiles.

* `dot cwf` (short for commit-with-filenames) will create a nice commit message showing which files you added/deleted/modified. You can also add your own description with the `-m` flag.
* `dot s` status of tracked files only
* `dot au` add/update currently tracked files
* `dot list` list all currently tracked files


## Requirements
* [git](https://git-scm.com/)


## Installation

```
pip install dotfile
```

or


```
git clone https://github.com/kylepollina/dot
cd dot
python3 setup.py install
```

## Usage

#### Using normal git commands
```
[~]$ dot rm --cached .bash_profile
rm '.bash_profile'
[~]$ dot add .zprofile
[~]$ dot add .alias
```

#### `dot cwf` (commit-with-filenames)
```
[~]$ dot cwf -m "Switched bash_profile to zprofile and alias changes"
[master 8724093] Switched bash_profile to zprofile and alias changes Added: ['.zprofile'] Deleted: ['.bash_profile'] Modified: ['.alias']
 3 files changed, 81 insertions(+), 22 deletions(-)
 delete mode 100644 .bash_profile
 create mode 100644 .zprofile
[~]$
[~]$ dot log | head
commit 87240937d9ceb04984a2e851348927c9eef3386b
Author: kyle<>
Date:   Mon Mar 30 21:25:32 2020 -0500

    Switched bash_profile to zprofile and alias changes
    Added: ['.zprofile']
    Deleted: ['.bash_profile']
    Modified: ['.alias']
```

#### `dot s` (git status -uno) Status of tracked files only
```
[~/.config/nvim/UltiSnips]$ dot s
On branch master
Your branch is up to date with 'origin/master'.

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	deleted:    javascript.snippets
	new file:   ruby.snippets

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   python.snippets
	modified:   ../../um/umconfig

Untracked files not listed (use -u option to show untracked files)
```

#### `dot au` (git add -u) Add all tracked files to index

```
[~/.config/nvim/UltiSnips]$ dot au
[~/.config/nvim/UltiSnips]$ dot s
On branch master
Your branch is up to date with 'origin/master'.

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	deleted:    javascript.snippets
	modified:   python.snippets
	new file:   ruby.snippets
	modified:   ../../um/umconfig

Untracked files not listed (use -u option to show untracked files)
```

#### `dot list` (git ls-tree --full-tree -r --name-only HEAD) List all tracked files

```
[~]$ dot list
.alias
.bash_profile
.config/bpython/config
.config/iterm/profiles.json
.config/nvim/UltiSnips/all.snippets
.config/nvim/UltiSnips/html.snippets
.config/nvim/UltiSnips/javascript.snippets
.config/nvim/UltiSnips/python.snippets
.config/nvim/colors/PaperColor.vim
.config/nvim/colors/nightfly.vim
.config/nvim/init.vim
.gitconfig
.zprofile
.zshrc
```


## Setup
To setup your dotfile repository, run `dot init` and it will walk you through the setup.
You can setup a new repository, or use an existing repository.

#### New repository setup

```
[~]$ dot init
===== dotfile setup =====
Choose how you want to initialize your dotfiles:
[0] Create new dotfile repository
[1] Use existing dotfile repository
 > 0
New repository setup
--------------------
Repository name: [.dotfiles]
Default work tree: [/Users/kyle]

Generated configs: /Users/kyle/.config/dot/config.toml

[dot]
git-dir=/Users/kyle/.dotfiles/.git
work-tree=/Users/kyle

Do you wish to continue? (y/n [y]) y

Created config file at /Users/kyle/.config/dot/config.toml
Initialized empty Git repository in /Users/kyle/.dotfiles/.git/
Dotfile repository created at /Users/kyle/.dotfiles
```

#### Existing repository setup
```
[~]$ git clone https://github.com/kylepollina/.dotfiles
Cloning into '.dotfiles'...
remote: Enumerating objects: 65, done.
remote: Counting objects: 100% (65/65), done.
remote: Compressing objects: 100% (45/45), done.
remote: Total 2101 (delta 39), reused 43 (delta 20), pack-reused 2036
Receiving objects: 100% (2101/2101), 1.18 MiB | 1.89 MiB/s, done.
Resolving deltas: 100% (577/577), done.
[~]$
[~]$ dot init
===== dotfile setup =====
Choose how you want to initialize your dotfiles:
[0] Create new dotfile repository
[1] Use existing dotfile repository
 > 1
Existing repository setup
-------------------------
Repository name: .dotfiles
Work tree directory: [/Users/kyle]

Generated configs: /Users/kyle/.config/dot/config.toml

[dot]
git-dir=/Users/kyle/.dotfiles/.git
work-tree=/Users/kyle

Do you wish to continue? (y/n [y]) y

Created config file at /Users/kyle/.config/dot/config.toml
Dotfiles setup at /Users/kyle/.dotfiles

Analyzing dotfile repository...
There is 2 files and 0 directories in /Users/kyle/.dotfiles

Files
-----
.zprofile
.bash_profile

Would you like to move these into your work tree? (y/n [y]) y

Moving file /Users/kyle/.dotfiles/.zprofile to /Users/kyle
overwrite /Users/kyle/.zprofile? (y/n [n]) y
/Users/kyle/.dotfiles/.zprofile -> /Users/kyle/.zprofile

Moving file /Users/kyle/.dotfiles/.bash_profile to /Users/kyle
overwrite /Users/kyle/.bash_profile? (y/n [n]) n
not overwritten
```

## License
MIT
