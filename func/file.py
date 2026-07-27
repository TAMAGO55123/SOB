import os
from typing import Any
import json
from func.log import get_log

class File:
    def __init__(self, path:str) -> None:
        """
        設定ファイル管理用クラス
        JSONであること。
        """
        self.log = get_log(f"File.py")
        try:
            with open(path, mode="x") as f:
                json.dump({}, f)
            self.log.info(f"{path}が存在しないため、ファイルを作成しました。")
        except FileExistsError:
            pass
        if not path.endswith(".json"):
            raise ValueError("JSONファイルのパスを指定してください")
        self.file_path:str = path
    
    def get(self, key: str) -> Any:
        with open(self.file_path, "r") as f:
            data = json.load(f)
        if key not in data:
            raise KeyError(f"{key}が存在しません。")
        return data[key]
    def get_all(self) -> dict:
        with open(self.file_path, "r") as f:
            return json.load(f)
    def set(self, key:str, value:Any) -> None:
        d = self.get_all()
        d[key] = value
        with open(self.file_path, "w") as f:
            json.dump(d, f, indent=4, ensure_ascii=False)
    def delete(self, key:str):
        d = self.get_all()
        d.pop(key)
        with open(self.file_path, "w") as f:
            json.dump(d, f, indent=4, ensure_ascii=False)