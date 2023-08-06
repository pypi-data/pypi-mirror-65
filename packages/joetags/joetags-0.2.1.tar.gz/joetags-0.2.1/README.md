# Joetags

**DECREASES file tree complexity**  
**INCREASES your Productivity**  

Joetags is a cli app to organize projects in a meaningful way for humans and machines
You can Tag all your projects/directories to easily find them inside huge parent directories.  
A branch of a branch of a branch of a branch is history.  

Projects are Complex and not Black and White, they can be written in a particular language, be artistic at the same time, and made for a specific client. They can be about biology while being about chemics. The world is sometimes more complex than it seems. But Directory Trees force us to classify projects with just one property.

However with joetags you can add as many tags to directories as you want and easily find stuff. 
Aditionally labeled projects/directories can be made more accessible to automated processes.

# Installing

Install and update using pip:
```
pip install joetags
```

## How Joetags improves Working

Before using Joetags you may have a file tree like this:

* User/projects/py  
* User/projects/py/ml
* User/projects/py/bots
* User/projects/py/art
* User/projects/go  
* User/projects/go/hardware
* User/projects/php  

after  

* User/projects  

where all your projects are live!
Simply search py for all py tagged projects or search py|php to get all py or php tagged projects

## How to search for directories

```
joetags search 'expr'
```

expressions can have unions:| intersections:& and can be negated:!

### Examples
- **python|(php&machine_learning)**: finds all python projects or php machine learning_projects
- **python&!utility**: all python projects not tagged with utility
finds

## How to Write .joetag File
Tags can use all letters, numbers and underscores and have to begin with a letter
Tagnames can be followed by a Groupname (same syntax) seperated by :

**tag:group**  

```
python:programming  
hobby  
michael_deangelo:client  
```

Just type **joetags add** followed by a directory to easily add tags


## Why are tags and groups handled the same in search

```
joetag search 'socialmedia'
```
does not care if socialmedia is a tag or a group, why is that?  

groups may be tags for other groups:
if socialmedia is a group in one place it could be a tag in another place  

`socialmedia:social`

however it mustn't only have one 'parent' group  

`socialmedia:social`
`socialmedia:internet`

can both coexist in joetags

While the same could be achived with less characters and no duplicates we root for easy usage and syntax
