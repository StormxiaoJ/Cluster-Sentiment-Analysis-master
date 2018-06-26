#Cluster Sentiment Analysis Project, CCC2018-35, Melbourne
#Members: Yan Jiang 816920, Yijiang Liu 848008, Zihua Liu 857673, Zhenxiang Wang 879694, Lingtao Jiang 867583

echo "How many instances do you want to launch? (>1)"
read param1

if [ 2 -le $param1 ]
then
	param1=`expr $param1 - 1`;
	echo "==========================="
	echo "Please set the volume attached to the instances (Integer)"
	read param2
	echo "==========================="
	echo "Please enter the name of your key:"
	read keypair
	echo "==========================="
	echo "Please set the cookie (password used for communication between servers):"
	read param3
	echo "==========================="
	echo "Please set the username of the administer of CouchDB:"
	read param4
	echo "==========================="
	echo "Please set the password of the administer of CouchDB:"
	read param5
	sudo ansible-playbook buildcluster.yaml --extra-vars "num=${param1} volume=${param2} key=${keypair} cookie=${param3} username=${param4} password=${param5}"
	echo "==========================="
        echo "All tasks have been finished!"
        echo "Have a nice day! Goodbye!"
        echo "==========================="
else
	echo "==========================="
	echo "Please launch more than 1 instance."
	echo "Have a nice day! Goodbye!"
	echo "==========================="
fi


echo ""
echo ""
echo "--      --      --  --------  --         -------   ------   --      --  --------"
echo " --    ----    --   --        --        --        --    --  ---    ---  --"
echo "  --  --  --  --    ------    --        --        --    --  ----  ----  ------"
echo "   ----    ----     --        --        --        --    --  -- ---- --  --"
echo "    --      --      --------  --------   -------   ------   --  --  --  --------"
echo ""
echo "==========================="
echo "What do you want to do?"
echo "---------------------------"
echo "Press 1: Build a cluster"
echo "Press 2: Add new hosts"
echo "==========================="
echo ""
read param
if [ 1 -eq $param ]
then
	echo "==========================="
	echo "You have chosen 1:"
	echo "Begin to build a cluster..."
	echo "==========================="
	sh buildcluster.sh
elif [ 2 -eq $param ]
then
	echo "==========================="
	echo "You have chosen 2:"
	echo "Begin to add new hosts..."
	echo "==========================="
	sh addhost.sh
else
	echo "==========================="
	echo "Please Enter 1 or 2!"
	echo "Have a nice day! GoodBye!"
	echo "==========================="
fi
