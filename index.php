<h1>Pomme Bots</h1>
<pre>
<?php
$command = "python observe.py --stat True";
$command = escapeshellcmd($command);
$output = shell_exec($command);
$output = htmlspecialchars($output);
echo "\n$output";
?>
</pre>

