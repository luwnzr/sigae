<?php session_start(); ?>
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SIGAE - Login</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
  <style>
    body { font-family: 'Inter', sans-serif; }
  </style>
</head>
<body class="bg-gray-100 min-h-screen flex items-center justify-center p-4">

  <div class="w-full max-w-sm bg-white rounded-2xl shadow-lg p-8 border-t-4 border-orange-500">

    <div class="flex flex-col items-center justify-center mb-8">
      <div class="flex items-center gap-3">
        <div class="w-8 h-8 bg-blue-900 rounded-tl-xl rounded-br-xl flex items-center justify-center shadow-sm">
          <div class="w-2 h-2 bg-orange-500 rounded-full"></div>
        </div>
        <h1 class="text-4xl font-extrabold text-blue-900 tracking-tight">SIGAE</h1>
      </div>
      <p class="text-[11px] text-gray-500 uppercase tracking-widest mt-2 font-semibold">Gestão de Ativos</p>
    </div>

    <!-- CAIXA DE MENSAGEM DE ERRO AQUI -->
    <?php
    if (isset($_SESSION['login_erro'])) {
        echo '<div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-xl mb-5 text-sm text-center font-semibold shadow-sm">';
        echo $_SESSION['login_erro'];
        echo '</div>';
        unset($_SESSION['login_erro']); 
    }
    ?>

    <!-- FORMULÁRIO -->
    <form action="controllers/LoginController.php" method="POST" class="space-y-5">
      <div>
        <input
          type="text"
          name="identificacao"
          required
          placeholder="CPF ou E-mail corporativo"
          class="w-full px-4 py-3 bg-gray-50 rounded-xl border border-gray-200 text-gray-800 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-900 focus:bg-white transition"
        >
      </div>

      <div>
        <input
          type="password"
          name="senha"
          required
          placeholder="Senha"
          class="w-full px-4 py-3 bg-gray-50 rounded-xl border border-gray-200 text-gray-800 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-900 focus:bg-white transition"
        >
      </div>

      <div class="flex justify-end">
        <a href="#" class="text-sm font-semibold text-blue-900 hover:text-orange-500 transition">Esqueci minha senha</a>
      </div>

      <button
        type="submit"
        class="w-full bg-blue-900 hover:bg-blue-950 text-white font-semibold py-3 rounded-xl shadow-md hover:shadow-lg transition-all duration-200"
      >
        Entrar no Sistema
      </button>
    </form>

  </div>

</body>
</html>