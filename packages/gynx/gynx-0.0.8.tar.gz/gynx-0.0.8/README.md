gynx
====

Google Drive sync client for Linux.

*This project is still in an experimental phase. Care should be exercised when syncing important Google Drive files.*

## Installation

The simplest way to install **gynx** is through pip

```bash
pip install --user gynx
```

Use the `--user` flag to install the relevant files and scripts in your home diretory.
**N.B.** Do not install as the root user, or using `sudo`, to prevent permissions errors during use.

### From Source

To install from source

```bash
git clone https://gitlab.com/ml394/gynx.git
cd gynx
python setup.py install
```

This should be run inside a Python 3 virtual environment.

## Usage

Create a Google Drive sync folder in your home directory and run the `gynx` command to start the syncing operations.

The first time this is run, you will be asked to sign into Google via your web browser and give the **gynx** app permissions to access your account.

```bash
mkdir ~/drive;
cd ~/drive;
gynx
```

Your authentication token will be saved in the app config, so you will only need to sign in once. On subsequent executions you can simply `cd` into your synced drive directory and run the `gynx` command.

**N.B.** You must be in your root drive folder when you run the `gynx` command. It will try to sync your Google Drive folder with whatever folder you are currently in.

### Options

The `gynx` command can be run with a few options to further customize your sync operation, sign in using another account, and refresh your file cache to fix errors.

| Option            | Description                                                                                                 |
|-------------------|-------------------------------------------------------------------------------------------------------------|
| `--version` `-V`  | Print **gynx** release number to console and exit                                                           |
| `--help` `-h`     | Print **gynx** help text to console and exit                                                                |
| `--verbose` `-v`  | Run in verbose mode. Prints out remote drive information prior to program executions                        |
| `--clean` `-c`    | Removes the stored file caches before running. Use this option following any output errors.                 |
| `--refresh` `-r`  | Deletes the contents of the local directory and runs a full download from the remote drive. **Be careful!** |
| `--auth` `-a`     | Create a new auth token by signing in with another Google account. This will overwrite your current token.  |
| `--dry-run` `-d`  | Only print the operations to be performed to the console, but don't run them. Useful for debugging.         |
| `--schedule` `-s` | Run sync automatically on a schedule. Press Ctrl+C to stop.                                                 |
| `--duration` `-D` | Minutes until next automatic run (default 10).                                                              |
| `--start` `-S`    | Start automatic folder monitoring after the intial run. Press Ctrl+C to stop                                |

## Contributing

If you're interested in contributing to **gynx**, please follow these steps:

1. Take a look at the [Contributing Guidelines](CONTRIBUTING.md) and make sure you understand the merge request process
2. Check out ongoing issues in the [Issue List](https://gitlab.com/ml394/gynx/issues) and see if there's anything you can help out with. Feel free to submit your own issue if you discover a bug or want to suggest a new feature.
3. Clone the `development` branch and checkout your own branch to commit your changes.
4. Push your branch and submit a [Merge Request](https://gitlab.com/ml394/gynx/merge_requests) for review.

### To Do

This is a list of upcoming planned features as set out in the project [Milestones](https://gitlab.com/ml394/gynx/milestones). For a full list of issues and current development status, check the [Issue Board](https://gitlab.com/ml394/gynx/boards)

- [x] Working CLI interface for all recursive functions
- [x] PyPi deployment and installation
- [x] Full test suite with > 85% coverage
- [x] Continuous sync and changes monitoring through cron or system service
- [ ] API web service to distribute app credentials
- [ ] Allow users to generate own app credentials for individual quotas

## Donations

~~If you like the software and would like to donate, take a look at~~ [TBC](https://gitlab.com/ml394/gynx)

Instead, donate to an organization or open source project that helps promote a free and safe Internet, such as:
* [Electronic Frontier Foundation](https://supporters.eff.org/donate)
* [Wayback Machine](https://archive.org/donate/)
* [Wikipedia](https://donate.wikimedia.org/wiki/Ways_to_Give)
* [Django](https://www.djangoproject.com/foundation/donate/)
* [requests](https://www.kennethreitz.org/requests3)


> It seductively wiggles its hips as it walks. It can cause people to dance in unison with it.
> > ![](assets/jynx.png)
