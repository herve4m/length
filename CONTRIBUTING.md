# How to Contribute

We welcome contributions from the community.
There are a few ways you can help us improve.

## Opening an Issue

If you see something you would like changed, but you are not sure how to change
it, then submit an issue describing what you'd like to see.

## Working Locally

Before committing your contribution, install and then run the `pre-commit` tool to verify your work.
The `pre-commit` configuration for the GitHub repository instructs the tool to run the `black` and `flake8` commands.

You can use the following steps to prepare `pre-commit` on your system:

1. Install the `pre-commit`.
2. Navigate to your local copy of the GitHub repository.
3. Install the `pre-commit` hooks for the project: `pre-commit install`

Git automatically runs `pre-commit` every time you commit your work.
You can also run `pre-commit` at any time by using the `pre-commit run --all` command from inside your local copy of the GitHub repository.

See the [pre-commit](https://pre-commit.com/) documentation for more details.

## Submitting a Pull Request

Prepare and submit pull requests as follows:

1. Fork the repository on GitHub and then clone it on your system.
2. Create a branch named appropriately for the change you are going to make.
3. Make your code change.
4. Push your code change to your forked repository.
5. Use the GitHub web UI to navigate to the original repository https://github.com/herve4m/length/pulls (not your forked repository).
   Open a pull request.
6. All pull requests go to a validation process.
   Make sure to run `pre-commit` before submitting your code.

For more details of forks and pull request, see the [Creating a pull request from a fork](https://docs.github.com/en/github/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork) and [How to create a pull request in GitHub](https://opensource.com/article/19/7/create-pull-request-github) documentations.

## Contributing Translations

You can contribute to Lenght translations with [Weblate](https://hosted.weblate.org/projects/length/).
