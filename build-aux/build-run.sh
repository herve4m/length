#!/bin/bash

rm -rf repo .flatpak-builder builddir
flatpak uninstall -y io.github.herve4m.Length.Devel
flatpak remote-add --user --if-not-exists gnome-nightly https://nightly.gnome.org/gnome-nightly.flatpakrepo
flatpak-builder --force-clean --user --install-deps-from=gnome-nightly --repo=repo --install builddir io.github.herve4m.Length.Devel.yaml
flatpak run io.github.herve4m.Length.Devel
