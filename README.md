gungnir
(why the fuck did we name it this, its the most awful thing in the world to type out)
==================================================================================================


Gungnir is an app to aid in the creation of ec2 instances and AMIs.

Deploying apps is the bane of the django community.  Computers are hard, let gungnir solve the issue for you. Just feed us a github repo and a spare cat.


Scaling apps is also hard. We can help with that some.  Most people using AWS don't bother with autoscale groups.
If you're not using autoscale groups and you get a lot of traffic you're gonna have a bad time.
The key to being able to start an autoscale group is having a shippable AMI.  We do that for you out of the box.

Some times the defaults aren't what you need, and thats ok. If you don't like our deploy choices (and I'm not sure I do), you can build your own deploy class.
Simply ensure that ensure it has a build() method that will do all the work.
To aid you in this journey, we've added some handy wrappers to make distributed deploys via fabric painless.
You can use our built in ubuntu/gunicorn instance builder or build your own by writing a builder class.



The Big Requirements
============
celery
boto
gitpython
python-mysql


Assumptions We Make about your git repo.
========================================

1.  You have a working requirements.txt
2.  You have a settings file in your app somewhere (you can pass this to your buildconfig with the python importable path name)
3.

Installing
==========
#.  Clone the app into a repo
#.  pip install -r requirements.txt
#.  Edit settings.py configure the DB to your liking
#.  Change AWS_SECRET_KEY and AWS_ACCESS_KEY in settings.py
#.  Change the BROKER_* variables to point to your RabbitMQ Server
#.  ./manage.py syncdb
#.  ./manage.py






Adding a new app
