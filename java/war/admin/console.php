<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<title>PHP Console</title>
</head>
<body>
<h1>PHP Console</h1>
<?php $script = $_POST['script'] ?>
<pre><?php if($script) eval($script); ?></pre>
<form action="" method="post">
<p><textarea rows="20" cols="80" name="script"><?php echo $script; ?></textarea></p>
<p><input type="submit" /></p>
</form>
</body>
</html>
