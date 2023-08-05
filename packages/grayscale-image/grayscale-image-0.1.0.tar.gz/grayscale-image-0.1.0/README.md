# grayscale-image

Grayscale image.

## Install

```shell
pip install grayscale-image
```

## Installed Command Utils

- grayscale-image

## Usage

```shell
C:\Code\grayscale-image>grayscale-image --help
Usage: grayscale-image [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  file    Grayscale an image file.
  folder  Grayscale .png and .jpg images in a folder.

C:\Code\grayscale-image>grayscale-image file --help
Usage: grayscale-image file [OPTIONS] SRC_FILE DST_FILE

  Grayscale an image file.

Options:
  --help  Show this message and exit.

C:\Code\grayscale-image>grayscale-image folder --help
Usage: grayscale-image folder [OPTIONS] SRC_ROOT DST_ROOT

  Grayscale .png and .jpg images in a folder.

Options:
  --help  Show this message and exit.
```

## Examples


```shell
grayscale-image file a.png b.png
```

- Grayscale a.png and save to b.png.

```shell
grayscale-image folder src dst
```

- Grayscale all .png and .jpg images in src folder, and save them to dst folder.


## Releases

### v0.1.0 2020/04/05

- First release.
