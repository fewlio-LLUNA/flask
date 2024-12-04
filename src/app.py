# -*- coding: utf-8 -*-
"""Webアプリのサンプルです"""

# ライブラリのインポート
from datetime import datetime, timedelta

# import weather_forecast
from flask import Flask, render_template, request
from markupsafe import Markup

import omikuji
import school_timetable_old

# Flaskのインスタンス化
application = Flask(__name__, static_folder="static", template_folder="templates")


@application.route("/")
@application.route("/index")
def index() -> str:
    """トップページ

    Returns:
        str: レンダリング結果
    """
    return render_template("./index.html")


@application.route("/tomorrow_plan", methods=["GET", "POST"])
def tomorrow_plan() -> str:
    """明日の予定を表示する

    Returns:
        str: レンダリング結果
    """
    # 明日の日付（曜日表示付き）
    DAY_NAME = "月火水木金土日"
    tomorrow_dt = datetime.now() + timedelta(days=1)
    tomorrow_dt_str = f"{tomorrow_dt.strftime('%Y/%m/%d')}({DAY_NAME[tomorrow_dt.weekday()]})"

    # # 明日の天気予報
    # weather_osaka = weather_forecast.get_osaka_tomorrow_weather()

    # 明日の時間割
    tomorrow_lessons = school_timetable_old.get_tomorrow_timetable()
    timetable = [[lesson.period, lesson.subject, lesson.classroom, lesson.teacher] for lesson in tomorrow_lessons]

    # おみくじを引く
    if request.method == "POST":
        fortune = omikuji.draw()
        fortune_result = fortune.result.value
        fortune_advice = fortune.advice
    else:  # GET
        fortune_result = ""
        fortune_advice = ""

    return render_template(
        "./tomorrow_plan.html",
        date=tomorrow_dt_str,
        weather_area="大阪",
        # weather_result=weather_osaka,
        school_timetable=timetable,
        fortune_result=fortune_result,
        fortune_advice=Markup(fortune_advice.replace("\n", "<br>")),
    )
