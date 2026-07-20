import configparser
import pathlib


def read_conf(section=None, key=None):
    file = pathlib.Path(__file__).parent.parent/'conf'/'conf.ini'

    try:
        # 创建配置解析器
        conf = configparser.ConfigParser()
        conf.read(file, encoding='utf-8')
        # 根据参数返回不同结果
        if section and key:
            # 返回具体的配置值
            return conf[section][key]
        elif section:
            # 返回指定段落的所有配置
            return dict(conf.items(section))
        else:
            # 返回整个配置文件
            result = {}
            for section_name in conf.sections():
                result[section_name] = dict(conf.items(section_name))
            return result
    except Exception as e:
        print(f"读取配置文件失败: {e}")
        return None


