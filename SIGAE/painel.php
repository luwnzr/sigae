<?php
declare(strict_types=1);

if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

// Se o usuário tentar entrar aqui sem passar pelo login, expulsamos ele!
if (!isset($_SESSION['usuario_id'])) {
    header('Location: /SIGAE/login.php');
    exit;
}
?>
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SIGAE - Painel Principal</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>body { font-family: 'Inter', sans-serif; }</style>
</head>
<body class="bg-gray-100 min-h-screen flex flex-col">

    <!-- NAVBAR SUPERIOR -->
    <header class="bg-blue-900 text-white shadow-md">
        <div class="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
            <div class="flex items-center gap-3">
                <div class="w-8 h-8 bg-white rounded-tl-xl rounded-br-xl flex items-center justify-center shadow-sm">
                    <div class="w-2 h-2 bg-orange-500 rounded-full"></div>
                </div>
                <span class="text-2xl font-extrabold tracking-tight">SIGAE</span>
                <span class="text-xs bg-orange-500 text-white px-2 py-0.5 rounded-full font-semibold ml-2">Painel</span>
            </div>
            
            <div class="flex items-center gap-4">
                <div class="text-right hidden sm:block">
                    <p class="text-sm font-semibold"><?php echo htmlspecialchars($_SESSION['usuario_nome']); ?></p>
                    <p class="text-xs text-orange-300 uppercase tracking-wider"><?php echo htmlspecialchars($_SESSION['usuario_tipo']); ?></p>
                </div>
                <a href="controllers/LogoutController.php" class="bg-red-600 hover:bg-red-700 text-white text-sm font-semibold px-4 py-2 rounded-xl shadow transition">
                    Sair
                </a>
            </div>
        </div>
    </header>

    <!-- CONTEÚDO PRINCIPAL -->
    <main class="flex-grow max-w-7xl w-full mx-auto px-4 py-8">
        
        <!-- Boas-vindas -->
        <div class="mb-8">
            <h1 class="text-2xl font-bold text-gray-800">Visão Geral do Sistema</h1>
            <p class="text-gray-500 text-sm mt-1">Gerencie os ativos e o inventário corporativo de forma ágil.</p>
        </div>

        <!-- CARDS DE ESTATÍSTICAS (KPIs) -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div class="bg-white p-6 rounded-2xl shadow-sm border border-gray-200 border-l-4 border-l-blue-900">
                <p class="text-xs font-bold text-gray-400 uppercase tracking-wider">Total de Ativos</p>
                <h3 class="text-3xl font-extrabold text-blue-900 mt-2">0</h3>
                <p class="text-xs text-gray-500 mt-1">Cadastrados no sistema</p>
            </div>
            
            <div class="bg-white p-6 rounded-2xl shadow-sm border border-gray-200 border-l-4 border-l-orange-500">
                <p class="text-xs font-bold text-gray-400 uppercase tracking-wider">Empréstimos Ativos</p>
                <h3 class="text-3xl font-extrabold text-orange-500 mt-2">0</h3>
                <p class="text-xs text-gray-500 mt-1">Sob cautela no momento</p>
            </div>

            <div class="bg-white p-6 rounded-2xl shadow-sm border border-gray-200 border-l-4 border-l-green-600">
                <p class="text-xs font-bold text-gray-400 uppercase tracking-wider">Manutenções</p>
                <h3 class="text-3xl font-extrabold text-green-600 mt-2">0</h3>
                <p class="text-xs text-gray-500 mt-1">Itens em revisão</p>
            </div>
        </div>

        <!-- SEÇÃO DE AÇÕES RÁPIDAS -->
        <div class="bg-white rounded-2xl shadow-sm border border-gray-200 p-6">
            <h2 class="text-lg font-bold text-gray-800 mb-4">Ações Rápidas</h2>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                <button class="p-4 bg-gray-50 hover:bg-blue-50 border border-gray-200 hover:border-blue-900 rounded-xl text-left transition group">
                    <p class="font-bold text-blue-900 group-hover:text-blue-950">＋ Cadastrar Novo Ativo</p>
                    <p class="text-xs text-gray-500 mt-1">Adicionar equipamento ao inventário</p>
                </button>
                
                <button class="p-4 bg-gray-50 hover:bg-blue-50 border border-gray-200 hover:border-blue-900 rounded-xl text-left transition group">
                    <p class="font-bold text-blue-900 group-hover:text-blue-950">📋 Registrar Movimentação</p>
                    <p class="text-xs text-gray-500 mt-1">Empréstimos e devoluções</p>
                </button>

                <button class="p-4 bg-gray-50 hover:bg-blue-50 border border-gray-200 hover:border-blue-900 rounded-xl text-left transition group">
                    <p class="font-bold text-blue-900 group-hover:text-blue-950">👥 Gerenciar Usuários</p>
                    <p class="text-xs text-gray-500 mt-1">Alunos, professores e acessos</p>
                </button>
            </div>
        </div>

    </main>

    <!-- RODAPÉ -->
    <footer class="bg-white border-t border-gray-200 py-4 text-center text-xs text-gray-400">
        SIGAE - Sistema de Gestão de Ativos Educacionais &copy; 2026
    </footer>

</body>
</html>