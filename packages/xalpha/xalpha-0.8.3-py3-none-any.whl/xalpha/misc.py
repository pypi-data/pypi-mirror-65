# -*- coding: utf-8 -*-
"""
modules for misc crawler without unfied API
"""

import pandas as pd
from bs4 import BeautifulSoup
from xalpha.cons import rget


def get_ri_status(suburl=None):
    if not suburl:
        suburl = "m=cb&a=cb_all" # 可转债

    url = "http://www.richvest.com/index.php?"
    url += suburl
    r = rget(url, headers={"user-agent": "Mozilla/5.0"})
    b = BeautifulSoup(r.text, "lxml")
    cl = []
    for c in b.findAll("th"):
        cl.append(c.text)
    nocl = len(cl)
    rl = []
    for i, c in enumerate(b.findAll("td")):
        if i % nocl == 0:
            r = []
        r.append(c.text)
        if i % nocl == nocl - 1:
            rl.append(r)
    return pd.DataFrame(rl, columns=cl)
