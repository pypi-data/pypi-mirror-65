# tinder-cli

CLI implementation of Tinder API

## Quick Start

Install the package:

    pip install -U tinder-cli

## Getting Tinder API token

In order to access tinder an API token is required. You can get your Tinder API token in multiple ways.

Once logged in to [Tinder.com](https://tinder.com), inspect any fetch / xhr request and locate your "X-Auth-Token".

Or you can use the following library:

[https://github.com/meister245/tinder-token](https://github.com/meister245/tinder-token#cli-script)

## CLI Usage

The CLI will prompt you for your Tinder API token on first usage, which will be stored in `~/.tinder-cli`

Usage information

    tinder-cli --help

Available CLI commands

    tinder-cli profile
    tinder-cli teasers

    tinder-cli info --id <tinder ID>
    tinder-cli like --id <tinder ID>
    tinder-cli superlike --id <tinder ID>
    tinder-cli pass --id <tinder ID>
