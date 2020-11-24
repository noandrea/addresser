# Addresser 

Parse unstructured address strings into structured ones.

> ⚠ This project is meant as an exercise and is not designed or implemented 
> for a specific use case or context. For the same reason the package is not 
> distributed via Pypy but has to be installed manually.

## Implementation 

The implemented strategy uses regular expression to identify patterns corresponding
to house numbers and treats the rest as a street name. W

> 🔍 strings that are identified as being an apartment number (eg. `Suite 32`)  are stripped
> from the result.

The heuristic used is to search first in the beginning of the string for something that looks
like a house number and failing that search to the end of the string for something that can be identified as a house number. 
The fallback when no house number can be identified is to use the complete input string as the street name.

## Installation 

Download the latest wheel binary from the [release](https://github.com/noandrea/addresser/releases/latest) page and install it using :

```
pip install addresser-$VERSION.py3.none-any.whl
```

To uninstall run:

```
pip uninstall addresser
```

## Usage 

`addresser` can be used both as a stand alone command line program and imported as a library.

### As a library 

The following is a code snippet showing how to import and use the library.

```python
# import addresser
from addresser.parser import parse

a = parse("viale Mazzini 234a")

print(a.street) # prints "viale Mazzini"
print(a.number) # prints "234a"
print(a.src) # prints the input string "viale Mazzini 234a"
```

### As a CLI

The following si an example how to run the CLI

```sh
|> addresser parse "viale Mazzini 234a"
{"street": "viale Mazzini", "housenumber": "234a"}
```

There are a few more commands available, use the `-h` to find out more

```sh
|> addresser -h
usage: addresser [-h] {parse,parse-file,generate-addresses,version} ...

positional arguments:
  {parse,parse-file,generate-addresses,version}
    parse               Parse an input string into a structured address
    parse-file          Parse a address list file into a JSONlines file
    generate-addresses  Generate a file with a list of addresses
    version             Print the version and exit

optional arguments:
  -h, --help            show this help message and exit

```


## Build 

The project uses [Poetry](https://python-poetry.org/) for packaging and a `Makefile` is provided with shortcuts:

Run linter (flake8) and type checks (mypy)
```
make lint
```

Run tests and produce coverage reports
```
make test 
```

Create packaged build
```
make build
```

## Performance 

The following is not by any mean an exhaustive performance analysis but only to give a general idea of the performance of the library. The test have been executed on a low power Intel CPU from 2019. 
```
1: addresser parse-file (100_000 records / 10 runs)
            Mean        Std.Dev.    Min         Median      Max
real        1.072       0.022       1.043       1.063       1.121       
user        1.019       0.026       0.977       1.017       1.073       
sys         0.050       0.008       0.040       0.048       0.064    
```



## Known Issues
- While the current implementation seems to work fairly well for the test set (generated with [`Faker`](https://github.com/joke2k/faker)), it is probably biased by what has been added to `Faker`.
- The `Faker` library is required as a non-dev dependency to be able to generate sample data via CLI, but in a real scenario that requirement is unnecessary.

## Faq

**Q**: Why have/haven't you used library X?  <br/>
**A**: I seek to use libraries that are well known, popular and maintained, but I don't know them all and I have my preferences; but I do not a crusader and I will use what is the most fit solution in the context. 

**Q**: You didn't write test for this/that, or tests are not covering 100%<br>
**A**: This is an exercise and a showcase, it is by no means meant to be a production software.


  

