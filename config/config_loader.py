import os
import yaml
import json
import argparse


class ConfigNamespace:
    """딕셔너리를 점 표기법으로 접근 가능하도록 변환하는 클래스"""

    def __init__(self, dictionary):
        self._data = dictionary
        for key, value in dictionary.items():
            setattr(self, key, ConfigLoader()._dict_to_attr(value))

    def __getitem__(self, key):
        return getattr(self, key)

    def __repr__(self):
        return json.dumps(self.__dict__, indent=4, ensure_ascii=False)

    def keys(self):
        return list(self._data.keys())

    def to_dict(self):
        return {key: self._to_dict(value) for key, value in self._data.items()}

    def _to_dict(self, obj):
        if isinstance(obj, ConfigNamespace):
            return obj.to_dict()
        elif isinstance(obj, list):
            return [self._to_dict(item) for item in obj]
        else:
            return obj


class ConfigLoader:
    _instance = None  # 싱글톤 인스턴스를 저장할 클래스 변수

    def __new__(cls, config_path="config.yaml"):
        if cls._instance is None:
            cls._instance = super(ConfigLoader, cls).__new__(cls)
            cls._instance.init_config(config_path)
        return cls._instance

    def init_config(self, config_path):
        """설정 파일을 로드하는 초기화 메서드"""
        self.config_path = config_path
        self.env = os.getenv("ENV", "DEV")  # 기본값: DEV
        self.file_config = self.load_file_config()  # 설정 파일 로드
        self.env_config = self.load_env_config()  # 환경변수 로드
        self.arg_config = self.load_arg_config()  # 명령줄 인자 파싱
        self.config = self.merge_config()  # 우선순위에 따라 병합

    def load_file_config(self):
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        with open(self.config_path, "r", encoding="utf-8") as f:
            config_data = yaml.safe_load(f)

        # 기본 설정을 먼저 불러오고, 환경별 설정을 덮어쓰기
        config = config_data.get("default", {}).copy()
        env_config = config_data.get("environments", {}).get(self.env, {})
        config.update(env_config)
        return config

    def load_env_config(self):
        """환경 변수로부터 설정을 불러오는 메서드"""
        config = {
            "account_name": os.getenv("ACCOUNT_NAME", ""),
            "product_names": os.getenv("PRODUCT_NAMES", "").split(),
            "access_key": os.getenv("ACCESS_KEY"),
            "secret_key": os.getenv("SECRET_KEY"),
        }
        return config

    def load_arg_config(self):
        parser = argparse.ArgumentParser(description="Metric Exporter CLI")
        parser.add_argument(
            "--account_name",
            "-a",
            help="Account name (huniverse, cmhos, symcs)",
        )

        args, unknown = parser.parse_known_args()
        return {key: value for key, value in vars(args).items() if value is not None}

    def merge_config(self):
        """설정 파일 → 환경변수 → 명령줄 인자의 우선순위로 병합"""
        merged_config = self.file_config.copy()

        # 환경변수 병합
        for key, value in self.env_config.items():
            if value is not None:
                merged_config[key] = value

        # 명령줄 인자 병합
        for key, value in self.arg_config.items():
            if value is not None:
                merged_config[key] = value

        return self._dict_to_attr(merged_config)

    def _dict_to_attr(self, data):
        """딕셔너리를 객체 속성처럼 접근 가능하도록 변환"""
        if isinstance(data, dict):
            return ConfigNamespace(data)
        elif isinstance(data, list):
            return [self._dict_to_attr(item) for item in data]
        return data

    def get(self, key, default=None):
        return self.config.get(key, default)

    def get_resource_types(self):
        return self.config.get("resource_types", {})

    def print_config(self):
        """현재 환경에 적용된 전체 설정을 출력"""
        print(f"Current ENV: {self.env}")
        print(json.dumps(self.config.to_dict(), indent=4, ensure_ascii=False))


config_loader = ConfigLoader()
config = config_loader.config
