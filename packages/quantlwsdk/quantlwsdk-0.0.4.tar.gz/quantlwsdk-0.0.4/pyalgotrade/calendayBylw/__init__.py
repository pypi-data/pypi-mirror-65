# -*- coding: utf-8 -*-
"""
Created on Fri Dec  7 13:40:01 2018

@author: SH
"""


import pandas as pd
from pandas.tseries.offsets import DateOffset
import datetime
import time
from gm.api import *


class customTradeCalendar:
    
	#tradingDays 必须是字符串 list。即使一个list ，然后每个成员都是一个字符串
    def __init__(self,tradingDays):	# 重载构造函数
        sTradingDays = pd.Series(tradingDays,name='tradingDays')
        sTradingDays=sTradingDays.sort_values()
        self.sTradingDays = sTradingDays			# 创建成员变量并赋初始值
    def __del__(self):      		# 重载析构函数
        pass				# 空操作
        
        
#    def getMonthDays(self,date,offset):
#        rdataFetch = rdata.RData()
#        businessday_list = rdataFetch.get_businessday()
#        daySeries=pd.Series(businessday_list)
#        daySeries=daySeries.sort_values()
#        astartdt=daySeries.loc[daySeries>'2013'].iloc[0]
#        aenddt=daySeries.loc[daySeries<'2014'].iloc[-1]  


    def mDatesOffset(self,date,yoffset=0,moffset=0,doffset=0,leftOrright=-1):
        """
        本函数用来确定 普通日期的 上一个交易日，下一个交易日等

        :param date:  date 必须是字符串形式 。只能是日期
        :param yoffset:
        :param moffset:
        :param doffset:
        :param leftOrright: 这个参数表示，如果算出的日期不是一个交易日，落在两个交易日之间，那么应该选上一个交易日，还是下一个交易日。
        -1表示选上一个交易日 ，1表示选下一个交易日。
        :return:
        """
     
        from pandas.tseries.offsets import DateOffset
        import datetime
        newDate=datetime.datetime.strptime(date,'%Y-%m-%d')\
            + DateOffset(years=yoffset,months=moffset, days=doffset)
        strNewDate=newDate.strftime('%Y-%m-%d')
        
        
        
        # 即表示，如果当前日期date  要找一个偏移日期
        #如果是左偏的日期，那么就是往日期大的选，如果是右偏日期，就往日期小的选，总之，要让日期更靠近基准日期date

        aRDate = self.sTradingDays.loc[self.sTradingDays == strNewDate]
        if not aRDate.empty:
            return aRDate.iloc[0]
        else:
            if leftOrright==1:

                aRDate=self.sTradingDays.loc[self.sTradingDays>strNewDate].iloc[0]
            else:
                aRDate=self.sTradingDays.loc[self.sTradingDays<strNewDate].iloc[-1]
