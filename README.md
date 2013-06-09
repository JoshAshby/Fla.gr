## fla.gr - ALL THE BOOKMARKS
  
A bit of introduction:
---------------------
fla.gr grew out of my increasing hate for the interface on delicious and a need
to always have bookmarks accessible from just about anywhere. I also was looking
for a basic scratchpad, with some formating options, preferably markdown
enabled. As a result of having just started working with gevent and having
built my Seshat framework, I figured this was the perfect time to go about
making a new bookmarking service that was what I wanted. And so, with many
co rewrites, many revisions and lots of refactoring, I've been slowly
building fla.gr from the ground up.  
Early versions of fla.gr grew from Seshat, and were powered by a funky, worth
nothing UI framework that was meant to be a bridge between Twitter's Bootstrap
styled HTML, and Python. I didn't want to go the route of using something like
Cheetah or serving a single page app and then making fla.gr an API, and it
resulted in a lot of head banging, and pain. In the end, I've gone for Cheetah
to render all the templates, and have stuck to writing just plan Python and
HTML as mostly separate systems.  
  
What you need:
---------------
A web server, I personally use Lighttpd, fastCGI and support to use it with
the webserver, ZeroMQ, Redis, CouchDB, Python 2.7, node.js, and all the
node packages and the python packages. The simplest way to get the python
and node.js packages and generate the templates is to do:  
  
  npm install  
  mkvirtualenv flagr  
  pip install -r requirements.txt  
  make flagr  
  
After this you'll have to setup your static folder so the content in `interface/resources/` 
is available at `/static` on your web server, along with fastCGI setup to send
all results to the server, except for `/static` to `localhost:8080` or whatever port
you specify in `config.json` and finally:
  
  cd flagr_core
  ./firstTime.py
  ./app.py noDaemon
  
To test fla.gr out (you might have to `chmod +x`)  
  
It's recommend by Me to run fla.gr in a Python virtualenv just to be safe
and to make sure everything runs smoothly even if you have a more up to date
system than I do.  
  
If you have problems with fla.gr not starting due to a `NULL result without error in PyObject_Call`
this is a known problem with GCC4.8, so please try:  
  
  pip uninstall greenlets
  CFLAGS="-O0" pip install greenlet==0.4.0
  
I won't be of much help if the problem persists, as it is, at the moment, a
Greenlets problem. I will only help out if this is something that is
directly related to code that I wrote in fla.gr. Aka: Send bug reports and
crash dumps to the appropriate project.
