# Blindage 🔐

[![Test](https://github.com/henriquesebastiao/blindage/actions/workflows/test.yml/badge.svg)](https://github.com/henriquesebastiao/blindage/actions/workflows/test.yml)
[![coverage](https://coverage-badge.samuelcolvin.workers.dev/henriquesebastiao/blindage.svg)](https://coverage-badge.samuelcolvin.workers.dev/redirect/henriquesebastiao/blindage)

*You are in control of your data.*

Blindage is a Python password manager in CLI that stores your passwords encrypted in a SQLite database on your machine.

## Features

- Beautiful CLI interface made with [Typer](https://github.com/fastapi/typer) and [Rich](https://github.com/Textualize/rich).
- Saves the master password encrypted with the Argon 2 key derivation algorithm.
- Stores other encrypted data based on a key generated from the master password, making it impossible to read the data without the encryption key, that is, without the master password.
- Password suggestions containing upper and lower case letters, numbers and special characters.
