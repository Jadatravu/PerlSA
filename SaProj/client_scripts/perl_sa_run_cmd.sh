#!/bin/sh
PERL5LIB=/home/user/perl5/lib/perl5/; export PERL5LIB
cd $1 $2
#build=`date +%Y_%m_%d_%H_%M_%S`
build=2015_09_14_10_31_50
mkdir -p /tmp/$build
#for p in `find . -type f \( -name \"*.pm\" -o -name \"*.pl\" \)`
for p in `find . -type f \( -name "*.pm" -o -name "*.pl" \)`
do
out_file=/tmp/$build/`echo $p | tr '//' '^'` 
echo $p
perlcritic --brutal  --verbose "+^%l^%c^%s^%m^+\n" $p > $out_file 
#python /usr/share/PerlSA/issues_upload.py  $out_file  $build  $2 
python /usr/share/PerlSA/issues_upload_cmd.py  $out_file  $build  $2 
done

