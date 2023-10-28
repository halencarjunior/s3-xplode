# s3-xplode
```sh
▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
█░▄▄█░▄▄░████░█░█▀▄▄▀██░████▀▄▄▀█░▄▀█░▄▄█
█▄▄▀███▄▀█▄▄█▀▄▀█░▀▀░██░████░██░█░█░█░▄▄█
█▄▄▄█░▀▀░████▄█▄█░█████░▀▀░██▄▄██▄▄██▄▄▄█
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
```

## _Xplode Public S3 And Scan for Secrets_
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](http://www.gnu.org/licenses/gpl-3.0)

S3-xplode is a script that will scan a public s3 bucket for secrets using Regex. So, what is the main difference between others: It will do everything "on the fly". No files are saved on the disk and no third-party software.

## Basic Requirements

- You should have a list of previously enumerated s3 with public permission.
- You could use my other script, sss3, to search for public buckets
- patterns.config file containing regex to scan for files. Edit this file and include your own regex for a secret type

## Usage

```python
$ git clone https://github.com/halencarjunior/s3-xplode.git
$ python3 s3-xplode

Choose 1 to scan for a single bucket
Choose 2 to name a file containing a list of bucket names
```

## Development

Want to contribute? Great! Please send your PR to us and we'll be grateful for your help.

Thanks for using and helping to share, please

**Free Software, Hell Yeah!**
