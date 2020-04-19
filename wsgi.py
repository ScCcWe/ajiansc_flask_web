# !/usr/bin/env python 
# -*- coding: utf-8 -*-
# file_name: wsgi.py
# author: ScCcWe
# time: 2020/4/19 13:17

import os

from dotenv import load_dotenv

# 手动设置环境变量
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# 导入程序实例
from app import app
