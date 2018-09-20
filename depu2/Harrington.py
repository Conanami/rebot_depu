import dealer
import math
import random
from dealer import IsDrawFlush
from dealer import IsDrawStraight
from read_pokerstar import getPubList
from read_pokerstar import getPubnum
from read_pokerstar import getCallchip
from read_pokerstar import getSurvivor
from read_pokerstar import getMyHand
from read_pokerstar import calcuWinrate


def makeDecision(rtSit):
    #得到还剩几个人
    leftman=getSurvivor(rtSit)[1]
    