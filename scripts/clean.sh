sudo find . -name '*__pycache__' 2> /dev/null | awk '{print "sudo rm -rf " $1}' | sh
