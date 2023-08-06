uniapi
===============
A Web Site check tool.

Install
===============
```
 pip install webcheck
```

Useage
===============
Show help
```bash
python -m webcheck -h
```
Check url
```bash
python -m webcheck http://www.baidu.com
```
Or check urls
```bash
python -m webcheck http://www.baidu.com https://www.qq.com https://www.tt.com
```
Or check urls store in a file(urls.txt)
```bash
python -m webcheck -f urls.txt
```