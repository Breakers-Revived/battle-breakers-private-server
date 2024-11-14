# Contributing

Contributions are welcome for this server emulator on this repository! When contributing to this repository, 
please first discuss the change you wish to make on our
[Battle Breakers Fan Discord Server](https://discord.gg/3Hpv72hvvx), or via an issue.

> [!IMPORTANT]
> Pull requests should be made to the **development** branch only.

## Development Environment Setup

### Prerequisites

- [Python 3.11+](https://www.python.org/downloads/)
- [MongoDB](https://www.mongodb.com/try/download/community)
- [Git](https://git-scm.com/downloads)

### Installation

1. Clone the repository on the development branch

    ```sh
    git clone --recurse-submodules https://github.com/dippyshere/battle-breakers-private-server.git -b development
    cd battle-breakers-private-server
    ```

2. Set up a virtual environment and install the required packages

    ```sh
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3. Ensure the MongoDB server has been started

   (Windows)
    ```cmd
    net start MongoDB
    ```

   (Linux)
    ```bash
    sudo systemctl start mongodb
    ```

   > [!NOTE]
   > Depending on your MongoDB installation you may need to use `mongod` instead of `mongodb`.

   (macOS)
    ```shell
    brew services start mongodb-community
    ```

4. Start the server

    ```sh
    sanic main:app
    ```

5. Configure the game to connect to your server

    This can be done by modifying Engine.ini, using a reverse proxy, or by using the [AndroidPatcherCLI](https://github.com/Breakers-Revived/AndroidPatcherCLI)

6. Make your changes and submit a pull request to the development branch.

## Support & Community

If you need help with anything, or have any questions, suggestions / requests, or would like to get back into a Battle
Breakers community, please join the [Discord server](https://discord.gg/3Hpv72hvvx)!