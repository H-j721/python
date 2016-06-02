# -*- coding:utf-8 -*-

__author__ = 'JiangHE'

'''
longest Palindrome
'''

# Create time   : 2016-04-03 23:21
# Last modified : 2016-04-03 23:27
#########################################################

# RL回文半径数组: RL[i]表示以第i个字符为对称轴的回文串的回文半径
# maxRight: 当前访问到的所有回文子串,所能触及的最右一个字符的位置
# pos: MaxRight对应的回文串的对称轴所在的位置

def manacher(s):
    s = '#' + '#'.join(s) + '#'

    RL = [0] * len(s)
    maxRight = 0
    maxLen = 0
    pos = 0

    for i in range(len(s)):
        if i < maxRight:
            RL[i] = min(RL[2 * pos - i], maxRight - i)
        else:
            RL[i] = 1

        while i - RL[i] > 0 and i + RL[i] < len(s) and s[i - RL[i]] == s[i + RL[i]]:
            RL[i] += 1
        if RL[i] + i - 1 > maxRight:
            maxRight = RL[i] + i - 1
            pos = i
        maxLen = max(maxLen, RL[i])
    return maxLen - 1
