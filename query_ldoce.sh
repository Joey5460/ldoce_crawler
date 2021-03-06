#!/usr/bin/bash
if [ -z $2 ]
then
    core_words='ldoce-core-vocabulary.txt'
else
	core_words=$2
fi

case $1 in 
    trim)
        #awk  '{OFS= "\t"}{for(i=2;i<5;i++) $i=""; print  $0}' $2 
        awk  '{printf("%15-s %s %s %s %s %s %s\n",$1,$5,$6,$7,$8,$9,$10);}' $2 
    ;;
    s)
        if [ -z $2 ]
        then
            egrep 'S1|S2|S3' $core_words
        else
            egrep 'S1|S2|S3' $2
        fi
    ;;
    w)
        if [ -z $2 ]
        then
            egrep 'W1|W2|W3' $core_words
        else
            egrep 'W1|W2|W3' $2
        fi
    ;;
    s1)
        if [ -z $2 ]
        then
            egrep 'S1' $core_words
        else
            egrep 'S1' $2
        fi
    ;;
    s2)
        if [ -z $2 ]
        then
            egrep 'S2' $core_words
        else
            egrep 'S2' $2
        fi
    ;;
    s3)
        if [ -z $2 ]
        then
            egrep 'S3' $core_words
        else
            egrep 'S3' $2
        fi
    ;;
    freq)
		egrep -v 'W1|W2|W3|S1|S2|S3' $core_words 
        ;;
    low)
        egrep -v 'W1|W2|W3|S1|S2|S3' $core_words| egrep '●○○'   
        ;;
    mid)
        egrep -v 'W1|W2|W3|S1|S2|S3' $core_words| egrep '●●○'   
        ;;
    high)
        egrep -v 'W1|W2|W3|S1|S2|S3' $core_words| egrep '●●●' 
        ;;
    *)
        ;;
esac
