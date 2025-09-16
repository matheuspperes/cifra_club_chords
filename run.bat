@echo off
title Projeto CifraClub

echo ===============================
echo    INICIANDO PROJETO CIFRACLUB
echo ===============================
echo.

REM Verifica se pipenv está instalado
echo Verificando dependencias...
pip show pipenv >nul 2>&1
if errorlevel 1 (
    echo Pipenv nao encontrado. Instalando...
    pip install pipenv
)

REM Instala dependancias do projeto
echo Instalando dependencias do projeto...
pipenv install

echo.
echo Iniciando aplicacao...
echo ===============================
echo.

REM Executa a aplicação
pipenv run python main.py

echo Abrindo pasta dos PDFs...
explorer "pdf_files"

REM Pausa para ver possíveis erros
echo.
echo Aplicacao finalizada. Pressione qualquer tecla para sair...
pause >nul