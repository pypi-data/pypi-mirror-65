# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 11:03:46 2020

@author: yoelr
"""
import re

__all__ = ('to_searchable_format',)

def to_searchable_format(ID):    
    return re.sub(r"\B([A-Z])", r" \1", ID).capitalize().replace('_', ' ')