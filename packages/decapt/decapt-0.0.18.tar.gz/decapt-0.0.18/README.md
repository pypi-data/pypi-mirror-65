# Simple declarative package management
## For Debianish Linux

Declarative package management means you make a file containing everything you want installed, and the package manager adds/removes to make the system match that.  It's good if you happen to install lots of random programs and forget to remove them until you forgot whether they were important to have installed or not in the first place!

Requires: aptitude, sudo, python 3.6+

1. `pip install decapt`
2. `decapt generate`
3. Modify `decapt.luxem`
4. Update your system with `decapt`

## Features

* Manage snap packages
* Manage manual debian packages
  Add an entry like `{ name: mypackage, path: ~/debs/mypackage }` where there's a `build.sh` script in `path` which creates a `mypackage.deb` in `path`.
* [Luxem](https://gitlab.com/rendaw/luxem)

## Notes

### Autoremove

Debian considers _installed_ "suggested" and "recommended" for other installed packages to be important, so they won't be autoremoved after being installed once.  If for instance something recommends chrome or firefox, and you remove chrome from your list and add firefox, it won't be removed (by default).  To make these not recommended, create `/etc/apt/apt.conf.d/99_norecommends` and add:
```
APT::Install-Recommends "false";
APT::AutoRemove::RecommendsImportant "false";
APT::AutoRemove::SuggestsImportant "false";
```
[(source)](https://askubuntu.com/questions/351085/how-to-remove-recommended-and-suggested-dependencies-of-uninstalled-packages)

If you run `apt autoremove` you can confirm what this affects that's currently installed.  You should probably add some to your decapt list (ex: `grub-efi-amd64`).  You can check why something on that list is currently installed by running `aptitude why PACKAGE` -- if it's actually a dependency (not just suggested/recommended) by something else, try `aptitude why` on that something else until you find what package at the head of the chain is set free by this change.
 
### Base packages

Decapt generate consults the list of currently manually installed non-base software.  Debian seems to "manually" install a lot of unnecessary packages, so the initially generated list will include both packages and dependencies, where you might only want the package itself?  To convert all manually installed dependencies to auto packages, run:

```
$ sudo apt-mark showmanual | while read line; do if [[ $(apt-cache rdepends --installed $line | wc -l) -ne 2 ]]; then apt-mark auto $line; fi; done
```

If you do `decapt generate` after that you should have a smaller list of base-system spam in the list.

(TODO: rdepends seems to include suggested/recommended dependencies too, so this might need to be reworked to use a different tool).

## Friends (not really)

* [Nix](https://nixos.org/nix/) - A strict declarative package (and config) manager, and also the basis of Linux distro [NixOS](https://nixos.org/)
* [Guix](https://guix.gnu.org/) - A strict declarative package (and config) manager, and also the basis of Linux distro GuixSD
* [aconfmgr](https://github.com/CyberShadow/aconfmgr) - A declarative Arch-native package and config manager
* [decpac](https://gitlab.com/rendaw/decpac) - I made something similar for Arch