#        print(aRDate)
        return aRDate

    def mDateTimeOffset(self, datetime_, yoffset=0, moffset=0, doffset=0, leftOrright=-1,\
                        mhoffset=0,mmoffset=0,msoffset=0):
            """
            本函数用来确定 普通日期的 上一个交易日，下一个交易日等

            :param date:  date 必须是字符串形式 。只能是日期
            :param yoffset:
            :param moffset:
            :param doffset:
            :param leftOrright: 这个参数表示，如果算出的日期不是一个交易日，落在两个交易日之间，那么应该选上一个交易日，还是下一个交易日。
            -1表示选上一个交易日 ，1表示选下一个交易日。
            :return:
            """


            newDateTime = datetime.datetime.strptime(datetime_, '%Y-%m-%d %H:%M:%S') \
                      + DateOffset(years=yoffset, months=moffset, days=doffset,\
                                   hours=mhoffset,minutes=mmoffset,seconds=msoffset)

            strNewDateTime=newDateTime.strftime('%Y-%m-%d %H:%M:%S')
            strNewDate = strNewDateTime[0:10]

            # 即表示，如果当前日期date  要找一个偏移日期
            # 如果是左偏的日期，那么就是往日期大的选，如果是右偏日期，就往日期小的选，总之，要让日期更靠近基准日期date

            aRDate = self.sTradingDays.loc[self.sTradingDays == strNewDate]
            if not aRDate.empty:
                aRDate=aRDate.iloc[0]
            else:
                if leftOrright == 1:

                    aRDate = self.sTradingDays.loc[self.sTradingDays > strNewDate].iloc[0]
                else:
                    aRDate = self.sTradingDays.loc[self.sTradingDays < strNewDate].iloc[-1]
            #        print(aRDate)

            aRdateTime=aRDate+strNewDateTime[10:]
            return aRdateTime



    #本函数用来 推断 交易日的上一个交易日，下一个交易日等行为。
    def tradingDaysOffset(self,date,aoffset):
        
        if aoffset>0:
            aSeries=self.sTradingDays.loc[self.sTradingDays>date]
            if len(aSeries)<aoffset:
                return None
            else:
                return aSeries.iloc[aoffset-1]
            # return self.sTradingDays.loc[self.sTradingDays>date].iloc[0]
        if aoffset<0:

            aSeries = self.sTradingDays.loc[self.sTradingDays < date]
            if len(aSeries) < abs(aoffset):
                return None
            else:
                return aSeries.iloc[aoffset]
        if aoffset == 0:
            return date

    def isTradingDate(self,date):
        adate=self.sTradingDays.loc[self.sTradingDays == date]
        if adate.empty:
            return False
        else:
            return True
    


    #这个是给定一个带time的日期，要获得上一个交易日下一个交易日。
    #注意这里与下面函数不同在于，这里返回，只需要返回交易日，不需要交易日带时间
    #cdatetime可以是交易日，也可以不是交易日。所以给换了个函数名字
    # def tradingDateTimeOffset(self, cdatetime, aoffset):
    def tradeDateTimeTradingDateOffset(self, cdatetime, aoffset):
        #其实就是夜盘的问题
        #cdatetime 只能是交易时段的时间


        #1 比如20180713是周五，那么20180713 21：00之后的数据 是属于20180716日的数据。
        #2 但是 有的品种，夜盘时间很长，所以 20180714 这个是周六，但是从20180714 00：00 到02：00 也有数据，这个数据
        #应该也算到20180716的 日期上。

        #综上所述，就是处理这两种情况。

        #给几个例子
        #20190930 15：00，是9月最后一个交易日了，20191001是休息日。那么如果传入时间20191001 08：00，那么先确定这个时间属于交易日20191008
        #然后再根据交易日20191008 来确定是往上几个交易日
        #即这种非交易时段的时间，如何确定交易日，从这个逻辑看，就是



      # #算法1  性能太慢。主要是查找太多了。
      #
      #
      #   provideTime=cdatetime[11:13]
      #   provideDate=cdatetime[0:10]
      #
      #   #先判断是否是交易日。
      #   if self.isTradingDate(provideDate):
      #       if provideTime>='21':
      #           realTradedingDates=self.tradingDaysOffset(provideDate,aoffset=1)
      #       else:
      #           realTradedingDates=provideDate
      #   else:
      #       realTradedingDates = self.mDatesOffset(provideDate, leftOrright=1)
      #   return self.tradingDaysOffset(realTradedingDates,aoffset)


    #算法2

        provideTime = cdatetime[11:13]
        provideDate=cdatetime[0:10]

        aSeries=self.sTradingDays.loc[self.sTradingDays > cdatetime].head(1)
        index_=aSeries.index[0]
        smallDate=self.sTradingDays.loc[index_-1]
        bigDate = self.sTradingDays.loc[index_]

        #先判断是否是交易日。
        if provideDate==smallDate:  #是交易日
            if provideTime>='21':
                realTradedingDates=bigDate
            else:
                realTradedingDates=provideDate
        else:
            realTradedingDates = bigDate
        return self.tradingDaysOffset(realTradedingDates,aoffset)


        i=1






            # 本函数用来 推断 交易日的上一个交易日期时间，下一个交易日期时间的行为。
        #这函数先废弃。发现分钟时间要连起来，中间跳空的太多，比如晚上的跳，中午休市的跳。
    # def tradingDayTimesOffset(self, datetime_,doffset=0,exchangeCode='SHSE', mhoffset=0,mmoffset=0,msoffset=0):
    #
    #     date=datetime_[0:10]
    #
    #     newDate=''
    #     if doffset > 0:
    #         aSeries = self.sTradingDays.loc[self.sTradingDays > date]
    #         if len(aSeries) < doffset:
    #             return None
    #         else:
    #             newDate=aSeries.iloc[doffset - 1]
    #         # return self.sTradingDays.loc[self.sTradingDays>date].iloc[0]
    #     if doffset < 0:
    #
    #         aSeries = self.sTradingDays.loc[self.sTradingDays < date]
    #         if len(aSeries) < abs(doffset):
    #             return None
    #         else:
    #             newDate =aSeries.iloc[doffset]
    #     if doffset == 0:
    #         newDate =date
    #     strNewDateTime=newDate+datetime_[10:]
    #
    #
    #
    #     #
    #     # offsetDateTime = datetime.datetime.strptime(strNewDateTime, '%Y-%m-%d %H:%M:%S') \
    #     #               + DateOffset(hours=mhoffset, minutes=mmoffset, seconds=msoffset)
    #     #
    #     # strOffsetDateTime=offsetDateTime.strftime('%Y-%m-%d %H:%M:%S')
    #     #
    #     #
    #     # def tradeTimeMerge(strNowDateTime,aDayEndTime='15:00:00',aDayStartTime='09:00:00'):
    #     #
    #     #     nowDatetime=datetime.datetime.strptime(strNowDateTime, '%Y-%m-%d %H:%M:%S')
    #     #     currEndDateTime=strNowDateTime[0:10]+' '+aDayEndTime
    #     #
    #     #
    #     #
    #     #
    #     #     #说明结束时间结束之后，下一次开始时间在第二日
    #     #     if aDayEndTime>aDayStartTime:
    #     #         if strNowDateTime[11:]>aDayEndTime:
    #     #             # 越界了多长时间间隔。
    #     #             spanTime = nowDatetime-currEndDateTime
    #     #
    #     #
    #     #
    #     #
    #     #             strNextTDate=(offsetDateTime+DateOffset(days=1)).strftime('%Y-%m-%d')
    #     #
    #     #     # 说明结束时间结束之后，下一次开始时间在当日的晚些时候，比如期货中有夜盘的品种
    #     #     if aDayEndTime < aDayStartTime:
    #     #
    #     #         ii=1
    #     #
    #     #
    #     # if exchangeCode=='SZSE' or exchangeCode=='SHSE':
    #     #     tradeTimeMerge(strOffsetDateTime)
    #
    #
    #     return strNewDateTime
    #

    def nonTradeDateTimeTradingDateOffset(self, cdatetime, leftOrright,aoffset):

        #cdatetime 只能是非交易时段的时间
        '''

        首先，交易日序列 是 没有时间的。只有日期。那么如果给定一个日期时间，你无法判断是否该时间是否是 交易时段内。比如
        1、20190930 15：00，是9月最后一个交易日了，20191001是休息日。那么如果传入时间201910930 21：11， 这个明显是非交易时段，但是那是我们知道
        十一之前的交易日 晚上夜盘停掉了。而单独的交易日序列，是没有这个信息的
        2、20191018 15：00，是周五，20191021 是周一，那么20191018 21：11，这个明显又是交易时段。



        这个函数描述的是，如果一个日期时间是一个非交易时段的时间，那么肯定是夹在2个交易日之间，那么到底选哪个交易日。

        :param
        leftOrright: 这个参数表示，如果算出的日期不是一个交易日，落在两个交易日之间，那么应该选上一个交易日，还是下一个交易日。
        -1表示选上一个交易日 ，1表示选下一个交易日。
        '''


        atempTradingDateTimes = self.sTradingDays.copy()
        atempTradingDateTimes = atempTradingDateTimes + ' 15:00:00'
        aSeries = atempTradingDateTimes.loc[atempTradingDateTimes < cdatetime].tail(1)
        smallDateTime = aSeries.iloc[0]
        smallDate = smallDateTime[0:10]

        anotherSeries = atempTradingDateTimes.loc[atempTradingDateTimes > cdatetime].head(1)
        bigDateTime = anotherSeries.iloc[0]
        bigDate = bigDateTime[0:10]

        if leftOrright==-1:
            tDate=smallDate
        if leftOrright==1:
            tDate=bigDate


        return self.tradingDaysOffset(tDate,aoffset)



    def get_latest_finished_tradingdate(self,cdatetime):
        atempTradingDateTimes=self.sTradingDays.copy()
        atempTradingDateTimes=atempTradingDateTimes+' 15:00:00'
        aSeries = atempTradingDateTimes.loc[atempTradingDateTimes < cdatetime].tail(1)
        tDateTime=aSeries.iloc[0]
        tDate=tDateTime[0:10]
        return tDate

        
    def getADateTimeSeries(self,startDt,endDt):

        #看到rqalpha的一种实现

        # left = self.sTradingDays.searchsorted(startDt)
        # right = self.sTradingDays.searchsorted(endDt, side='right')
        # return self.sTradingDays[left:right]


        return self.sTradingDays.loc[(self.sTradingDays>=startDt)&(self.sTradingDays<=endDt)]

    def getNLastTradingDays(self,years=-1,months=-3,days=-2):


        #函数的作用。比如当前时间是20190704 09:31:53
        #那么第一个时间，就是当前时间 按照上面参数偏移 年月日，末尾时间，就在当前时间上一个时间。因为当前时间，可能有些行情取不到

        currDateTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        currDate = currDateTime[0:10]

        m1dt = datetime.datetime.strptime(currDate, '%Y-%m-%d') \
               + DateOffset(years=years, months=months,days=days)
        m1dtStr = m1dt.strftime('%Y-%m-%d')

        # m2dt = datetime.datetime.strptime(currDate, '%Y-%m-%d') \
        #        + DateOffset(days=days)
        m2dt = datetime.datetime.strptime(currDate, '%Y-%m-%d') \
               + DateOffset(days=-1)
        m2dtStr = m2dt.strftime('%Y-%m-%d')

        # aNewTradeCalendar=getACalendarInstance()

        sTradingDate = self.mDatesOffset(m1dtStr, yoffset=0, leftOrright=1)
        eTradingDate = self.mDatesOffset(m2dtStr, yoffset=0, leftOrright=-1)
        return (sTradingDate,eTradingDate)



