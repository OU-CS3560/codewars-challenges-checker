> [!NOTE]  
> Depreated in favor of a GitHub action variant [OU-CS3560/check-codewars-kata](https://github.com/OU-CS3560/check-codewars-kata)

# Codewars Challenge Checker

## Requirements

```console
python -m pip install -r requirements.txt
```

## Usage

To check if users compelte at least N or more Katas.

```console
python cw_checker.py --n 2 users.csv
```

To check if users complete a specific Kata.

```console
python cw_checker.py --slug multiply users.csv
```
