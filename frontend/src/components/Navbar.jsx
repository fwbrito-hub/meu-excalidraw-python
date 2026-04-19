import React from 'react';

const Navbar = ({ user, currentProject, onSave, onSaveAs, onRename, onNewProject, onAnalyze, onLogout }) => {
  return (
    <nav className="navbar-container">
      <div className="glass floating-island">
        <div className="nav-brand">
          <div className="logo-box">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
            </svg>
          </div>
          <span className="brand-text">ExcaliSaaS <span className="badge">PRO</span></span>
        </div>

        {/* Informação do Projeto Atual Centralizada */}
        <div className="flex-1 flex justify-center min-w-[200px] px-4">
            {currentProject ? (
                <div className="flex items-center gap-2 bg-indigo-50/50 px-4 py-1.5 rounded-full border border-indigo-100">
                    <span className="text-sm font-semibold text-slate-700 max-w-[200px] truncate" title={currentProject.name}>
                        {currentProject.name}
                    </span>
                    <button onClick={onRename} className="p-1 hover:bg-white rounded-md transition-colors text-slate-400 hover:text-indigo-600" title="Renomear Projeto">
                        <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                        </svg>
                    </button>
                </div>
            ) : (
                <span className="text-sm font-medium text-slate-400 bg-slate-50/50 px-4 py-1.5 rounded-full border border-slate-100">
                    Quadro Temporário (Não Salvo)
                </span>
            )}
        </div>

        <div className="nav-actions">
          <button onClick={onNewProject} className="p-2 text-slate-500 hover:bg-slate-100 hover:text-slate-800 rounded-lg transition-colors" title="Novo Quadro em Branco">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4v16m8-8H4" />
            </svg>
          </button>
          
          <button onClick={onSave} className="btn-secondary" title="Salvar alterações">
            Salvar
          </button>
          
          <button onClick={onSaveAs} className="btn-secondary whitespace-nowrap" title="Criar uma cópia com novo nome">
            Salvar Como
          </button>

          <button onClick={onAnalyze} className="btn-primary">
            <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.381z" clipRule="evenodd" />
            </svg>
            Análise IA
          </button>
          
          <div className="divider" />
          
          <div className="user-profile">
            <div className="avatar">{user ? user[0].toUpperCase() : 'U'}</div>
            <div className="user-info">
              <span className="welcome">Olá,</span>
              <span className="username">{user || 'Usuário'}</span>
            </div>
            <button onClick={onLogout} title="Sair" className="logout-btn">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                 <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 16l4-4m0 0l-4-4m4 4H7" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
