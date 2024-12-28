# satori-to-anki

Automatically create new Anki flashcards from your Satori Reader flashcards.

# Installation

1. Clone the repository
1. Install the dependencies with `uv sync`
1. Symlink the plugin into your Anki plugins directory
   ```sh
   ln -s $(pwd) [Anki plugins directory]
   ```
1. Restart Anki

# Usage

1. Create a new deck named "Satori Reader" with the template here: https://ankiweb.net/shared/info/1941232915
1. Tools > Login to Satori Reader
1. Tools > Sync Satori Reader

From then on, any new flashcards you create in Satori Reader will be automatically imported into Anki upon sync.
