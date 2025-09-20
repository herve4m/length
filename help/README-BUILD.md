# Write Content

- Write your help pages in the `C` directory.
- List your new pages and images in the `meson.build` file.

# Prepare for Translation

- Add your language to the `LINGUAS` file.

- Update the `help.pot` file from the pages in the `C` directory:

```
$ cd help
$ itstool -o help.pot ../help/C/*.page
```

- Merge the new `help.pot` file with an existing translation file:

```
$ msgmerge fr/fr.po help.pot  > fr/fr-new.po
$ mv fr/fr-new.po fr/fr.po
```
