gungnir
==================================================================================================
*(why the fuck did we name it this, its the most awful thing in the world to type out)*


Gungnir is an app to aid in the creation of ec2 instances and AMIs.

Deploying apps is the bane of the django community.  Computers are hard, let gungnir solve the issue for you. Just feed us a github repo and a spare cat.


Scaling apps is also hard. We can help with that.  Most people using AWS don't bother with autoscale groups.
__If you're not using autoscale groups and you get a lot of traffic you're gonna have a bad time.__
The key to being able to start an autoscale group is having a shippable AMI.  We do that for you out of the box.

Some times the defaults aren't what you need, and thats ok. If you don't like our deploy choices (and I'm not sure I do), you can build your own deploy class.
Simply ensure that ensure it has a build() method that will do all the work.
To aid you in this journey, we've added some handy wrappers to make distributed deploys via fabric painless.
You can use our built in ubuntu/gunicorn instance builder or build your own by writing a builder class.



The Big Requirements
============
* django
* lots of django stuff
* celery
* boto
* gitpython
* python-mysql


Assumptions We Make about your git repo.
========================================
1. You have a working requirements.txt
1. You have a settings file in your app somewhere (you can pass this to your buildconfig with the python importable path name)
1. more than this, but you get what you get with 48 hours of de time.

Installing
==========
2.  Clone the app into a repo
2.  pip install -r requirements.txt
2.  Edit settings.py configure the DB to your liking
2.  Change AWS_SECRET_KEY and AWS_ACCESS_KEY in settings.py
2.  Change the BROKER_* variables to point to your RabbitMQ Server
2.  ./manage.py syncdb
2.  ./manage.py


Using Gungnir
===========
3. register an account (only valid accounts can build, we have provided the testers with one)
3. login
3. add an application
3. add your repo: git://github.com/jawnb/badatcomputers.git
3. add a build config, for aws keypair use 'djangodash'
3. create your build!

lol
