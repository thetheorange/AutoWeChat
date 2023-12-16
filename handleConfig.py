import json
import os.path

# 默认配置
init_config = {
    "interval": 1,
    "text_box": []
}

init_config = json.dumps(init_config)


# 读取配置文件
def read_config():
    try:
        if not os.path.exists("config.json"):
            with open("config.json", "w") as f:
                f.write(init_config)
        else:
            with open("config.json", "r") as f:
                return json.loads(f.read())
    except Exception as e:
        print(e)


# 修改配置文件
def modify_config(key, value):
    try:
        if not os.path.exists("config.json"):
            with open("config.json", "w") as f:
                f.write(init_config)
        else:
            # 读取旧数据
            with open("config.json", "r") as f:
                content = json.load(f)

            if key in content:
                content[key] = value
            else:
                print("not found key to update")

            # 写入新数据
            with open("config.json", "w") as f:
                json.dump(content, f, indent=2)
    except Exception as e:
        print(f"[MODIFY CONFIG] ERROR: {e}")
