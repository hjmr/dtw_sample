FROM=data_raw
TO=data
for name in JL-CW JW-CW MK-JW NR-JW ZR-CM
do
  for f in $(ls ${FROM}/${name}/h5/*.h5)
  do
    base=$(basename $f | sed -r "s/^.*[a-z]+([0-9]+\-[^-]+\.h5$)/\1/g")
    b=$(basename $base .h5)
    p=$(echo $b | cut -d"-" -f1)
    q=$(echo $b | cut -d"-" -f2)
    if [ ! -d ${TO}/${name} ]; then
      mkdir ${TO}/${name}
    fi
    if [ ! -d ${TO}/${name}/${p} ]; then
      mkdir ${TO}/${name}/${p}
    fi
    while [ -f ${TO}/${name}/${p}/${q}.h5 ]
    do
      let q=$q+1
    done
    cp $f ${TO}/${name}/${p}/${q}.h5
  done
done
