<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<meta content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no" name="viewport">
	<title>Simple Lightbox - Responsive touch friendly Image lightbox</title>
	<link href='http://fonts.googleapis.com/css?family=Slabo+27px' rel='stylesheet' type='text/css'>
	<link href='/dist/simplelightbox.min.css' rel='stylesheet' type='text/css'>
	<link href='demo.css' rel='stylesheet' type='text/css'>
</head>
<body>
	<div class="container">
		<h1 class="align-center">Bildergalerie yourphotobooth.de</h1>
		<div class="gallery">
			
<?php
// Ordnername 
$ordner = "images"; //auch komplette Pfade möglich ($ordner = "download/files";)
 
// Ordner auslesen und Array in Variable speichern
$alledateien = scandir($ordner); // Sortierung A-Z
// Sortierung Z-A mit scandir($ordner, 1)               
 
// Schleife um Array "$alledateien" aus scandir Funktion auszugeben
// Einzeldateien werden dabei in der Variabel $datei abgelegt
foreach ($alledateien as $datei) {
 
 // Zusammentragen der Dateiinfo
 $dateiinfo = pathinfo($ordner."/".$datei); 
 //Folgende Variablen stehen nach pathinfo zur Verfügung
 // $dateiinfo['filename'] =Dateiname ohne Dateiendung  *erst mit PHP 5.2
 // $dateiinfo['dirname'] = Verzeichnisname
 // $dateiinfo['extension'] = Dateityp -/endung
 // $dateiinfo['basename'] = voller Dateiname mit Dateiendung
 

 // scandir liest alle Dateien im Ordner aus, zusätzlich noch "." , ".." als Ordner
 // Nur echte Dateien anzeigen lassen und keine "Punkt" Ordner
 // _notes ist eine Ergänzung für Dreamweaver Nutzer, denn DW legt zur besseren Synchronisation diese Datei in den Orndern ab
 if ($datei != "." && $datei != ".."  && $datei != "_notes") { 
 ?>
<a href="<?php echo $dateiinfo['dirname']."/".$dateiinfo['basename'];?>">
<img src=<?php echo "thumbs/".$dateiinfo['basename'];?>></a>
<?php
 };
 };
?>

		</div>
		<br><br>

	</div>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js"></script>
<script type="text/javascript" src="../dist/simple-lightbox.js"></script>
<script>
	$(function(){
		var $gallery = $('.gallery a').simpleLightbox();

		$gallery.on('show.simplelightbox', function(){
			console.log('Requested for showing');
		})
		.on('shown.simplelightbox', function(){
			console.log('Shown');
		})
		.on('close.simplelightbox', function(){
			console.log('Requested for closing');
		})
		.on('closed.simplelightbox', function(){
			console.log('Closed');
		})
		.on('change.simplelightbox', function(){
			console.log('Requested for change');
		})
		.on('next.simplelightbox', function(){
			console.log('Requested for next');
		})
		.on('prev.simplelightbox', function(){
			console.log('Requested for prev');
		})
		.on('nextImageLoaded.simplelightbox', function(){
			console.log('Next image loaded');
		})
		.on('prevImageLoaded.simplelightbox', function(){
			console.log('Prev image loaded');
		})
		.on('changed.simplelightbox', function(){
			console.log('Image changed');
		})
		.on('nextDone.simplelightbox', function(){
			console.log('Image changed to next');
		})
		.on('prevDone.simplelightbox', function(){
			console.log('Image changed to prev');
		})
		.on('error.simplelightbox', function(e){
			console.log('No image found, go to the next/prev');
			console.log(e);
		});
	});
</script>
</body>
</html>
