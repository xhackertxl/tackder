load   data
infile '000026.csv'
append   into   table DAY_002578
fields terminated by ','
trailing   nullcols
(
--------------------------------------------------------

    "DATE" DATE "yyyy-mm-dd",
	"OPEN",
	"HIGH" ,
	"CLOSE" ,
	"LOW" ,
	"VOLUME" ,
	"AMOUNT" ,
	"FACTOR" ,
	"MA_5" ,
	"MA_13" ,
	"MA_34" ,
	"MA_55" ,
	"MA_260" ,
	"EMA_5" ,
	"EMA_13" ,
	"EMA_34" ,
	"EMA_55" ,
	"EMA_260"
)
