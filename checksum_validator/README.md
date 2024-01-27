# Usage

The `checksums.txt` must be in the following format:

```text
9c569f964ac3095d1e48bc30296659459d27733a  /usr/sbin/capsh
3f89ead7de5698e05e7a6dbd9c1c69df0a59dd5f  /usr/sbin/getcap
ec7f295cdf4ead62a4c30ebb871e2846a4a48ef3  /usr/sbin/getpcaps
e972ed0d1c921e5b7a53a4840dcff59c4920e34f  /usr/sbin/setcap
e15d611c315431d71fae6e7eb3ad1bcced5b0385  /etc/fix-attrs.d/01-resolver-resolv
4f29720883559a74be03f4de69de2f66113b064b  /etc/logrotate.d/acpid
a2587c4e97408b64274e5e052b74e3754892c13a  /etc/ssl/ct_log_list.cnf
c06bb154438af6218b8f58bc0f70520674fb3090  /etc/ssl/openssl.cnf
09932372e8a3560633070e64922fa848e1c62ba4  /etc/sysctl.d/00-alpine.conf
86a55b51f64e11d16d4cce9a34dfe34d9c6bed5e  /etc/cont-init.d/10-adduser
5dc0b601585c94dcb08afc13ca010f4f2529c2f3  /etc/cont-init.d/30-resolver
afb7b065503e748794e1adeba62b48b9c01e3e61  /etc/cont-init.d/40-resolver
4361398866dab0c3689c0d050aa84567d3afed6a  /etc/cont-init.d/99-add-flag
```

## Python
```commandline
python checksum_validator.py checksums.txt
```

## Shell
```commandline
sh checksum_validator.sh checksums.txt
```