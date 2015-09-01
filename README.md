Catalog project	
==============

## Intro
This is a simple application to practice implementation of social auth and CRUD using the flask framework. 


## Requirements
All requirements are included in `vagrant/pg_config.sh`. 

## Installation

```
git clone https://github.com/craig-mulligan/udacity-project-3.git
```

```
cd vagrant
```

```
vagrant up
```

```
vagrant ssh
```

```
cd /vagrant/catalog
```

To see app structure
```
ls 
```

## Setup

There is already a DB file. `catalog.db` but if you wish to start from scratch delete this file and then run the application. Create an facebook application and add your credentials(app_id & app_secret) in `fb_client_secrets.json`.


## Running the application

```
python run.py
```

This will launch the server on localhost port 3000.

## Usage

You have to login with facebook. There are no other auth providers once in you can create items and categorize them. This app has 4 basic functions: adding, viewing, updating and deleting items. A new Category can only be added when adding an item, categories without any assocaited items are deleted. Only creators of the items can edit or delete and item. Also have to be logged in to add, edit or delete items. There are also 3 json endpoints to request, items, categories or users. 



## To shut down vagrant 

```
vagrant halt
```

Have fun!