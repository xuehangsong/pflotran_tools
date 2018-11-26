for itime in $(seq 219 365)
do
    echo $itime
    convert -density 120 /pic/dtn/shua784/John_case_optim_5/tracer/tracer.$(printf "%04d" $itime).png -background white -flatten  /pic/dtn/shua784/John_case_optim_5/tracer_small/$itime.jpg
done

convert -delay 10 -quality 100 /pic/dtn/shua784/John_case_optim_5/tracer_small/*.jpg  /pic/dtn/shua784/John_case_optim_5/tracer.gif



#  for itime in $(seq 100 120)
# for itime in $(seq 219 365)	     
# do
#     echo $itime
#     convert -density 120 /pic/dtn/shua784/John_case_optim_5/vec/vec.$(printf "%04d" $itime).png   /pic/dtn/shua784/John_case_optim_5/vec_small/$itime.png
# done



