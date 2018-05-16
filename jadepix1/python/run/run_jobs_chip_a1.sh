for file in ./python/run/jobs_chip_a1/*
do
if [ -f "$file" ]
then
    echo "$file is submitted!"
    #hep_sub -g physics $file
fi
done