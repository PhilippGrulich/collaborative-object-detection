
precisions=(1e-2 1e-3 1e-4 1e-5 1e-6 1e-7 1e-8 1e-9 1e-10 1e-11)

for frame in comp/*; do
   for layer in $frame/*; do
    for file in $layer/*; do
    echo "process $file"
    c="_decomp"
    res=$file$c
    ./3rdparty/zfp/bin/zfp -h -z $file -o $res
    done
   done
done







