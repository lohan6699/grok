<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Cadastro de Clientes</title>
  
  <style>
    * { margin:0; padding:0; box-sizing:border-box; }
    body {
      font-family: system-ui, -apple-system, sans-serif;
      background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
      min-height: 100vh;
      padding: 20px;
      color: #1f2937;
    }
    .container {
      background: white;
      width: 100%;
      max-width: 600px;
      margin: 0 auto;
      border-radius: 16px;
      box-shadow: 0 10px 40px rgba(0,0,0,0.18);
      overflow: hidden;
    }
    .tabs {
      display: flex;
      background: #f3f4f6;
      border-bottom: 1px solid #e5e7eb;
    }
    .tab {
      flex: 1;
      padding: 16px;
      text-align: center;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.2s;
      color: #4b5563;
    }
    .tab.active {
      background: white;
      color: #4f46e5;
      border-bottom: 3px solid #4f46e5;
    }
    .tab-content {
      padding: 28px;
      min-height: 420px;
    }
    .tab-content.hidden { display: none; }

    /* Form styles */
    .form-group { margin-bottom: 24px; }
    label { display: block; margin-bottom: 8px; font-weight: 500; font-size: 0.95rem; color: #374151; }
    input, select {
      width: 100%; padding: 14px 16px; border: 1px solid #d1d5db; border-radius: 10px;
      font-size: 1rem; transition: all 0.2s;
    }
    input:focus, select:focus {
      outline: none; border-color: #6366f1; box-shadow: 0 0 0 4px rgba(99,102,241,0.12);
    }
    .error { color: #dc2626; font-size: 0.84rem; margin-top: 6px; min-height: 1.2em; }
    button {
      width: 100%; padding: 16px; background: #4f46e5; color: white; border: none;
      border-radius: 10px; font-size: 1.1rem; font-weight: 600; cursor: pointer; margin-top: 16px;
      transition: all 0.25s;
    }
    button:hover:not(:disabled) { background: #4338ca; transform: translateY(-2px); }
    button:disabled { background: #9ca3af; cursor: not-allowed; }

    .success-msg, .error-msg {
      padding: 16px; margin: 20px 0; border-radius: 10px; text-align: center; font-weight: 500;
    }
    .success-msg { background: #ecfdf5; color: #065f46; border: 1px solid #a7f3d0; }
    .error-msg   { background: #fef2f2; color: #991b1b; border: 1px solid #fecaca; }

    .row { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
    @media (max-width: 520px) { .row { grid-template-columns: 1fr; gap: 24px; } }

    /* Lista de clientes */
    .client-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
    .client-list { display: flex; flex-direction: column; gap: 16px; }
    .client-card {
      background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 12px;
      padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);
      position: relative;
    }
    .client-card h3 { margin: 0 0 12px; color: #1f2937; font-size: 1.15rem; }
    .client-info { font-size: 0.95rem; color: #4b5563; line-height: 1.6; }
    .client-info strong { color: #374151; }
    .delete-btn {
      position: absolute; top: 16px; right: 16px;
      background: #ef4444; color: white; border: none;
      border-radius: 6px; padding: 6px 12px; font-size: 0.85rem;
      cursor: pointer; transition: background 0.2s;
    }
    .delete-btn:hover { background: #dc2626; }
    .no-clients { text-align: center; color: #6b7280; padding: 80px 20px; font-size: 1.1rem; }
  </style>
</head>
<body>

  <div class="container">
    <div class="tabs">
      <div class="tab active" data-tab="cadastro">Novo Cadastro</div>
      <div class="tab" data-tab="lista">Clientes Cadastrados</div>
    </div>

    <div class="tab-content" id="cadastro">
      <form id="cadastro-form" novalidate>
        <!-- Campos do formulário (mantidos iguais à versão anterior) -->
        <div class="form-group">
          <label for="nome">Nome completo *</label>
          <input type="text" id="nome" required minlength="3" placeholder="Ex: João Silva Santos">
          <span class="error" id="erro-nome"></span>
        </div>

        <div class="row">
          <div class="form-group">
            <label for="cpf">CPF *</label>
            <input type="text" id="cpf" required placeholder="000.000.000-00" maxlength="14" inputmode="numeric">
            <span class="error" id="erro-cpf"></span>
          </div>
          <div class="form-group">
            <label for="nascimento">Data de nascimento *</label>
            <input type="date" id="nascimento" required>
            <span class="error" id="erro-nascimento"></span>
          </div>
        </div>

        <div class="form-group">
          <label for="email">E-mail *</label>
          <input type="email" id="email" required placeholder="seuemail@exemplo.com">
          <span class="error" id="erro-email"></span>
        </div>

        <div class="row">
          <div class="