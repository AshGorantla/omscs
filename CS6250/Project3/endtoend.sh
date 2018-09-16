#!/bin/bash

## declare an array variable
declare -a arr=("SimpleTopo" "SingleLoopTopo" "ComplexTopo" "Test_1" "SimpleNegativeCycle" "cycle_in_the_middle" "fully_cyclic_triangle" "odd_length" "semi_cyclic_triangle" "simplified_complex_topo" "small_but_negative" "wheels_on_the_bus" "Test_2")

## now loop through the above array
for i in "${arr[@]}"
do
   
    python run_topo.py $i.txt $i.log >/dev/null
    python output_validator.py $i.log >/dev/null
    python check_output.py $i.log $PWD/logs/$i.log &> temp.txt 
    if grep -Fxq "Output matches!" temp.txt
    then
    echo "$i passed"
    else
    echo "$i failed"
    fi
done


