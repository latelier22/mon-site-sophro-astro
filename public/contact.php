<?php
if ($_SERVER["REQUEST_METHOD"] !== "POST") {
    http_response_code(405);
    exit("Méthode non autorisée");
}

function clean($value) {
    return trim(strip_tags($value ?? ""));
}

$nom = clean($_POST["nom"] ?? "");
$emailRaw = trim($_POST["email"] ?? "");
$email = filter_var($emailRaw, FILTER_VALIDATE_EMAIL);
$telephone = clean($_POST["telephone"] ?? "");
$message = trim($_POST["message"] ?? "");

if (!$nom || !$email || !$message) {
    header("Location: /contact?error=1");
    exit;
}

$to = "contact@alexandracoirier-sophrologue.fr";
$subject = "Nouveau message depuis le site Alexandra Coirier";

$contenu = "Nouveau message depuis le formulaire du site\n\n";
$contenu .= "Nom : " . $nom . "\n";
$contenu .= "Email : " . $email . "\n";
$contenu .= "Téléphone : " . $telephone . "\n\n";
$contenu .= "Message :\n" . $message . "\n";

$headers = [];
$headers[] = "From: Alexandra Coirier Site <no-reply@alexandracoirier-sophrologue.fr>";
$headers[] = "Reply-To: " . $email;
$headers[] = "MIME-Version: 1.0";
$headers[] = "Content-Type: text/plain; charset=UTF-8";

$success = mail($to, $subject, $contenu, implode("\r\n", $headers));

if ($success) {
    header("Location: /contact?success=1");
    exit;
} else {
    header("Location: /contact?error=1");
    exit;
}