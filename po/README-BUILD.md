# Updating PO Files After Changes to the Code

This process is not for translators, but for code developers to prepare the
new contents for translation.

- Run `meson setup builddir` at the root of the repository.
- Change to the `builddir` directory.
- Update the `po/length.pot` file by running `meson compile length-pot`.
- Update all the language `po/*.po` files by running `meson compile length-update-po`.

Translators can then update their PO file.
