SLAcompiler
===========

SLAcompiler is a "recompiler" designed to convert the original, shorthand GSLAUUA syntax to standard HTML syntax. This project is written by Arctic and Orangestar and is licensed under GPLv3.

##Examples:

The basic syntax is very similar to HTML. The following is valid GSLAUUA syntax:

    <div#contactoptions.wide.clearfix>

When run through SLAcompiler, this will result in the following:

    <div id="contactoptions" class="wide clearfix">

As long as classes are grouped together, you can put these CSS-styled attributes anywhere in your tags. It even supports default HTML attributes by leaving them alone. This is also proper GSLAUUA syntax:

    <div.wide.clearfix#contactoptions onclick="contactMe()">

<!-- /*This text kept for prosperity*/

This is a compiler for GSLAUUA written by myself and orangestar written in python

Its basic syntax is <tag.class#id>

Example: <div.box1#wide> is the same as <div id="box1" class="wide">


Licensed under GPLv3 -->
