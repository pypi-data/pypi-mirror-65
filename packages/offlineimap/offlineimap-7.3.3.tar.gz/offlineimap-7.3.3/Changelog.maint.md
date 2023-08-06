---
layout: page
title: Changelog of the stable branch
---

* The following excerpt is only usefull when rendered in the website.
{:toc}

This is the Changelog of the maintenance branch.

**NOTE FROM THE MAINTAINER:**

	This branch comes almost as-is. With no URGENT requirements to update this
	branch (e.g. big security fix), it is left behind.
	If anyone volunteers to maintain it and backport patches, let us know!


### OfflineIMAP v6.7.0.3 (2016-07-26)

#### Bug Fixes

* sqlite: properly serialize operations on the database files


### OfflineIMAP v6.7.0.2 (2016-07-22)

#### Bug Fixes

* sqlite: close the database when no more threads need connection.


### OfflineIMAP v6.7.0.1 (2016-06-08)

#### Bug Fixes

* Correctly open and close sqlite databases.


### OfflineIMAP v6.3.2.1 (2011-03-23)

#### Bug Fixes

* Sanity checks for SSL cacertfile configuration.
* Fix regression (UIBase is no more).
* Make profiling mode really enforce single-threading.
