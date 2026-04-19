import React, { useState, useImperativeHandle, forwardRef } from "react";
import { Excalidraw } from "@excalidraw/excalidraw";
import "@excalidraw/excalidraw/index.css";
import api from "../api";

const ExcalidrawWrapper = forwardRef((props, ref) => {
    const [excalidrawAPI, setExcalidrawAPI] = useState(null);
    const [status, setStatus] = useState("");

    useImperativeHandle(ref, () => ({
        salvar: async (nomeAtual, idAtual) => {
            if (!excalidrawAPI) return;
            setStatus("Processando Salvamento...");
            const elements = excalidrawAPI.getSceneElements();
            try {
                const payload = {
                    nome_projeto: nomeAtual || `Projeto_${new Date().getTime()}`,
                    elementos_json: elements
                };
                if (idAtual) payload.id = idAtual;
                
                const response = await api.post("/api/projetos/salvar", payload);
                setStatus(`Projeto Salvo no Banco!`);
                setTimeout(() => setStatus(""), 3000);
                return response.data;
            } catch (error) {
                console.error(error);
                setStatus("Erro na Persistência.");
                setTimeout(() => setStatus(""), 3000);
                throw error;
            }
        },
        analisar: async () => {
            if (!excalidrawAPI) return;
            setStatus("Agente IA Analisando...");
            const elements = excalidrawAPI.getSceneElements();
            try {
                const response = await api.post("/api/agente/analisar", {
                    nome_projeto: "Analise IA",
                    elementos_json: elements
                });
                setStatus("");
                return response.data;
            } catch (error) {
                console.error(error);
                setStatus("Falha na Consultoria IA.");
                setTimeout(() => setStatus(""), 3000);
                throw error;
            }
        },
        carregarCena: (elementos) => {
            if (!excalidrawAPI || !elementos) return;
            excalidrawAPI.updateScene({ elements: elementos });
        }
    }));

    return (
        <div className="wrapper-full">
            {status && (
                <div className="status-indicator">
                    {status}
                </div>
            )}

            <div className="excalidraw-canvas">
                <Excalidraw 
                    excalidrawAPI={(api) => setExcalidrawAPI(api)} 
                    langCode="pt-BR"
                    theme="light"
                />
            </div>
        </div>
    );
});

export default ExcalidrawWrapper;
