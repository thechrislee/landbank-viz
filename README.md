[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
# landbank

> plots Cuyahoga Landbank Properties

This application scrapes address data from [Cuyahoga Land Bank](https://cuyahogalandbank.org/land-bank-homes/). This data is then plotted to a nifty map. :house_with_garden:

## Installation

Use git to clone the repository.

```console
$ git clone https://github.com/thechrislee/landbank-viz.git
$ cd landbank-viz
$ poetry shell
```

## Usage

```console
$ landbank --help
Usage: landbank [OPTIONS] URL

Arguments:
  URL  [required]

Options:
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.

$ landbank https://cuyahogalandbank.org/all-available-properties/
```
![Info](https://user-images.githubusercontent.com/79058735/212891980-288e6882-b5fc-4c0a-aa83-fbaf1cbeac45.png)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)

