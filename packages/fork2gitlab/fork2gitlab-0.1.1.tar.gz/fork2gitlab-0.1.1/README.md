A script to help forking a project to gitlab and keeping it updated downstream

# Installation

`pip install fork2gitlab`

# Configuration

In order to interact with the gitlab instance, a configuration file will be needed.
Create on in on the [locations supported by python-gitlab][python-gitlab locations]

# Usage

**Forking**

Use `f2g fork <git url>` to import a git project.

The project will also be automatically mirrored hourly by gitlab.

You can then create your branch and make changes. 

**Syncing**

Use `f2g sync <gitlab project name> <branch>` to merge upstream changes into your branch.

Since gitlab takes care of the hourly sync, this command simply attempts to merge the upstream changes.
When a merge conflict occurs, a merge request will be created.

It's up to you to notify in case the merge request has been created. 

[python-gitlab locations]: https://python-gitlab.readthedocs.io/en/stable/cli.html#configuration
