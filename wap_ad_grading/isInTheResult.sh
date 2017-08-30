input=dadi.txt
source=noReduceWithPcResult.txt
output1=dadiInTheResult.txt
output2=dadiNotInTheResult.txt
rm -f $output1
rm -f $output2
sum=`cat $input | wc -l`
count=0
for line in `cat $input`
do
	count=`expr $count + 1`
	echo "sum:$sum now:$count"
	#echo $line
	#host=`python getHost.py $line`
	#echo $host
	result=`cat $source | grep $line`
	if test -z "$result"
	then
		echo "do not exist"
		echo $line >> $output2
	else
		echo "exist"
		echo $line >> $output1
	fi
done
