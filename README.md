SLAcompiler
===========

SLAcompiler is a "recompiler" designed to convert the original, shorthand GSLAUUA syntax to standard HTML syntax. This project is written by Arctic and Orangestar and is licensed under GPLv3.

##Examples:

The basic syntax is very similar to HTML. The following is valid GSLAUUA syntax:

    &lt;div#contactoptions.wide.clearfix&gt;

When run through SLAcompiler, this will result in the following:

    &lt;div id="contactoptions" class="wide clearfix"&gt;

As long as classes are grouped together, you can put these CSS-styled attributes anywhere in your tags. It even supports default HTML attributes by leaving them alone. This is also proper GSLAUUA syntax:

    &lt;div.wide.clearfix#contactoptions onclick="contactMe()"&gt;

For a good example of a page, throw the following into a file and compile it. If all went well, the text should be blue.

    &lt;!DOCTYPE html&gt;
    &lt;html&gt;
      &lt;meta charset="utf-8"&gt;
      &lt;title&gt;Blue text!&lt;/title&gt;
      &lt;style&gt;
        #blue {
          color: blue;
        }
      &lt;/style&gt;
    &lt;head&gt;
    &lt;/head&gt;
    &lt;body#blue&gt;
      &lt;p#blue&gt;This text is blue!&lt;/p&gt;
      &lt;p&gt;This text is not!&lt;/p&gt;
    &lt;/body&gt;
    &lt;/html&gt;

<!-- /*This text kept for prosperity*/

This is a compiler for GSLAUUA written by myself and orangestar written in python

Its basic syntax is <tag.class#id>

Example: <div.box1#wide> is the same as <div id="box1" class="wide">


Licensed under GPLv3 -->
