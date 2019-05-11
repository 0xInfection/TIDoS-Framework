<!-- # Welcome to MkDocs

For full documentation visit [mkdocs.org](https://mkdocs.org).

## Commands

* `mkdocs new [dir-name]` - Create a new project.
* `mkdocs serve` - Start the live-reloading docs server.
* `mkdocs build` - Build the documentation site.
* `mkdocs help` - Print this help message.

## Project layout

    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files. -->

# Overview

## Project Layout

    TIDOS-FRAMEWORK/                    # Project root (Threat/)
        core/                           # Apps core functionality
            build_menu.py               # Builds out the app menus
            colors.py                   # Reference for app colors
            functions.py                # Reference for app functions
            process.py                  # Reference for app multiprocessing
            useragents.py               # List of User Agents
        modules/                        # All modules
            enumeration/                # Enumeration modules
            exploitation/               # Exploitation modules
            recon/                      # Recon modules
            vulnysis/                   # Vulnerability Analysis/Assessment modules
        tidos.py                        # Main run file (threat.py)