#判断某个品种的某个交易日是不是它的交易日
#有的品种，在交易日可能也没有行情，所以 要单独判断下，该品种那天有没有交易
def isTrading(symbol,datetime_):
    from gm.api import history
    dt_=datetime.datetime.strptime(datetime_,'%Y-%m-%d')
    tempHQ = history(symbol=symbol, frequency='1d', start_time=dt_, end_time=dt_, fields=None, df=True)
    if tempHQ.empty:
        return False
    else:
        return  True


def getACalendarInstance():
    # 准备一个 日历对象。
    # currDateTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    currDateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    currDate = currDateTime[0:10]
    nextYearofToday = datetime.datetime.strptime(currDate, '%Y-%m-%d') \
                      + DateOffset(years=1)
    nextYearofTodayStr = nextYearofToday.strftime('%Y-%m-%d')
    aTradingDays = get_trading_dates(exchange='SHSE', start_date='2000-01-01', end_date=nextYearofTodayStr)
    aNewTradeCalendar = customTradeCalendar(aTradingDays)
    return aNewTradeCalendar



def getNLastTradingDays(aNewTradeCalendar,years=-1,months=-3,days=-2):
    currDateTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    currDate = currDateTime[0:10]

    m1dt = datetime.datetime.strptime(currDate, '%Y-%m-%d') \
           + DateOffset(years=years, months=months)
    m1dtStr = m1dt.strftime('%Y-%m-%d')

    m2dt = datetime.datetime.strptime(currDate, '%Y-%m-%d') \
           + DateOffset(days=days)
    m2dtStr = m2dt.strftime('%Y-%m-%d')

    # aNewTradeCalendar=getACalendarInstance()

    sTradingDate = aNewTradeCalendar.mDatesOffset(m1dtStr, yoffset=0, leftOrright=1)
    eTradingDate = aNewTradeCalendar.mDatesOffset(m2dtStr, yoffset=0, leftOrright=-1)
    return (sTradingDate,eTradingDate)