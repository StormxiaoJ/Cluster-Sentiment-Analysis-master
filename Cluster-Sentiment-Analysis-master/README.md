# User Guide
This is a user guide for Team35's Cloud Assignment 2
## Specification
To use this application to do the Deployment Automation, you need to do the following in advance:
1. You need to install Anisble on your PC properly with no dependency problem
2. You need to have a key pair and use key-agent to add in the key pair:
		// Suppose you have a key pair id_rsa and id_rsa.pub at /root/.ssh/
		sudo ssh-agent bash
		ssh-add /root/.ssh/id_rsa
## Functionality
* Launch instances in Nectar Cloud, create volumes and attach them to the instances
* Make file system and mount the volumes at /mnt/database/
* Install CouchDB and build a CouchDB cluster (Register as service so that it will start when system boots up and always restart when being shut down)
* Install Spark and build it as standalone mode (Master-slaves) (Register as service so that it will always restart when crashing down)
* Install Python 3.5 and clone our python code from GitHub and run the code
* Add new nodes to the existing cluster
## Usage
1. Unpack the package to a directory you like
2. Change the privilege of the directory which is called cloud recursely to let you have the right to run the sh file, you can simply do like this:
		chmod -R 777 could/
3. Simply use sh command to execute the play.sh file without to do any change:
		// Make sure you run this command inside the directory could/
		sh play.sh
4. Follow the instruction and do the things you want to do.
## Working Demo
Youtube: https://youtu.be/nlcv2GNyFpQ
