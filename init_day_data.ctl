load   data
infile '002270.csv'
append   into   table DAY_002270
fields terminated by ','
trailing   nullcols
(
--------------------------------------------------------

    "date" DATE "yyyy-mm-dd",
	"OPEN",
	"HIGH" ,
	"CLOSE" ,
	"LOW" ,
	"VOLUME" ,
	"AMOUNT" ,
	"FACTOR"
)
