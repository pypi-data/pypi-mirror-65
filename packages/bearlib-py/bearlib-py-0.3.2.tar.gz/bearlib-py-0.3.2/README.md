# BearLib

## What is BearLib?

BearLib is a library of utilities and standardizations used for writing Python code for UNCO applications and scripts.

## Modules

### `logging`

A module for logging both locally (file and console), as well as remote webhooks (Teams, Discord, Slack, etc)

#### `logging.core`

The core logging functionality. Contains the default file + console code, as well as the ability to load webhooks.

#### `logging.webhooks`

All officially supported webhooks, as well as the `Webhooks` superclass

##### Officially supported webhooks

* Discord
* Teams
* Slack

### `notifiers`

Handlers for sending (non-logging) notifications out to various services

#### `notifiers.email`

SMTP Email support for notifications

### `oracle`

A module for utilities to be used with Oracle SQL databases

#### `oracle.factories`

Some extra cursor rowfactories for returning different types of data besides lists

## Usage

Basic usage with Teams webhook

```py
from bearlib.logging import core, webhooks

_logger = core.Logger(level="WARNING", echo=True, write=False)

teams = webhooks.Teams(
    hook_url="<Teams webhook URL>",
    summary="Example Teams Webhook",
    notify_only=False, # Set to true for no data to be sent
    subtitle="Example usage",
)

_logger.add_webhook(teams)

_logger.log("WARNING", "Something non-critical happened")

_logger.change_level("DEBUG")
_logger.log("DEBUG", "Debugging enabled")

_logger.close_log()
```
