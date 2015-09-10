#!/bin/sh
PERL5LIB=/home/user/perl5/lib/perl5/; export PERL5LIB
cd $1 $2
build=`date +%Y_%m_%d_%H_%M_%S`
mkdir -p /tmp/$build
for p in `find . -name "*.pl"`
do
out_file=/tmp/$build/`echo $p | tr '//' '^'` 
perlcritic --brutal  --verbose "+^%l^%c^%s^%m^+\n" $p > $out_file 
python /home/user/issues_check_status.py  $out_file  $build  $2 
done

