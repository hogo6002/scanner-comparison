
type=$1   #docker or project
ecosystem=$2

python3 ./compare.py $type $ecosystem     # docker scout JSON result may be invalid, remove the last few lines