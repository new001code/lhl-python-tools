# lhl-python-tools

This is a kit for python development.

## 安装

```bash
pip install lhl-python-tools
```

## 使用

Some of the features of this tool are based on the file `$project/conf/lhl_tools_config.yml`

lhl_tools_config.yml

```yml
# email
email:
  host: xxx(smtp.xxx.com)
  port: xxx(25)
  user: xxx(your_email@gmail.com)
  password: xxx(your_password_token)

# async-tools, define some thread or process pool information
async-tools:
  thread-pool:
    - thread_name: max_workers
    - default: 10
  process-pool:
    - process_name: max_workers
    - default: 1
  
# logger, see [loguru-config](https://github.com/erezinman/loguru-config)
logger:
  handlers:
  - sink: ext://sys.stderr
    format: '[{time}] {message}'
  - sink: file.log
    enqueue: true
    serialize: true
  levels:
    - name: NEW
      'no': 13
      icon: ¤
      color: ""
  extra:
    common_to_all: default
  activation:
    - [ "my_module.secret", false ]
    - [ "another_library.module", true ]
```
