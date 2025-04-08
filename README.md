> !!! 已停止维护，强烈建议使用 [FfmpegZZZ/JMComic-Api](https://github.com/FfmpegZZZ/JMComic-Api) !!!

## 使用方法(docker和直接运行二选一即可)

### 直接运行

1. **下载源码包并解压**，进入项目根目录

2. **创建虚拟环境**：
     ```bash
     python -m venv .venv
     ```

3. **激活虚拟环境**：
    - 在 Windows 上：
      ```bash
      .\.venv\Scripts\activate
      ```
    - 在 macOS 或 Linux 上：
      ```bash
      source .venv/bin/activate
      ```

4. **安装依赖**：
     ```bash
     pip install -r requirements.txt
     ```
5. **运行**
    ```bash
    python main.py 
    ```

### 使用docker

```bash
docker run -d -p 8699:8699 linglambda/jmcomic-api
```
