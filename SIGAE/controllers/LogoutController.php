<?php
declare(strict_types=1);

// Inicia a sessão para poder destruí-la
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

// Limpa todas as variáveis da sessão
$_SESSION = [];

// Destrói a sessão no servidor
session_destroy();

// Redireciona de volta para a tela de login correta com o caminho do SIGAE
header('Location: /SIGAE/login.php');
exit;