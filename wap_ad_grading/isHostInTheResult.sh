input=dadi.txt
source=noReduceWithPcResult.txt
output1=dadiHostInTheResult.txt
output2=dadiHostNotInTheResult.txt
output3=dadiHostGrade.txt
rm -f $output1
rm -f $output2
count=0
sum=`cat $input | wc -l`
for line in `cat $input`
do
        count=`expr $count + 1`
        echo "sum:$sum  now:$count"
	#echo $line
	host=`python getHost.py $line`
	#echo $host
	result=`cat $source | grep $host | sed -n '1p'`
	if test -z "$result"
	then
		echo "do not exist"
		echo $line >> $output2
	else
		echo "exist"
		echo $line >> $output1
		echo $result >> $output3
	fi
done
