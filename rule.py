#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fact import Fact

class Rule:
    def __init__(self, id, if_subject, if_condition, then_subject, then_condition, if_and=False, if_subject2 = None, if_condition2 = None):
        self.id = id
        self.if_fact = Fact(if_subject, if_condition)
        self.then_fact = Fact(then_subject, then_condition)
        self.if_and = if_and
        if if_and == True:
            self.if_fact2 = Fact(if_subject2, if_condition2)
        
        


