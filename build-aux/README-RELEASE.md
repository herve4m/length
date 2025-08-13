# Update Version

- Create a branch and change to it.
- Update `version` in `meson.build`.
- Add a `<release>` entry in `data/io.github.herve4m.Length.metainfo.xml.in.in`.
- Add the same entry in `CHANGELOG.rst`.
- Commit, create a PR (_Prepare for release (version 0.8.1)_ for example), and merge.
- Change to the `main` branch, pull the new contents, and delete the version branch:

  ```
  $ git checkout main
  $ git pull
  $ git branch -d <version_branch>
  ```

- Create and push the version tag:

  ```
  $ git tag 0.8.1
  $ git push origin 0.8.1
  ```

- Wait for the GitHub Actions to complete successfully.


# Publish

- Clone https://github.com/flathub/io.github.herve4m.Length
- Create a branch, such as `herve4m/v0.8.1`.
  Change to the branch.
- Edit the `io.github.herve4m.Length.yaml` file.
  Change the `tag` and the `commit` entries.
  For the commit, go to https://github.com/herve4m/length/tags, click the commit for the tag, and use the copy icon to get the full SHA.
- Commit and create a PR named `v<version>`, such as `v0.8.1`.
- Wait for the automatic build to complete.
- Merge the PR and delete the branch.
