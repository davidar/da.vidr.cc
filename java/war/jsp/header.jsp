<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
    <head>
        <meta http-equiv="Content-Type" content="text/html;charset=UTF-8" />
        <title><%= request.getParameter("title") %></title>
        <link rel="stylesheet" href="http://static.da.vidr.cc/css/blueprint/screen.css" type="text/css" media="screen, projection" />
        <link rel="stylesheet" href="http://static.da.vidr.cc/css/blueprint/print.css" type="text/css" media="print" />    
        <!--[if lt IE 8]><link rel="stylesheet" href="http://static.da.vidr.cc/css/blueprint/ie.css" type="text/css" media="screen, projection" /><![endif]-->
    </head>
    <body>
        <div class="container">
            <h1><%= request.getParameter("title") %></h1>
