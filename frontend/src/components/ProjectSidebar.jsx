import React, { useState, useEffect } from 'react';
import api from '../api';

const ProjectSidebar = ({ onSelectProject, onDeleteProject, refreshTrigger, isOpen, setIsOpen }) => {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(false);

  // Buscar projetos do usuário
  const fetchProjects = async () => {
    setLoading(true);
    try {
      const response = await api.get('/api/projetos');
      setProjects(response.data);
    } catch (error) {
      console.error("Erro ao carregar projetos:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (isOpen) {
      fetchProjects();
    }
  }, [isOpen, refreshTrigger]);

  return (
    <div 
      className={`fixed left-0 top-0 h-full z-40 transition-all duration-500 ease-in-out ${
        isOpen ? 'w-80' : 'w-0'
      }`}
    >
      {/* Sidebar Content */}
      <div className={`h-full w-full bg-white/70 backdrop-blur-xl border-r border-white/20 shadow-2xl relative overflow-hidden transition-opacity duration-300 ${
        isOpen ? 'opacity-100' : 'opacity-0'
      }`}>
        
        {/* Header */}
        <div className="p-6 border-b border-slate-200/50">
          <h2 className="text-xl font-bold text-slate-800 flex items-center gap-2">
            <svg className="w-6 h-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
            </svg>
            Meus Desenhos
          </h2>
        </div>

        {/* Project List */}
        <div className="p-4 overflow-y-auto h-[calc(100%-100px)]">
          {loading ? (
            <div className="flex justify-center p-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
            </div>
          ) : projects.length === 0 ? (
            <p className="text-center text-slate-500 mt-10">Nenhum projeto salvo ainda.</p>
          ) : (
            <div className="space-y-3">
              {projects.map((proj) => (
                <div 
                  key={proj.id}
                  onClick={() => onSelectProject(proj)}
                  className="group p-4 bg-white/50 hover:bg-white border border-slate-200/50 hover:border-indigo-300 rounded-xl cursor-pointer transition-all duration-300 hover:shadow-lg hover:-translate-y-0.5"
                >
                  <div className="flex justify-between items-start">
                    <h3 className="font-semibold text-slate-700 group-hover:text-indigo-600 transition-colors truncate pr-2">
                      {proj.nome_projeto}
                    </h3>
                    
                    <button 
                      onClick={(e) => onDeleteProject?.(proj.id, e)}
                      className="text-slate-300 hover:text-red-500 hover:bg-slate-50 rounded p-1 transition-all"
                      title="Excluir Projeto"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                  </div>
                  <div className="flex items-center gap-2 mt-2 text-[10px] text-slate-400 font-medium">
                    <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    {new Date(proj.data_criacao).toLocaleDateString('pt-BR')}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Toggle Button */}
      <button 
        onClick={() => setIsOpen(!isOpen)}
        className={`absolute top-1/2 -right-4 translate-y-[-50%] z-50 bg-indigo-600 text-white p-2 rounded-full shadow-xl hover:bg-indigo-700 transition-all duration-300 group ${
            isOpen ? 'rotate-180' : ''
        }`}
      >
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7" />
        </svg>
        
        {/* Tooltip */}
        <span className="absolute left-full ml-4 px-2 py-1 bg-slate-800 text-white text-[10px] rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none">
            {isOpen ? 'Fechar Menu' : 'Meus Projetos'}
        </span>
      </button>
    </div>
  );
};

export default ProjectSidebar;
