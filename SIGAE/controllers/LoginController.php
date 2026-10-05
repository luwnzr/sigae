<?php
declare(strict_types=1);

if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

require_once __DIR__ . '/../config/database.php';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header('Location: /SIGAE/login.php');
    exit;
}

$identificacao = trim($_POST['identificacao'] ?? '');
$senha         = trim($_POST['senha'] ?? '');

if ($identificacao === '' || $senha === '') {
    redirecionarComErro('Preencha todos os campos.');
}

// Identifica se é E-mail, o login especial "adm" ou um CPF
if (filter_var($identificacao, FILTER_VALIDATE_EMAIL)) {
    $tipoIdentificacao = 'email';
} elseif ($identificacao === 'adm') {
    $tipoIdentificacao = 'adm';
} else {
    $tipoIdentificacao = 'cpf';
    $identificacao = preg_replace('/[^0-9]/', '', $identificacao);

    if (strlen($identificacao) !== 11) {
        redirecionarComErro('CPF inválido.');
    }
}

try {
    /** @var PDO $pdo */
    $pdo = getConnection();

    // Define a query com base no tipo de identificação
    if ($tipoIdentificacao === 'email') {
        $sql = 'SELECT id, nome, senha, tipo_usuario FROM usuarios WHERE email = :identificacao LIMIT 1';
    } elseif ($tipoIdentificacao === 'adm') {
        $sql = 'SELECT id, nome, senha, tipo_usuario FROM usuarios WHERE cpf = :identificacao OR email = :identificacao LIMIT 1';
    } else {
        $sql = 'SELECT id, nome, senha, tipo_usuario FROM usuarios WHERE cpf = :identificacao LIMIT 1';
    }

    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':identificacao', $identificacao, PDO::PARAM_STR);
    $stmt->execute();

    $usuario = $stmt->fetch(PDO::FETCH_ASSOC);

} catch (PDOException $e) {
    error_log('Erro no LoginController: ' . $e->getMessage());
    redirecionarComErro('Erro interno. Tente novamente mais tarde.');
}

if (!$usuario) {
    redirecionarComError('Usuário não encontrado.');
}

if (!password_verify($senha, $usuario['senha'])) {
    redirecionarComError('Senha incorreta.');
}

session_regenerate_id(true);

$_SESSION['usuario_id']   = $usuario['id'];
$_SESSION['usuario_nome'] = $usuario['nome'];
$_SESSION['usuario_tipo'] = $usuario['tipo_usuario'];
$_SESSION['logado_em']    = time();

header('Location: /SIGAE/painel.php');
exit;

function redirecionarComErro(string $mensagem): void
{
    $_SESSION['login_erro'] = $mensagem;
    header('Location: /SIGAE/login.php');
    exit;
}