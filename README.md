# Menu-Analyzer
Projetos 1 - CESAR School

# 🍽️ Aplicativo de Restaurante - Interface com Tkinter

Este é um sistema de pedidos de restaurante com interface gráfica em Python, permitindo que usuários façam login, visualizem pratos, adicionem ao carrinho, configurem alergias e finalizem pedidos — tudo com uma interface estilizada usando `ttkbootstrap`.

## 🖼️ Funcionalidades

- Interface gráfica moderna com `ttkbootstrap`
- Banco de dados SQLite integrado
- Carrinho de compras com edição de itens
- Detecção de alergênicos por usuário
- Suporte a imagens para cada prato
- Scroll adaptado para diferentes telas
- Estrutura modular com múltiplas "telas virtuais"

## ⚙️ Requisitos

### ✅ Python

Você precisa do Python 3.8 ou superior. Para verificar:

python --version

### Pacotes Python

pip install ttkbootstrap pillow

| Pacote         | Finalidade                                                 |
| -------------- | ---------------------------------------------------------- |
| `ttkbootstrap` | Interface moderna para `tkinter`                           |
| `Pillow`       | Manipulação de imagens para exibição no app                |
| `sqlite3`      | Já incluso com Python — usado para gerenciar o banco local |

### 🧩 Tkinter (Interface Gráfica)

O `tkinter` já vem instalado com o Python em sistemas Windows e macOS.  
Se você estiver usando Linux e receber erro do tipo `ModuleNotFoundError: No module named 'tkinter`, instale com:

bash
sudo apt install python3-tk