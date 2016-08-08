<html>
<head>
<title>PGP Page</title>

<style type="text/css">
<!--

body
{ 
  font-family: Trebuchet MS, Arial, Helvetica, sans-serif;
  font-style: normal;
  font-weight: normal;
}

-->
</style>
</head>

<body bgcolor="#19334C" text="#FFFFFF" link="#FFFFFF" vlink="#FFFFFF" alink="#FFFFFF">

<?php

if (isset($_POST["text"]))
{
  flush();

  $text = $_POST["text"];
  $from = $_POST["from"];
  $subject = $_POST["subject"];

  $out = tempnam("", "");
  unlink($out);
  
  $ip = $_SERVER["REMOTE_ADDR"];
  $dn = gethostbyaddr($ip);
  $us = $_SERVER["HTTP_USER_AGENT"];

  $cmd = "gpg -q -a --batch --home /var/lib/russ/gpg -o " . escapeshellarg($out) . " --encrypt --recipient 164650CC > /tmp/err 2>&1";
  $fin = popen("$cmd", "w");
  fwrite($fin, "Subject = $subject\nFrom = $from\n");
  fwrite($fin, "IP Address = $ip\nHost = $dn\nHTTP_USER_AGENT = $us\n");
  fwrite($fin,$text);
  fclose($fin);
  
  $fout = fopen($out,"r");
  $ctext = fread($fout,filesize($out));
  fclose($fout);
  unlink($out);
  
  mail("russ+gpgpgp@yanofsky.org", "gpg.php mail", $ctext, "X-Mailer: PHP/" . phpversion(), "-f russ+gpgphp@yanofsky.org");
  
  print("<h3>Message Sent</h3><pre><b>From:    " . htmlspecialchars($from) . "\nSubject: " . htmlspecialchars($subject) . "</b>\n\n" . htmlspecialchars($text) . "</pre>");

} else {

?>

<p><small>PGP (Pretty Good Privacy) is a 
<a href="http://www.pcwebopedia.com/TERM/p/public_key_cryptography.html">public key</a>
cryptosystem that (among other things) allows you to send and recieve encrypted and digitally signed emails.
Two free, popular software packages that support it are 
<a href="http://www.pgp.com/products/freeware/">PGP Freeware</a> and the <a href="http://www.gnupg.org">GNU Privacy Guard</a>.
</small>
</p>

<p>My PGP key is:</p>

<form>
<textarea id="key" rows=10 cols=65 READONLY>
-----BEGIN PGP PUBLIC KEY BLOCK-----

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
/Fnpkj6YM0jLJ11p8OM=
=zZhM
-----END PGP PUBLIC KEY BLOCK-----
</textarea><br>
<script>
<!--

var key;
if (document.all && (key = document.all.key) && key.createTextRange)
{
  document.write('<small><a href="javascript:void(key.createTextRange().execCommand(\'Copy\'));" style="text-decoration:none">Copy to clipboard</a></small>');
}

// -->
</script>
</form>

<hr>

<p>If you haven't got PGP installed you can send me secure mail through this web 
form. The message entered here will be
encrypted with my public key and delivered to my email address.</p>

<?php
  if (!isset($_SERVER["HTTPS"]) || $_SERVER["HTTPS"] != "on")
    print '<h3><a href="https://russ.yanofsky.org/pgp.php" style="text-decoration:none"><font color=red>Click here to connect to a secure web server</font></a></h3>';
?>

<form method=post<?= !isset($_SERVER["HTTPS"]) || $_SERVER["HTTPS"] != "on" ? ' action="https://russ.yanofsky.org/pgp.php"' : ''?>>
<table>
<tr>
  <td><label for=from>From:</label></td>
  <td><input type=text name=from id=from size=40></td>
</tr>
<tr>
  <td><label for=subject>Subject:</label></td>
  <td><input type=text name=subject id=subject size=40></td>
</tr>
<tr>
  <td valign=top><label for=text>Text:</label></td>
  <td><textarea name=text id=text wrap=virtual rows=15 cols=76></textarea></td>
</tr>
<tr>
  <td>&nbsp;</td>
  <td><input type=submit name=submit value=Send></td>
</tr>  
</table>
</form>

<?php } ?>

</body>
</html>
