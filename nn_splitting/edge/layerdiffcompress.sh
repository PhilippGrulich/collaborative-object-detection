
#precisions=(1e-2 1e-3 1e-4 1e-5 1e-6 1e-7 1e-8 1e-9 1e-10 1e-11)
precisions=(1 2 4 6 8 12 16 24 32)

for image in data/*; do
   image=$(basename "$image")
   mkdir ./comp/$image
   for file in data/$image/*; do
    echo "process $image/$file"
    name=$(basename "$file")
    size=$(echo ${name##*_} | bc -l)
    mkdir ./comp/$image/$name/
    for var in "${precisions[@]}"
    do
      echo "${var}"
      ./3rdparty/zfp/bin/zfp -f -1 $size -i $file -z ./comp/$image/$name/$var -p $var -h

    done
   done
done







