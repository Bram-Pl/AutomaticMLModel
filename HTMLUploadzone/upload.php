<?php
$target_dir = "uploads/";
$target_file = $target_dir . basename($_FILES["fileToUpload"]["name"]);
$uploadOk = 1;
$imageFileType = strtolower(pathinfo($target_file,PATHINFO_EXTENSION));

if (!file_exists('uploads/')) {
    mkdir('uploads/', 0777, true);
}

// Check file size
if ($_FILES["fileToUpload"]["size"] > 500000) {
    echo "Sorry, your file is too large.";
    $uploadOk = 0;
}
// Allow certain file formats
if($imageFileType != "csv" && $imageFileType != "Csv" && $imageFileType != "cSv"
&& $imageFileType != "csV" && $imageFileType != "CSv" && $imageFileType != "cSV"
&& $imageFileType != "CsV" && $imageFileType != "CSV") {
    echo "Sorry, only CSV files are allowed.";
    $uploadOk = 0;
}
// Check if $uploadOk is set to 0 by an error
if ($uploadOk == 0) {
    echo "Sorry, your file was not uploaded.";
// if everything is ok, try to upload file
} else {
    if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file)) {
        echo "The file ". basename( $_FILES["fileToUpload"]["name"]). " has been uploaded and is ready to be processed.";
    } else {
        echo "Sorry, there was an error uploading your file.";
    }
}
?>