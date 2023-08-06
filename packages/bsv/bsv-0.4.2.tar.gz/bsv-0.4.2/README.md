主要功能
-------------
下载国内四大期货交易所历史成交与持仓排名数据。



脚本执行时间
-------------

- 交易所与期货公司结算步骤完成后，网站公布当天数据。若结算延迟，则可能影响数据的正常发布；

- 如果进行每日更新，则更新脚本的启动时间设置在当日下午五点之后，非交易日无数据。



交易所数据区别
----------------

2020年1月1日前，商品期货数据统计口径均按双边计算，金融期货按单边计算；之后均按单边计算。

- CFFEX

  同一交易日所有品种持仓排名数据不在同一个页面呈现，以各自品种分开呈现；

- INE

  暂无SC品种成交持仓排名数据公布；

- DCE

  通过下载压缩包并解析txt文件来获取单个交易日数据，但部分交易日压缩包无数据；

  2008-08-28, 2011-12-02, 2013-11-27, 2013-11-28, 2013-11-29, 

  2016-01-04, 2016-01-07, 2018-04-09, 2018-05-02

- CZCE

  网页结构不统一，需要区别对待，公布品种级别的汇总数据。



交易所公布标准
--------------

- SHFE
    http://www.shfe.com.cn/statements/decl/911319239.html
- CFFEX
    单边持仓达到1万手以上（含）和当月合约前20名结算会员的成交量、持仓量
- DCE
    根据相关规则，期货品种信息公布活跃月份（双边持仓量大于、等于2万手）合约，期权品种信息公布活跃月份（标的期货合约双边持仓量大于、等于2万手）合约系列 。
- CZCE
    暂无，待补充。



变量名称
------------

``交易所`` 

缩写 | 英文全称 | 中文全称 
:-: | :-: |:-: 
SHFE | Shanghai Futures Exchange| 上海期货交易所 
CFFEX | China Financial Futures Exchange| 中国金融期货交易所 
DCE | Dalian Commodity Exchange| 大连商品交易所 
CZCE | Zhengzhou Commodity Exchange| 郑州商品交易所 

``代码字段`` 

| 代码 |  字段  |
| :--: | :----: |
|  hp  | 持仓量 |
|  v   | 成交量 |
|  b   | 买持量 |
|  s   | 卖持量 |

``返回字段`` 

| 代码     |      字段      | python格式 |
| :------- | :------------: | ---------: |
| tday     |     交易日     |        str |
| ex       |     交易所     |        str |
| code     |    品种代码    |        str |
| product  |    品种中文    |        str |
| contract |    合约代码    |        str |
| symbol   | 成交/买持/卖持 |        str |
| rank     |      排名      |        int |
| member   |    会员单位    |        str |
| value    |    合约手数    |        int |
| Change   |     变化量     |        int |

``样例代码``

- 下载交易日数据

    ```python
    from downloader import hp_shfe, hp_cffex, hp_dce, hp_czce
    
    trading_day = '20190701'  # 日期格式必须为%Y%m%d
    
    for row in hp_shfe(trading_day):
        print(row)
    
    for row in hp_cffex(trading_day):
        print(row)
    
    for row in hp_dce(trading_day):
        print(row)
    
    for row in hp_czce(trading_day):
        print(row)
    ```

- dce压缩包无数据时，使用该交易日前后各三个交易日的所有合约列表进行post访问

    ```python
    from downloader import hp_dce_post
    trading_day = '20190701'
    code = 'A'
    contract = 'A1909'
    product = '豆一'
    
    for row in hp_dce_post(trading_day, code, contract, product):
        print(row)
    ```
