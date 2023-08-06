#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : Python.
# @File         : zk_app
# @Time         : 2020-03-11 14:39
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : Python.
# @File         : app
# @Time         : 2020-03-11 13:54
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : http://zkview.d.xiaomi.net/clusters/tjwqstaging/nodes?path=%2Fmipush%2Fhive&isAdmin=false


import time
import pandas as pd
from typing import Optional
from fastapi import FastAPI, Form, Depends, File, UploadFile
from pydantic import BaseModel
from starlette.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.responses import \
    RedirectResponse, FileResponse, HTMLResponse, PlainTextResponse
from starlette.status import *

from ..utils.zk_client import Config  # 获取zk配置

ROUTE = ""
app = FastAPI(
    debug=True,
    openapi_url=f"{ROUTE}/openapi.json",
    docs_url=f"{ROUTE}/docs",
    redoc_url=f"{ROUTE}/redoc",
    swagger_ui_oauth2_redirect_url=f"{ROUTE}/docs/oauth2-redirect"
)


@app.get("/")
async def read_root():
    print(f"App: {Config.zk_cfg}")
    return {"Hello": "World"}


if __name__ == '__main__':
    import os
    import socket

    me = socket.gethostname() == 'yuanjie-Mac.local'

    uvicorn = "uvicorn" if me else "/opt/soft/python3/bin/uvicorn"

    main_file = __file__.split('/')[-1].split('.')[0]

    # --reload测试环境
    os.system(f"uvicorn {main_file}:app --reload --host 0.0.0.0 --port 8000")
