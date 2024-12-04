# -*- coding: utf-8 -*-
"""時間割"""

# ライブラリのインポート
import csv
import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import List

# ロギングの設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 定数
CSV_PATH = Path("./school_timetable.csv")  # 時間割csvファイルのパス


@dataclass
class Lesson:
    """授業情報を格納するデータクラス"""

    period: str  # 時限
    subject: str  # 科目
    classroom: str  # 教室
    teacher: str  # 先生


class TimetableManager:
    """時間割管理クラス"""

    def __init__(self, file_path: Path):
        self.file_path = file_path

    def read_timetable(self) -> List[List[str]]:
        """CSVファイルから時間割を読み込む

        Returns:
            List[List[str]]: 時間割[[日付, 時限, 科目, 教室, 先生]]
        """
        try:
            if not self.file_path.exists():
                logger.error(f"ファイルが存在しません: {self.file_path}")
                return []

            with self.file_path.open(encoding="utf-8", newline="") as f:
                return [[s.strip() for s in row] for row in csv.reader(f) if row]
        except Exception as e:
            logger.error(f"ファイル読み込みエラー: {e}")
            return []

    def get_timetable_for_date(self, target_date: datetime) -> List[Lesson]:
        """指定日の時間割を取得する

        Args:
            target_date (datetime): 指定日

        Returns:
            List[Lesson]: 1日分の時間割[授業情報クラス]
        """
        date_str = target_date.strftime("%Y%m%d")
        timetable = self.read_timetable()

        lessons = []
        for row in timetable:
            if row and row[0] == date_str:
                lessons.append(Lesson(period=row[1], subject=row[2], classroom=row[3], teacher=row[4]))
        return lessons


def get_tomorrow_timetable() -> List[Lesson]:
    """明日の時間割を取得する

    Returns:
        List[Lesson]: 明日の時間割[授業情報クラス]
    """
    manager = TimetableManager(CSV_PATH)
    tomorrow = datetime.now() + timedelta(days=1)
    return manager.get_timetable_for_date(tomorrow)


if __name__ == "__main__":
    tomorrow_lessons = get_tomorrow_timetable()
    if tomorrow_lessons:
        for lesson in tomorrow_lessons:
            print(
                f"時限: {lesson.period}, 科目: {lesson.subject}, " f"教室: {lesson.classroom}, 担当: {lesson.teacher}"
            )
    else:
        print("明日の時間割はありません")
