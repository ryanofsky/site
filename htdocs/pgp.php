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

<? 

function param(&$arg)
{
  if (!isset($arg)) $arg = false;
}

if (isset($HTTP_POST_VARS["text"]))
{

  flush();

  param($text);
  param($from);
  param($subject);
  
  $in = tempnam("M:/server/shares/temp","secret");
  $out = tempnam("M:/server/shares/temp","secret");
  
  $ip = $HTTP_SERVER_VARS["REMOTE_ADDR"];
  $dn = gethostbyaddr($ip);
  $us = $HTTP_SERVER_VARS["HTTP_USER_AGENT"];
  
  $fin = fopen($in,"wb");
  fwrite($fin, "IP Address = $ip\nHost = $dn\nHTTP_USER_AGENT = $us\n");
  fwrite($fin,$text);
  fclose($fin);
  
  unlink($out);
  passthru("gpg -q -a --batch --home M:/server/bin/php/gpg -o \"$out\" --encrypt --recipient 5FAA0216 \"$in\"");
  
  $fout = fopen($out,"r");
  $text = fread($fout,filesize($out));
  fclose($fout);

  $bsize = 1024;
  $passes = (int)ceil((double)filesize($in) / (double)$bsize);
  $nulls = str_repeat("\x00",$bsize);
  
  $fin = fopen($in, "wb");
  for($i = 0; $i < $passes; ++$i)
    fwrite($fin,$nulls);
  fclose($fin);

  unlink($in);
  unlink($out);
  
  mail("rey4@columbia.edu",$subject,$text, "To: Russell Yanofsky <rey4@columbia.edu>\nFrom: $from\nX-Mailer: PHP/" . phpversion());
  
  print("<h3>Message Sent</h3><pre><b>From:    $from\nSubject: $subject</b>\n\n$text</pre>");

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
Version: GnuPG v1.0.6 (MingW32)
Comment: For info see http://www.gnupg.org

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
=D+Gl
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
form. Since I haven't set up a proper CA, it doesn't provide authentication, but 
it does provide end-to-end encryption. The message entered here will be
encrypted with my public key and delivered to my email address. The From: and
Subject: fields are optional and are sent as plaintext.</p>

<?
  if ($HTTP_SERVER_VARS["HTTPS"] != "on")
    print '<h3><a href="https://russ.hn.org/pgp.php" style="text-decoration:none"><font color=red>Click here to connect to a secure web server</font></a></h3>';
?>

<form method=post action="<?= $HTTP_SERVER_VARS["HTTPS"] != "on" ? "https://russ.hn.org/pgp.php" : "pgp.php"?>">
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

<? } ?>

</body>
</html>