temp="/user/antispam/wangyuan/temp.temp"
#output="/user/antispam/wangyuan/temp"
date
hadoop fs -rmr ${temp}

#hadoop jar antispam2.jar com.sogou.antispam.page.task.WebPageADFromHbase -DprocessUrl="http://4195702.71ab.com/index.asp" -Dmapreduce.fileoutputcommitter.algorithm.version=2 -Dorigin.page.splitable=true -Dmapreduce.map.memory.mb=5600 -Dmapreduce.map.java.opts=-Xmx4000m -files=adblock.model ${temp} 0
#-DprocessUrl="http://www.ddlsu.cn/"
hadoop jar antispam.jar com.sogou.ad.task.WapAdGrading -Dmapreduce.fileoutputcommitter.algorithm.version=2 -Dorigin.page.splitable=true -Dmapreduce.map.memory.mb=5600 -Dmapreduce.map.java.opts=-Xmx4000m -files=adblock.model ${temp} 100 | tee log/runWithList.log 2>&1 
if [ $? -ne 0 ]; then
    echo "Running job failed!"
     #   sendSms "/search/wunan208014/adRule/run.sh failed!!"
    exit 1;
else
    echo "Running job success!"
    # sendSms "/search/wunan208014/adRule/run.sh success!!"
       # hadoop fs -rmr $output
       # hadoop fs -mv $temp $output
       # sh -x prefix.sh
       # sh -x split.sh
fi
outputDir=0829
rm -r result/$outputDir
mkdir result/$outputDir
outputFile=result/$outputDir/all.txt
hadoop fs -getmerge /user/antispam/wangyuan/temp.temp/ $outputFile
cat $outputFile | wc -l
cat $outputFile | awk '{print $1,$3}' | awk '{if($2>0.7 && $2<1) printf("%s\t%s\n",$1,0);}' | sed -n '1,500p' > result/$outputDir/grade.txt
cat $outputFile | awk '{print $1,$3}' | awk '{if($2>0.5 && $2<0.7) printf("%s\t%s\n",$1,1);}' | sed -n '1,500p' >> result/$outputDir/grade.txt
cat $outputFile | awk '{print $1,$3}' | awk '{if($2>0.3 && $2<0.5) printf("%s\t%s\n",$1,2);}' | sed -n '1,500p' >> result/$outputDir/grade.txt
cat $outputFile | awk '{print $1,$3}' | awk '{if($2>0 && $2<0.3) printf("%s\t%s\n",$1,3);}' | sed -n '1,500p' >> result/$outputDir/grade.txt

#cat $outputFile | awk '{print $1,$3,$8}' | sort -u -k3 | awk '{if($2>0.7 && $2<1) printf("%s\t%s\n",$1,0);}' | sed -n '1,500p' > result/$outputDir/grade.txt
#cat $outputFile | awk '{print $1,$3,$8}' | sort -u -k3 | awk '{if($2>0.5 && $2<0.7) printf("%s\t%s\n",$1,1);}' | sed -n '1,500p' >> result/$outputDir/grade.txt
#cat $outputFile | awk '{print $1,$3,$8}' | sort -u -k3 | awk '{if($2>0.3 && $2<0.5) printf("%s\t%s\n",$1,2);}' | sed -n '1,500p' >> result/$outputDir/grade.txt
#cat $outputFile | awk '{print $1,$3,$8}' | sort -u -k3 | awk '{if($2>0 && $2<03.) printf("%s\t%s\n",$1,3);}' | sed -n '1,500p' >> result/$outputDir/grade.txt

#cat result/$outputDir/grade.txt | wc -l

#rm -f $outputFile

