import os
import sys
import subprocess
import time

def print_banner():
    banner = """
    ===================================================
      🚀 BEM-VINDO AO CURSO SAAS ELITE: EXCALIDRAW
    ===================================================
      Configurando seu ambiente de aprendizado...
    """
    print(banner)

def check_python_version():
    if sys.version_info < (3, 10):
        print("❌ Erro: Este curso exige Python 3.10 ou superior.")
        sys.exit(1)

def setup_environment():
    print("📦 [1/3] Instalando dependências do Backend...")
    try:
        # Usando o caminho relativo a partir da pasta course
        backend_path = os.path.join("..", "backend")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", os.path.join(backend_path, "requirements.txt")])
        print("✅ Backend pronto!")
    except Exception as e:
        print(f"❌ Erro ao instalar dependências: {e}")

def create_dotenv():
    print("🔑 [2/3] Configurando variáveis de ambiente (.env)...")
    dotenv_path = os.path.join("..", "backend", ".env")
    if not os.path.exists(dotenv_path):
        with open(dotenv_path, "w") as f:
            f.write("SECRET_KEY=sua_chave_secreta_de_estudante_123\n")
            f.write("ALGORITHM=HS256\n")
            f.write("ACCESS_TOKEN_EXPIRE_MINUTES=60\n")
        print("✅ Arquivo .env criado com sucesso!")
    else:
        print("ℹ️ Arquivo .env já existe. Pulando...")

def welcome_message():
    print("\n" + "="*51)
    print("✨ TUDO PRONTO! Seu ambiente está configurado.")
    print("🔗 Próximo passo: Abra a pasta /course e comece pela Lição 01.")
    print("="*51 + "\n")

if __name__ == "__main__":
    print_banner()
    check_python_version()
    setup_environment()
    create_dotenv()
    welcome_message()
    time.sleep(2)
