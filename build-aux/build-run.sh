#!/bin/bash

rm -rf repo .flatpak-builder builddir /tmp/length.flatpak
flatpak uninstall -y io.github.herve4m.Length.Devel
flatpak remote-add --user --if-not-exists gnome-nightly https://nightly.gnome.org/gnome-nightly.flatpakrepo
flatpak-builder --force-clean --user --install-deps-from=gnome-nightly --repo=repo --install builddir io.github.herve4m.Length.Devel.yaml
flatpak build-bundle repo /tmp/length.flatpak io.github.herve4m.Length.Devel
rm -rf repo .flatpak-builder builddir
flatpak run io.github.herve4m.Length.Devel
