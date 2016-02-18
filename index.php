<pre>
<?php
$command = "python observe.py";
$command = escapeshellcmd($command);
$output = shell_exec($command);
$output = htmlspecialchars($output);
echo "\n$output";
?>
</pre>

