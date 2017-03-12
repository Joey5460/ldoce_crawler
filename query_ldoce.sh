#!/usr/bin/bash
case $1 in 
    s)
        egrep 'S1|S2|S3' core_vocabulary.lm
        ;;
    t)
        #awk  '{OFS= "\t"}{for(i=2;i<5;i++) $i=""; print  $0}' $2 
        awk  '{printf("%15-s %s %s %s %s %s %s\n",$1,$5,$6,$7,$8,$9,$10);}' $2 
        ;;
    *)
        ;;
esac
