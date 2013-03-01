fla.gr - ALL THE BOOKMARKS
##########################

A bit of introduction:
---------------------
fla.gr grew out of my increasing hate for the interface on delicious and a need
to always have bookmarks acessible from just about anywhere. I also was looking
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
HTML as seperate systems.

What you need:
---------------
Well, currently nothing, because I'm rewriting this and it doesn't work. At
all.

However, you probably will eventually need ZeroMQ, Redis, CouchDB, Python
2.7, node.js, and all the node packages and the python packages. Simplest way
to get these is to do:

  npm install
  mkvirtualenv flagr
  pip install -r requirements.txt
  make flagr

It's recommened by Me to run fla.gr in a Python virtualenv just to be safe
and to make sure everything runs smoothly even if you have a more up to date
system than I do.

Besides that, everything else I'll eventually get around to writing about in
here, sostay tuned!
