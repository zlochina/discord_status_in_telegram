# Discord Status in Telegram

An application that bridges Discord and Telegram, providing real-time updates on voice channel activity and text messages from a Discord server to a Telegram chat.

## Table of Contents

1. [Features](#features)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Usage](#usage)
6. [Contributing](#contributing)
7. [License](#license)

## Features

- Real-time forwarding of Discord voice channel status to Telegram
  - Triggers notifications when users join or leave voice channels in the specified Discord guild
- Forwarding of text messages from Discord guild text channels to Telegram

## Requirements

- Python >= 3.7.1
- Poetry (for dependency management)

## Installation

1. Clone this repository:
   ```sh
   git clone https://github.com/zlochina/discord_status_in_telegram.git
   cd discord_status_in_telegram
   ```

2. Install the required dependencies using Poetry:
   ```sh
   poetry install
   ```

## Configuration

1. Create a `config.ini` file in the root directory:
   ```sh
   cp config-EXAMPLE.ini config.ini
   ```

2. Open `config.ini` and fill in the required key-value pairs:
   - Discord bot token
   - Discord guild ID
   - Telegram bot token
   - Telegram chat ID

## Usage

To run the application:

```sh
poetry run app
```

This command will start the Discord-Telegram bridge, and you should begin seeing updates in your specified Telegram chat.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Make your changes and commit them with descriptive commit messages
4. Push your changes to your fork
5. Submit a pull request to the main repository

Please ensure that your code adheres to the project's coding standards and includes appropriate tests.

## License

This project is licensed under the [MIT License](./LICENSE).
