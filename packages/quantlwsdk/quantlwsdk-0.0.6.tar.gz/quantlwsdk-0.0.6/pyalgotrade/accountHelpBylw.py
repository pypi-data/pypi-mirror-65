# -*- coding: utf-8 -*-
"""
20200410 lw

"""
from gm.api import get_orders,OrderSide_Buy,OrderSide_Sell,PositionEffect_Open,PositionEffect_Close,PositionEffect_CloseToday,PositionEffect_CloseYesterday

from pyalgotrade.utils import cusHoldingPostion
import pymongo
from datetime import timezone
from datetime import timedelta


#这个类从rqalpha搬过来的
class Positions(dict):
    def __init__(self, position_cls):
        super(Positions, self).__init__()
        self._position_cls = position_cls
        self._cached_positions = {}

    def __missing__(self, key):
        if key not in self._cached_positions:
            self._cached_positions[key] = self._position_cls(key)
        return self._cached_positions[key]

    def get_or_create(self, symbol,positionSide):

        key=symbol+'_'+str(positionSide)
        if key not in self:
            self[key] = self._position_cls(key)
        return self[key]



class baseAccount():
    def __init__(self, positions):
        self._positions=positions

    def ontrade(self, gmTrade):
        symbol_ = gmTrade.symbol
        side_ = gmTrade.side
        self._positions.get_or_create(symbol_,side_).ontrade(trade)



class mongoAccount():
    #=dbname='real_short_period',collectionname='holding'
    def __init__(self, dbname,collectionname,host='localhost'):
        client = pymongo.MongoClient(host=host, port=27017,tz_aware=True)
        db = client[dbname]
        self.collection = db[collectionname]

    def ontrade(self,gmTrade):

        symbol_ = gmTrade.symbol
        side_ = gmTrade.side
        vol_ = gmTrade.volume
        price_ = gmTrade.price
        time_=gmTrade.created_at
        #如果是平仓指令，则需要减去持仓
        if gmTrade.positionEffect in [PositionEffect_Close, PositionEffect_CloseToday,
                                      PositionEffect_CloseYesterday]:

            # symbol_ = gmTrade['symbol']
            # side_ = gmTrade['side']
            # vol_=gmTrade['volume']

            if side_==1: #说明是买平.就需要查找空头持仓
                idstr=symbol_+'_2'
            if side_==2: #说明是卖平.就需要查找多头 持仓
                idstr = symbol_ + '_1'


            self.collection.update({'_id':idstr},{'$inc':{"vol":-vol_},'$set':{'updated_at':time_}})
            self.collection.remove({'vol': 0})  #如果持仓为0了，就剔除掉该持仓。

        if gmTrade.positionEffect in [PositionEffect_Open]:


            if side_ == 1:  # 说明是买开.就需要查找多头持仓
                idstr = symbol_ + '_1'
            if side_ == 2:  # 说明是卖开.就需要查找空头 持仓
                idstr = symbol_ + '_2'

            currHolding=self.collection.find_one({'_id':idstr})

            if currHolding is not None:
                newVwap=(currHolding['vwap']*currHolding['vol']+ price_*vol_)/(currHolding['vol']+vol_)
                self.collection.update({'_id': idstr}, {'$set': {"vwap": newVwap,'updated_at':time_},'$inc':{'vol':vol_}})
            else:
                adoc={}
                adoc['_id']=idstr
                adoc['vwap'] = price_
                adoc['vol'] = vol_
                adoc['created_at'] = time_
                adoc['updated_at'] = time_
                self.collection.insert(adoc)


    def getHolding(self,symbol,poside,timeZoneNum=8):
        #poside 必须是字符串的1或者2
        idstr = symbol + '_'+poside
        currHolding = self.collection.find_one({'_id': idstr})
        if currHolding is not None:
            idstr=currHolding['_id']

            symbol_,positionSide=idstr.split('_')
            volume=currHolding['vol']
            vwap = currHolding['vwap']
            created_at = currHolding['created_at'].astimezone(timezone(timedelta(hours=timeZoneNum)))
            updated_at = currHolding['updated_at'].astimezone(timezone(timedelta(hours=timeZoneNum)))
            ahol=cusHoldingPostion.__from_create__(symbol,positionSide,volume,vwap,created_at,updated_at)
            return ahol

        i=1
