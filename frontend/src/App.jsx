import React, { useState, useRef, useEffect } from 'react';
import ExcalidrawWrapper from './components/ExcalidrawWrapper';
import Navbar from './components/Navbar';
import ProjectSidebar from './components/ProjectSidebar';
import api from './api';
import './index.css';

function App() {
  const [user, setUser] = useState(null);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [currentProject, setCurrentProject] = useState(null);
  const [refreshSidebar, setRefreshSidebar] = useState(0);
  const [toastMessage, setToastMessage] = useState("");
  const excalidrawRef = useRef(null);

  const triggerSidebarRefresh = () => setRefreshSidebar(prev => prev + 1);

  const showToast = (msg) => {
      setToastMessage(msg);
      setTimeout(() => setToastMessage(""), 3000);
  };

  // Verificar sessão ou injetar Modo Dev
  useEffect(() => {
    const savedUser = localStorage.getItem('username');
    if (savedUser) {
      setUser(savedUser);
    } else {
      // --- MODO DESENVOLVEDOR: Auto-Login ---
      console.log("--- MODO DEV: Injetando sessão Admin ---");
      localStorage.setItem('token', 'dev-admin-token');
      localStorage.setItem('username', 'Admin');
      setUser('Admin');
    }
  }, []);

  const handleLogout = () => {
    setUser(null);
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    window.location.reload();
  };

  const handleSave = async (forceNew = false) => {
    try {
      const defaultName = forceNew ? `Projeto_${new Date().getTime()}` : (currentProject?.name || `Projeto_${new Date().getTime()}`);
      const nome = prompt(forceNew ? "Nome para a cópia do projeto:" : "Nome do projeto:", defaultName);
      if (!nome) return; // cancelou o prompt

      const idAtual = forceNew ? null : currentProject?.id;
      const response = await excalidrawRef.current.salvar(nome, idAtual);
      
      if (response && response.id) {
        setCurrentProject({ id: response.id, name: nome });
        triggerSidebarRefresh();
        showToast("✓ Projeto salvo com sucesso!");
      }
    } catch (err) {
      console.error("Falha ao salvar", err);
      showToast("❌ Falha ao salvar o projeto.");
    }
  };

  const handleSaveAs = () => handleSave(true);

  const handleRename = async () => {
    if (!currentProject) {
        alert("Você precisa salvar o projeto primeiro para poder renomear!");
        return;
    }
    const newName = prompt("Novo nome do projeto:", currentProject.name);
    if (!newName || newName === currentProject.name) return;

    try {
        await api.put(`/api/projetos/${currentProject.id}/renomear`, { nome_projeto: newName });
        setCurrentProject(prev => ({ ...prev, name: newName }));
        triggerSidebarRefresh();
        showToast("✓ Projeto renomeado!");
    } catch (err) {
        console.error("Falha ao renomear", err);
        showToast("❌ Falha ao renomear.");
    }
  };

  const handleDelete = async (id, e) => {
    e.stopPropagation();
    if (!window.confirm("Atenção: Tem certeza que deseja excluir permanentemente este projeto?")) return;
    
    try {
        await api.delete(`/api/projetos/${id}`);
        if (currentProject && currentProject.id === id) {
            setCurrentProject(null);
            excalidrawRef.current?.carregarCena([]); // limpa a lousa
        }
        triggerSidebarRefresh();
        showToast("✓ Projeto excluído.");
    } catch (err) {
        console.error("Erro ao deletar", err);
        showToast("❌ Erro ao excluir o projeto.");
    }
  };

  const handleNewProject = () => {
    if (excalidrawRef.current?.getSceneElements?.()?.length > 0) {
       if (!window.confirm("Você tem alterações na lousa. Quer mesmo iniciar um novo quadro zerado?")) return;
    }
    setCurrentProject(null);
    excalidrawRef.current?.carregarCena([]);
  };

  const handleAnalyze = async () => {
    try {
      const result = await excalidrawRef.current.analisar();
      if (result && result.analise) {
        alert("Consultoria IA:\n\n" + result.analise);
      }
    } catch (err) {
      console.error("Falha na análise");
    }
  };

  const handleLoadProject = (proj) => {
    if (excalidrawRef.current) {
        try {
            setCurrentProject({ id: proj.id, name: proj.nome_projeto });
            const elements = typeof proj.elementos_json === 'string' 
                ? JSON.parse(proj.elementos_json) 
                : proj.elementos_json;
            excalidrawRef.current.carregarCena(elements);
        } catch (e) {
            console.error("Erro ao fazer parse dos elementos", e);
        }
    }
  };

  return (
    <div className="App immersive-layout">
      <Navbar 
        user={user} 
        currentProject={currentProject}
        onLogout={handleLogout}
        onSave={() => handleSave(false)}
        onSaveAs={handleSaveAs}
        onRename={handleRename}
        onNewProject={handleNewProject}
        onAnalyze={handleAnalyze}
      />
      
      <ProjectSidebar 
        isOpen={isSidebarOpen} 
        setIsOpen={setIsSidebarOpen} 
        onSelectProject={handleLoadProject} 
        onDeleteProject={handleDelete}
        refreshTrigger={refreshSidebar}
      />

      <main className="canvas-container relative">
        {toastMessage && (
            <div className="absolute top-4 left-1/2 -translate-x-1/2 z-[100] bg-slate-800 text-white px-6 py-3 rounded-full shadow-2xl animate-fade-in transition-all">
                {toastMessage}
            </div>
        )}
        <ExcalidrawWrapper ref={excalidrawRef} />
      </main>
    </div>
  );
}

export default App;
