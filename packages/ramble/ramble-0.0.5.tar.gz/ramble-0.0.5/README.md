## Running ramble

Ramble is a small program that enables you to control how consume/diffuse web, video content.
It can be used for digital signage and for increasing your own awareness and conciousness about t
the topics that to matter to you. It is currently compatible with linux and chromecast.

## Support ramble development

For the moment ramble at the proof-of-concept stage. If you like it, thanks to let us know. 
If you would like another feature we would be very interested in knowing it.

===

UNDER CONSTRUCTION -DOCS AND FEATURES ARE STILL IN ALPHA

===



This program has been tested under ubuntu linux with kde, but it should be easily generalisable to other environments.

## Test run wit docker

It is certainly better to install ramble directly on your system.
But if you want to give it a test without installing or removing any package, you can give our docker a sping

```
docker run --privileged --rm  --name ramble \
-e DISPLAY=:0 -v /tmp/.X11-unix/X0:/tmp/.X11-unix/X0 \
-e HOME=$HOME -v $HOME:$HOME:ro --entrypoint \
/bin/bash ramble -c 'ramble --play default 3'
```

```
docker run --privileged --rm  --name ramble \
 -e DISPLAY=:0 -v /tmp/.X11-unix/X0:/tmp/.X11-unix/X0  \
 --entrypoint /bin/bash \
ramble -c 'ramble --play ramble://https://raw.gitlab.com/default/  videos video'
```

### Writting your profile


```
playlist.yml:
  default:
  - url: ramble://news
    weigth: 3

```

## Core use cases 

#### Use case 1 : Create your own channel from youtube channel 1 and cast it on TV

```
CHROMECAST_DEVICE="Living Room TV" RAMBLE_WAKE_ON_LAN="70:54:b4:de:af:1a"   ramble --play kids_science chromecast
```

#### Use case 2 : See 3 videos from own 'science' channel on your screen 

```
ramble --play science video  3
```


#### Use case 3 : Show status monitors/alerts elements to monitor when you unlock screen

```
ramble --play-on-unlock status picture 2 
```


#### Use case 4 : Display sync content on all screensavers

```
# on server
ramble --play playlist nats

# on screens 
ramble --screensaver @nats 
# ramble --play @nats 
```

#### Use case 5 : Publish as channel for other to consume contents from
ramble --serve playlist


## Context dependent 

One of the important feature of ramble is to allow you to enable and prioritise content
based on information.

```
cat << EOF > '
#!/bin/bash

echo "{\"home-connected": $HOME_CONNECTED}"
'
```

We can go further by adding data coming from other systems, such as weather, trains, etc,
face recognition, etc...
