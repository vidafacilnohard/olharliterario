// Global variables
let currentRating = 0;
let currentBook = '';
let isLoggedIn = false;
let currentUser = '';
let userProfile = {
    nome: '',
    email: '',
    dataNascimento: '',
    telefone: '',
    bio: '',
    foto: 'https://via.placeholder.com/150/ff8b7e/ffffff?text=Usuário'
};

// Small DOM helpers to keep the code tidy and null-safe
const $ = (sel, root = document) => root.querySelector(sel);
const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));

// --- API helpers (token storage + fetch wrapper) ---
const API_BASE = '';
function getToken() { return localStorage.getItem('authToken') || ''; }
function setToken(t) { if (t) localStorage.setItem('authToken', t); else localStorage.removeItem('authToken'); }

async function apiFetch(path, options = {}, skipJsonHeader = false) {
    const headers = Object.assign({}, options.headers || {});
    const token = getToken();
    if (token) headers['Authorization'] = 'Bearer ' + token;
    if (!skipJsonHeader && !headers['Content-Type']) headers['Content-Type'] = 'application/json';
    options.headers = headers;
    try {
        const res = await fetch(API_BASE + path, options);
        return res;
    } catch (err) {
        console.error('apiFetch error', err);
        throw err;
    }
}

// Carregar livros do banco de dados Django
async function carregarLivrosDjango() {
    try {
        // Buscar apenas livros em destaque
        const res = await fetch('/api/books?destaque=true');
        if (!res.ok) {
            console.warn('Erro ao carregar livros do Django');
            return;
        }
        
        const livros = await res.json();
        if (!Array.isArray(livros) || livros.length === 0) {
            console.log('Nenhum livro em destaque encontrado no banco de dados');
            return;
        }
        
        const grid = $('#booksGrid');
        if (!grid) return;
        
        // Limpar TODOS os cards (incluindo hardcoded)
        grid.innerHTML = '';
        
        // Adicionar livros em destaque do Django
        livros.forEach(livro => {
            const card = document.createElement('div');
            card.className = 'book-card';
            card.dataset.bookId = livro.id;
            
            // Adicionar cursor pointer e evento de clique
            card.style.cursor = 'pointer';
            card.addEventListener('click', function(e) {
                // Não redirecionar se clicou no botão abrir
                if (!e.target.classList.contains('abrir-btn')) {
                    window.location.href = `livro.html?id=${livro.id}`;
                }
            });
            
            // Tentar usar capa do banco, senão buscar na pasta images/ com nome do arquivo
            let capaUrl = livro.capa;
            if (!capaUrl) {
                // Gerar nome do arquivo baseado no título do livro
                const nomeArquivo = livro.titulo.toLowerCase()
                    .normalize('NFD').replace(/[\u0300-\u036f]/g, '') // Remove acentos
                    .replace(/[^a-z0-9\s-]/g, '') // Remove caracteres especiais
                    .replace(/\s+/g, '-') // Substitui espaços por hífens
                    .replace(/-+/g, '-'); // Remove hífens duplicados
                capaUrl = `images/${nomeArquivo}.jpg`;
            }
            // Fallback final para placeholder
            const placeholderUrl = 'https://via.placeholder.com/300x450/ff8b7e/ffffff?text=' + encodeURIComponent(livro.titulo);
            
            const sinopse = livro.sinopse || 'Descrição não disponível.';
            const autor = livro.autor || 'Autor Desconhecido';
            
            // Adicionar estrelas de avaliação
            let stars = '';
            if (livro.total_avaliacoes > 0) {
                const fullStars = Math.floor(livro.media_avaliacoes);
                const hasHalfStar = livro.media_avaliacoes % 1 >= 0.5;
                
                for (let i = 0; i < fullStars; i++) {
                    stars += '★';
                }
                if (hasHalfStar) {
                    stars += '½';
                }
                stars = `<div class="book-rating">${stars} (${livro.total_avaliacoes})</div>`;
            }
            
            card.innerHTML = `
                <div class="bookmark"></div>
                <div class="book-cover">
                    <img src="${capaUrl}" alt="${livro.titulo}" onerror="this.onerror=null; this.src='${placeholderUrl}'">
                </div>
                <div class="book-info">
                    <h3 class="book-title">${livro.titulo}</h3>
                    <p class="book-author">${autor}</p>
                    ${stars}
                    <p class="book-description">${sinopse}</p>
                    <button class="abrir-btn" onclick="event.stopPropagation(); window.location.href='livro.html?id=${livro.id}'">Abrir</button>
                </div>
            `;
            
            grid.appendChild(card);
        });
        
        console.log(`${livros.length} livros em destaque carregados do banco de dados`);
        
    } catch (err) {
        console.error('Erro ao carregar livros:', err);
    }
}

// Load current user/profile if token exists
async function loadCurrentUser() {
    const token = getToken();
    if (!token) {
        // Não está logado - mostrar botão de login
        atualizarInterfaceUsuario(false);
        return;
    }
    try {
        const res = await apiFetch('/api/profile');
        if (!res.ok) {
            setToken('');
            atualizarInterfaceUsuario(false);
            return;
        }
        const data = await res.json();
        userProfile.nome = data.nome || '';
        userProfile.email = data.email || '';
        userProfile.dataNascimento = data.dataNascimento || '';
        userProfile.telefone = data.telefone || '';
        userProfile.bio = data.bio || '';
        if (data.foto) {
            userProfile.foto = data.foto.startsWith('images/') ? data.foto : ('images/' + data.foto);
        }
        isLoggedIn = true;
        currentUser = userProfile.nome || (userProfile.email || '').split('@')[0];
        
        // Mostrar botão "Adicionar Livro" apenas para superusuários
        const btnAdicionarLivro = $('#btnAdicionarLivro');
        if (btnAdicionarLivro && data.is_superuser) {
            btnAdicionarLivro.style.display = 'block';
        }
        
        atualizarInterfaceUsuario(true);
    } catch (err) {
        console.error('loadCurrentUser failed', err);
        atualizarInterfaceUsuario(false);
    }
}

// Atualizar interface baseado no estado de login
function atualizarInterfaceUsuario(estaLogado) {
    const btnLogin = $('#btnLogin');
    const dropdownPerfil = $('#dropdownPerfil');
    
    if (estaLogado) {
        // Usuário logado - mostrar dropdown de perfil
        if (btnLogin) btnLogin.style.display = 'none';
        if (dropdownPerfil) dropdownPerfil.style.display = 'block';
    } else {
        // Usuário não logado - mostrar botão de login
        if (btnLogin) btnLogin.style.display = 'block';
        if (dropdownPerfil) dropdownPerfil.style.display = 'none';
        isLoggedIn = false;
        currentUser = '';
    }
}

// Toggle Search Dropdown
function toggleSearchDropdown() {
    const dropdown = $('#searchDropdown');
    if (!dropdown) return;
    dropdown.classList.toggle('active');

    // Close other dropdowns (safe)
    const explorar = $('#explorarDropdown');
    if (explorar) explorar.classList.remove('active');
}

// Select Search Option
// Select Search Option
function selectSearchOption(option) {
    const btn = $('.search-dropdown .dropdown-btn');
    if (btn && btn.childNodes && btn.childNodes[0]) {
        btn.childNodes[0].textContent = option + ' ';
    }
    const dropdown = $('#searchDropdown');
    if (dropdown) dropdown.classList.remove('active');

    // Show notification
    showNotification(`Filtro alterado para: ${option}`);
}

// Realizar Busca no Banco de Dados
async function realizarBusca() {
    const searchInput = $('.search-input');
    if (!searchInput) return;
    
    const searchTerm = searchInput.value.trim();
    if (!searchTerm) {
        showNotification('Digite algo para buscar', 'error');
        return;
    }
    
    // Fechar dropdown de sugestões se estiver aberto
    fecharDropdownSugestoes();
    
    // Obter tipo de busca (livros, autores, editoras)
    const btn = $('.search-dropdown .dropdown-btn');
    let searchType = 'livros';
    if (btn && btn.childNodes && btn.childNodes[0]) {
        searchType = btn.childNodes[0].textContent.trim();
    }
    
    showNotification(`Buscando ${searchType}: ${searchTerm}...`);
    
    try {
        // Buscar no banco de dados
        const res = await fetch(`/api/books?busca=${encodeURIComponent(searchTerm)}`);
        if (!res.ok) throw new Error('Erro ao buscar');
        
        const livros = await res.json();
        
        if (!Array.isArray(livros) || livros.length === 0) {
            showNotification('Nenhum resultado encontrado', 'error');
            return;
        }
        
        // Filtrar por tipo de busca
        let resultadosFiltrados = livros;
        if (searchType === 'autores') {
            resultadosFiltrados = livros.filter(livro => 
                livro.autor && livro.autor.toLowerCase().includes(searchTerm.toLowerCase())
            );
        } else if (searchType === 'editoras') {
            resultadosFiltrados = livros.filter(livro => 
                livro.editora && livro.editora.toLowerCase().includes(searchTerm.toLowerCase())
            );
        }
        
        if (resultadosFiltrados.length === 0) {
            showNotification(`Nenhum resultado encontrado em ${searchType}`, 'error');
            return;
        }
        
        // Se encontrou apenas 1 livro, redirecionar direto
        if (resultadosFiltrados.length === 1) {
            showNotification(`Abrindo: ${resultadosFiltrados[0].titulo}`);
            setTimeout(() => {
                window.location.href = `livro.html?id=${resultadosFiltrados[0].id}`;
            }, 500);
        } else {
            // Se encontrou múltiplos, redirecionar para primeiro resultado
            showNotification(`Abrindo: ${resultadosFiltrados[0].titulo}`);
            setTimeout(() => {
                window.location.href = `livro.html?id=${resultadosFiltrados[0].id}`;
            }, 500);
        }
        
    } catch (err) {
        console.error('Erro na busca:', err);
        showNotification('Erro ao realizar busca', 'error');
    }
}

// Buscar Sugestões em Tempo Real
let timeoutBusca = null;
async function buscarSugestoes() {
    const searchInput = $('.search-input');
    if (!searchInput) return;
    
    const searchTerm = searchInput.value.trim();
    
    // Limpar timeout anterior
    if (timeoutBusca) {
        clearTimeout(timeoutBusca);
    }
    
    // Se o campo estiver vazio, fechar dropdown
    if (!searchTerm || searchTerm.length < 2) {
        fecharDropdownSugestoes();
        return;
    }
    
    // Aguardar 300ms antes de buscar (debounce)
    timeoutBusca = setTimeout(async () => {
        try {
            const res = await fetch(`/api/books?busca=${encodeURIComponent(searchTerm)}`);
            if (!res.ok) return;
            
            const livros = await res.json();
            
            if (!Array.isArray(livros) || livros.length === 0) {
                fecharDropdownSugestoes();
                return;
            }
            
            // Limitar a 5 sugestões
            const sugestoes = livros.slice(0, 5);
            mostrarDropdownSugestoes(sugestoes);
            
        } catch (err) {
            console.error('Erro ao buscar sugestões:', err);
        }
    }, 300);
}

// Mostrar Dropdown de Sugestões
function mostrarDropdownSugestoes(livros) {
    // Criar ou obter dropdown
    let dropdown = $('#searchSuggestionsDropdown');
    if (!dropdown) {
        dropdown = document.createElement('div');
        dropdown.id = 'searchSuggestionsDropdown';
        dropdown.className = 'search-suggestions-dropdown';
        
        // Posicionar abaixo do search input
        const searchBox = $('.search-box');
        if (searchBox) {
            searchBox.style.position = 'relative';
            searchBox.appendChild(dropdown);
        }
    }
    
    // Construir HTML das sugestões
    const sugestoesHtml = livros.map(livro => {
        const capaUrl = livro.capa || 'https://via.placeholder.com/50x75/ff8b7e/ffffff?text=Livro';
        return `
            <div class="suggestion-item" onclick="window.location.href='livro.html?id=${livro.id}'" style="cursor: pointer; display: flex; gap: 10px; padding: 10px; border-bottom: 1px solid #e0e0e0; transition: background 0.2s;">
                <img src="${capaUrl}" alt="${livro.titulo}" style="width: 40px; height: 60px; object-fit: cover; border-radius: 4px;" onerror="this.src='https://via.placeholder.com/40x60/ff8b7e/ffffff?text=Livro'">
                <div style="flex: 1; min-width: 0;">
                    <div style="font-weight: 600; color: var(--primary-color); font-size: 14px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${livro.titulo}</div>
                    <div style="color: var(--text-light); font-size: 12px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${livro.autor || 'Autor Desconhecido'}</div>
                </div>
            </div>
        `;
    }).join('');
    
    dropdown.innerHTML = sugestoesHtml;
    dropdown.style.display = 'block';
    
    // Adicionar hover effect
    const items = dropdown.querySelectorAll('.suggestion-item');
    items.forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.style.background = 'var(--card-bg)';
        });
        item.addEventListener('mouseleave', function() {
            this.style.background = 'white';
        });
    });
}

// Fechar Dropdown de Sugestões
function fecharDropdownSugestoes() {
    const dropdown = $('#searchSuggestionsDropdown');
    if (dropdown) {
        dropdown.style.display = 'none';
    }
}

// Mostrar Resultados da Busca em Modal
function mostrarResultadosBusca(livros) {
    // Criar modal de resultados se não existir
    let modal = $('#searchResultsModal');
    if (!modal) {
        modal = document.createElement('div');
        modal.id = 'searchResultsModal';
        modal.className = 'modal';
        document.body.appendChild(modal);
    }
    
    // Construir HTML dos resultados
    const resultadosHtml = livros.map(livro => {
        const capaUrl = livro.capa || 'https://via.placeholder.com/150x220/ff8b7e/ffffff?text=' + encodeURIComponent(livro.titulo);
        return `
            <div class="search-result-item" onclick="window.location.href='livro.html?id=${livro.id}'" style="cursor: pointer; display: flex; gap: 15px; padding: 15px; border-bottom: 1px solid #e0e0e0; transition: background 0.2s;">
                <img src="${capaUrl}" alt="${livro.titulo}" style="width: 60px; height: 90px; object-fit: cover; border-radius: 5px;" onerror="this.src='https://via.placeholder.com/60x90/ff8b7e/ffffff?text=Livro'">
                <div style="flex: 1;">
                    <h4 style="margin: 0 0 5px 0; color: var(--primary-color);">${livro.titulo}</h4>
                    <p style="margin: 0; color: var(--text-light); font-size: 14px;">${livro.autor || 'Autor Desconhecido'}</p>
                    ${livro.editora ? `<p style="margin: 5px 0 0 0; color: var(--text-light); font-size: 12px;">Editora: ${livro.editora}</p>` : ''}
                </div>
            </div>
        `;
    }).join('');
    
    modal.innerHTML = `
        <div class="modal-content" style="max-width: 600px; max-height: 80vh; overflow-y: auto;">
            <span class="close" onclick="fecharModal('searchResultsModal')">&times;</span>
            <h2 style="color: var(--secondary-color); margin-bottom: 20px;">Resultados da Busca (${livros.length})</h2>
            <div class="search-results-list">
                ${resultadosHtml}
            </div>
        </div>
    `;
    
    modal.classList.add('active');
    
    // Adicionar hover effect
    const items = modal.querySelectorAll('.search-result-item');
    items.forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.style.background = 'var(--card-bg)';
        });
        item.addEventListener('mouseleave', function() {
            this.style.background = 'transparent';
        });
    });
}

// Toggle Explorar Dropdown
function toggleExplorarDropdown() {
    const dropdown = $('#explorarDropdown');
    if (!dropdown) return;
    dropdown.classList.toggle('active');

    // Close other dropdowns
    const search = $('#searchDropdown');
    const perfil = $('#perfilDropdown');
    if (search) search.classList.remove('active');
    if (perfil) perfil.classList.remove('active');
}

// Toggle Perfil Dropdown
function togglePerfilDropdown() {
    const dropdown = $('#perfilDropdown');
    if (!dropdown) return;
    dropdown.classList.toggle('active');

    // Close other dropdowns
    const search = $('#searchDropdown');
    const explorar = $('#explorarDropdown');
    if (search) search.classList.remove('active');
    if (explorar) explorar.classList.remove('active');
}

// Explorar Function
function explorar(categoria) {
    const explorarDropdown = $('#explorarDropdown');
    if (explorarDropdown) explorarDropdown.classList.remove('active');
    showNotification(`Explorando: ${categoria.replace('-', ' ')}`);

    // Simulate loading new content
    const grid = $('#booksGrid');
    if (grid) grid.style.opacity = '0.5';

    setTimeout(() => {
        if (grid) grid.style.opacity = '1';
        showNotification(`${categoria.replace('-', ' ')} carregados!`);
    }, 800);
}

// Ver Mais Function
function verMais() {
    showNotification('Carregando mais livros...');
    
    const grid = $('#booksGrid');
    // Try to load a manifest file (images/extra-covers.json) which lists filenames
    // If manifest is missing, fallback to scanning the Downloads path (not accessible from browser)
    // Try to load a richer metadata manifest first (titles + desc). Falls back to the simple list.
    fetch('images/extra-covers-meta.json').then(res => {
        if (!res.ok) throw new Error('Meta manifest not found');
        return res.json();
    }).then(meta => {
        if (!Array.isArray(meta) || !meta.length) throw new Error('Empty meta');
        meta.forEach(item => {
            try {
                const filename = item.file;
                const title = item.title || (filename.replace(/[-_]/g, ' ').replace(/\.[a-zA-Z0-9]+$/,''));
                const desc = item.desc || 'Descrição não disponível.';
                const card = document.createElement('div');
                card.className = 'book-card';
                card.innerHTML = `\n                    <div class="book-cover">\n                        <img src="images/${filename}" alt="${title}">\n                    </div>\n                    <div class="book-info">\n                        <h3 class="book-title">${title}</h3>\n                        <p class="book-description">${desc}</p>\n                        <button class="comentar-btn" onclick="comentar('${title.replace(/'/g, "\\'")}')">Comentar</button>\n                        <p class="book-author">Autor Desconhecido</p>\n                    </div>\n                `;
                if (grid) grid.appendChild(card);
            } catch (err) {
                console.error('Erro ao adicionar card from meta', err);
            }
        });
        showNotification('Mais livros foram adicionados!');
    }).catch(() => {
        // fallback to simple list
        fetch('images/extra-covers.json').then(res => {
            if (!res.ok) throw new Error('Manifest not found');
            return res.json();
        }).then(list => {
            if (!Array.isArray(list) || !list.length) {
                showNotification('Nenhuma capa nova encontrada no manifest.', 'error');
                return;
            }
            list.forEach(filename => {
                try {
                    const card = document.createElement('div');
                    card.className = 'book-card';
                    card.innerHTML = `\n                        <div class="book-cover">\n                            <img src="images/${filename}" alt="${filename}">\n                        </div>\n                        <div class="book-info">\n                            <h3 class="book-title">${filename.replace(/[-_]/g, ' ').replace(/\.[a-zA-Z0-9]+$/,'')}</h3>\n                            <p class="book-description">Descrição não disponível.</p>\n                            <button class="comentar-btn" onclick="comentar('${filename.replace(/'/g, "\\'")}')">Comentar</button>\n                            <p class="book-author">Autor Desconhecido</p>\n                        </div>\n                    `;
                    if (grid) grid.appendChild(card);
                } catch (err) {
                    console.error('Erro ao adicionar card', err);
                }
            });
            showNotification('Mais livros foram adicionados!');
        }).catch(err => {
            console.warn('verMais manifest load failed', err);
            showNotification('Não foi possível carregar novas capas automaticamente. Copie os arquivos para images/ e atualize extra-covers.json.', 'error');
        });
    });
}

// Open Login Modal
// Open Login Modal
function abrirLogin() {
    // Redirecionar para a página de login
    window.location.href = 'login.html';
}

// Open Cadastro Modal
function abrirCadastro() {
    // Sempre abre o modal de cadastro
    const modal = $('#cadastroModal');
    if (modal) modal.classList.add('active');
}

// Open Perfil
function abrirPerfil() {
    // Preencher dados do perfil no modal
    const nomeInput = $('#perfilNome');
    const emailInput = $('#perfilEmail');
    const dataInput = $('#perfilDataNascimento');
    const telInput = $('#perfilTelefone');
    const bioInput = $('#perfilBio');
    const fotoImg = $('#perfilFoto');

    if (nomeInput) nomeInput.value = userProfile.nome;
    if (emailInput) emailInput.value = userProfile.email;
    if (dataInput) dataInput.value = userProfile.dataNascimento || '';
    if (telInput) telInput.value = userProfile.telefone || '';
    if (bioInput) bioInput.value = userProfile.bio || '';
    if (fotoImg) fotoImg.src = userProfile.foto;

    // Limpar campos de senha
    const senhaAtual = $('#perfilSenhaAtual');
    const novaSenha = $('#perfilNovaSenha');
    const confirmarSenha = $('#perfilConfirmarSenha');
    if (senhaAtual) senhaAtual.value = '';
    if (novaSenha) novaSenha.value = '';
    if (confirmarSenha) confirmarSenha.value = '';

    // Abrir modal
    const perfilModal = $('#perfilModal');
    if (perfilModal) perfilModal.classList.add('active');
}

// Alterar Foto de Perfil
function alterarFotoPerfil(event) {
    const file = event.target.files[0];
    
    if (file) {
        if (file.size > 5000000) { // 5MB
            showNotification('A imagem é muito grande. Máximo 5MB.', 'error');
            return;
        }
        
        if (!file.type.startsWith('image/')) {
            showNotification('Por favor, selecione uma imagem válida.', 'error');
            return;
        }
        // Upload to backend
        const token = getToken();
        if (!token) {
            showNotification('Faça login para alterar a foto.', 'error');
            return;
        }

        const form = new FormData();
        form.append('file', file);

        showNotification('Enviando foto...');
        (async () => {
            try {
                const res = await fetch('/api/upload-photo', { method: 'POST', headers: { 'Authorization': 'Bearer ' + token }, body: form });
                if (!res.ok) {
                    const e = await res.json().catch(()=>({}));
                    showNotification(e.error || 'Erro ao enviar foto', 'error');
                    return;
                }
                const data = await res.json();
                if (data && data.foto) {
                    userProfile.foto = data.foto;
                    const foto = $('#perfilFoto');
                    if (foto) foto.src = data.foto;
                }
                showNotification('Foto atualizada com sucesso!');
            } catch (err) {
                console.error(err);
                showNotification('Erro de conexão ao enviar foto', 'error');
            }
        })();
    }
}

// Salvar Perfil
function salvarPerfil(event) {
    event.preventDefault();
    
    const nome = ($('#perfilNome') || {}).value || '';


    const email = ($('#perfilEmail') || {}).value || '';
    const dataNascimento = ($('#perfilDataNascimento') || {}).value || '';
    const telefone = ($('#perfilTelefone') || {}).value || '';
    const bio = ($('#perfilBio') || {}).value || '';
    
    const senhaAtual = ($('#perfilSenhaAtual') || {}).value || '';
    const novaSenha = ($('#perfilNovaSenha') || {}).value || '';
    const confirmarSenha = ($('#perfilConfirmarSenha') || {}).value || '';
    
    // Validar mudança de senha se algum campo foi preenchido
    if (senhaAtual || novaSenha || confirmarSenha) {
        if (!senhaAtual) {
            showNotification('Digite sua senha atual para alterar a senha.', 'error');
            return;
        }
        
        if (novaSenha.length < 6) {
            showNotification('A nova senha deve ter pelo menos 6 caracteres.', 'error');
            return;
        }
        
        if (novaSenha !== confirmarSenha) {
            showNotification('As senhas não coincidem.', 'error');
            return;
        }
    }
    
    showNotification('Salvando alterações...');
    (async () => {
        try {
            const body = { nome, telefone, bio, dataNascimento };
            const res = await apiFetch('/api/profile', { method: 'POST', body: JSON.stringify(body) });
            if (!res.ok) {
                const err = await res.json().catch(() => ({}));
                showNotification(err.error || 'Erro ao salvar perfil', 'error');
                return;
            }
            // update local profile
            userProfile.nome = nome;
            userProfile.email = email;
            userProfile.dataNascimento = dataNascimento;
            userProfile.telefone = telefone;
            userProfile.bio = bio;
            currentUser = nome;
            showNotification('Perfil atualizado com sucesso!');
            if (novaSenha) showNotification('Senha alterada (não implementada no backend)', 'success');
            fecharModal('perfilModal');
        } catch (err) {
            console.error(err);
            showNotification('Erro de conexão ao salvar perfil', 'error');
        }
    })();
}

// Fazer Logout
// Fazer Logout
function fazerLogout() {
    showNotification('Saindo...');
    
    // Limpar token e dados do usuário
    setToken('');
    isLoggedIn = false;
    currentUser = '';
    userProfile = {
        nome: '',
        email: '',
        dataNascimento: '',
        telefone: '',
        bio: '',
        foto: 'https://via.placeholder.com/150/ff8b7e/ffffff?text=Usuário'
    };
    
    setTimeout(() => {
        showNotification('Você saiu da sua conta. Até logo!');
        // Redirecionar para a página inicial
        window.location.href = 'index.html';
    }, 500);
}

// Open Chat
function abrirChat() {
    showNotification('Chat em desenvolvimento. Em breve você poderá conversar com outros leitores!');
}


            // Populate the banner with mini-book thumbnails (favorites)
            async function loadBannerFavorites() {
                // Prefer explicit #bannerMiniBooks, otherwise fallback to .banner-image-container
                let container = $('#bannerMiniBooks');
                if (!container) container = document.querySelector('.banner-image-container');
                if (!container) return;
                // If the container is the wrapper, ensure we populate an inner grid
                if (!container.classList.contains('banner-mini-grid')) {
                    let inner = container.querySelector('.banner-mini-grid');
                    if (!inner) {
                        inner = document.createElement('div');
                        inner.className = 'banner-mini-grid';
                        container.appendChild(inner);
                    }
                    container = inner;
                }
                container.innerHTML = '';

                // Prefer to populate from featured books (.book-card)
                const featured = $$('.book-card');
                if (featured && featured.length) {
                    // Create an array with book objects extracted from featured cards
                    const books = featured.map(card => {
                        const imgEl = card.querySelector('.book-cover img');
                        const titleEl = card.querySelector('.book-title') || card.querySelector('h3');
                        const descEl = card.querySelector('.book-description') || card.querySelector('p');
                        return {
                            title: (titleEl && (titleEl.textContent || titleEl.innerText)) || (imgEl && (imgEl.alt || imgEl.title)) || 'Livro',
                            img: (imgEl && (imgEl.src || imgEl.getAttribute('src'))) || 'images/placeholder-culpa.svg',
                            desc: (descEl && (descEl.textContent || descEl.innerText)) || ''
                        };
                    });

                    // Ensure we have 12 items (duplicate cyclically if needed)
                    const target = 12;
                    let i = 0;
                    while (i < Math.max(target, books.length)) {
                        const b = books[i % books.length];
                        createMiniBook(container, b);
                        i++;
                    }
                    // Optionally add one extra (13th) for variety
                    if (books.length > 0 && books.length < 13) {
                        createMiniBook(container, books[0]);
                    }
                    return;
                }

                // Last resort: use all cover images found on page
                const covers = $$('.book-cover img');
                if (covers && covers.length) {
                    covers.slice(0, 12).forEach(img => {
                        const book = { title: img.alt || 'Livro', img: img.src || 'images/placeholder-culpa.svg', desc: '' };
                        createMiniBook(container, book);
                    });
                    return;
                }

                // Final fallback: static list of 13 sample books (ensures the banner nunca fica vazio)
                const staticFallback = [
                    { title: '1984', img: 'https://m.media-amazon.com/images/I/71kxa1-0mfL.jpg', desc: 'George Orwell' },
                    { title: 'O Pequeno Príncipe', img: 'https://m.media-amazon.com/images/I/81e4r7WZxYL.jpg', desc: 'Antoine de Saint-Exupéry' },
                    { title: 'Dom Casmurro', img: 'https://m.media-amazon.com/images/I/81Jx0sWw1-L.jpg', desc: 'Machado de Assis' },
                    { title: 'A Culpa é das Estrelas', img: 'images/culpa-das-estrelas.jpg', desc: 'John Green' },
                    { title: 'Harry Potter', img: 'https://m.media-amazon.com/images/I/81ibfYk4qmL._SY466_.jpg', desc: 'J. K. Rowling' },
                    { title: 'O Alquimista', img: 'https://m.media-amazon.com/images/I/71aFt4+OTOL.jpg', desc: 'Paulo Coelho' },
                    { title: 'O Morro dos Ventos Uivantes', img: 'https://m.media-amazon.com/images/I/81p3i1G3LXL.jpg', desc: 'Emily Brontë' },
                    { title: 'Cem Anos de Solidão', img: 'https://m.media-amazon.com/images/I/81r+LN0x0lL.jpg', desc: 'Gabriel García Márquez' },
                    { title: 'O Senhor dos Anéis', img: 'https://m.media-amazon.com/images/I/91b0C2YNSrL.jpg', desc: 'J. R. R. Tolkien' },
                    { title: 'Sapiens', img: 'https://m.media-amazon.com/images/I/713jIoMO3UL.jpg', desc: 'Yuval Noah Harari' },
                    { title: 'A Sutil Arte de Ligar o F*da-se', img: 'https://m.media-amazon.com/images/I/71QKQ9mwV7L._SY466_.jpg', desc: 'Mark Manson' },
                    { title: 'O Apanhador no Campo de Centeio', img: 'https://m.media-amazon.com/images/I/71g2ednj0JL.jpg', desc: 'J. D. Salinger' },
                    { title: 'O Hobbit', img: 'https://m.media-amazon.com/images/I/91b0C2YNSrL.jpg', desc: 'J. R. R. Tolkien' }
                ];
                staticFallback.forEach(b => createMiniBook(container, b));
            }

            function createMiniBook(container, book) {
                const div = document.createElement('div');
                div.className = 'mini-book';
                // make mini-books purely visual (no keyboard focus / role) per user request
                // previously: div.tabIndex = 0; div.setAttribute('role', 'button');

                // enforce fixed sizing to avoid layout-driven differences
                div.style.width = getComputedStyle(document.documentElement).getPropertyValue('--mini-book-w') || '54px';
                div.style.height = getComputedStyle(document.documentElement).getPropertyValue('--mini-book-h') || '92px';

                const cover = document.createElement('div');
                cover.className = 'mini-cover';
                const img = document.createElement('img');
                img.src = book.img || 'images/placeholder-culpa.svg';
                img.alt = book.title || 'Livro';
                // enforce cover size
                cover.style.width = getComputedStyle(document.documentElement).getPropertyValue('--mini-cover-w') || '46px';
                cover.style.height = getComputedStyle(document.documentElement).getPropertyValue('--mini-cover-h') || '70px';
                cover.appendChild(img);

                const title = document.createElement('div');
                title.className = 'mini-book-title';
                title.textContent = book.title || '';

                div.appendChild(cover);
                div.appendChild(title);

                // Interaction disabled: do not open modal or react to keys/clicks per user request
                // div.addEventListener('click', () => openBookModal(book));
                // div.addEventListener('keypress', (e) => { if (e.key === 'Enter') openBookModal(book); });

                container.appendChild(div);
            }

            function openBookModal(book) {
                try {
                    const modal = $('#bookModal');
                    if (!modal) return;
                    const img = $('#modalBookImg');
                    const title = $('#modalBookTitle');
                    const desc = $('#modalBookDesc');
                    if (img) { img.src = book.img || 'images/placeholder-culpa.svg'; img.alt = book.title || 'Livro'; }
                    if (title) title.textContent = book.title || '';
                    if (desc) desc.textContent = book.desc || book.description || 'Sem descrição disponível.';
                    modal.classList.add('active');
                } catch (err) {
                    console.error('openBookModal error', err);
                }
            }

            // Wire the modal "Abrir Livro" button to a simple action
            function wireBookModalActions() {
                const openBtn = $('#openBookBtn');
                if (openBtn) {
                    openBtn.addEventListener('click', () => {
                        showNotification('Abrindo livro...');
                        // Simple demo: close modal after a short delay
                        setTimeout(() => {
                            fecharModal('bookModal');
                        }, 800);
                    });
                }

                // Close modal on Escape key
                document.addEventListener('keydown', (e) => {
                    if (e.key === 'Escape') {
                        fecharModal('bookModal');
                    }
                });
            }

            // Enable drag-to-scroll for the banner mini grid (mouse / touch / pointer friendly)
            function enableBannerDrag() {
                const grid = document.querySelector('.banner-mini-grid');
                if (!grid) return;

                let isDown = false;
                let startX;
                let scrollLeftStart;

                grid.addEventListener('pointerdown', (e) => {
                    isDown = true;
                    grid.setPointerCapture(e.pointerId);
                    grid.classList.add('grabbing');
                    startX = e.clientX;
                    scrollLeftStart = grid.scrollLeft;

                    // Visual feedback: scale the target mini-book if clicked
                    const target = e.target.closest('.mini-book');
                    if (target) target.classList.add('dragging');
                });

                grid.addEventListener('pointermove', (e) => {
                    if (!isDown) return;
                    const dx = e.clientX - startX;
                    grid.scrollLeft = scrollLeftStart - dx;
                });

                function endDrag(e) {
                    if (!isDown) return;
                    isDown = false;
                    try { grid.releasePointerCapture && grid.releasePointerCapture(e.pointerId); } catch (_) {}
                    grid.classList.remove('grabbing');
                    // remove dragging class from any mini-book
                    grid.querySelectorAll('.mini-book.dragging').forEach(n => n.classList.remove('dragging'));
                }

                grid.addEventListener('pointerup', endDrag);
                grid.addEventListener('pointercancel', endDrag);

                // Also support wheel-to-scroll by horizontal wheel or shift+wheel
                grid.addEventListener('wheel', (e) => {
                    if (Math.abs(e.deltaX) > 0 || e.shiftKey) {
                        // let default horizontal scroll
                        return;
                    }
                    // Convert vertical wheel to horizontal scroll for convenience
                    e.preventDefault();
                    grid.scrollLeft += e.deltaY;
                }, { passive: false });
            }
// Close Modal
function fecharModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.classList.remove('active');
}

// Spawn multiple small moving book icons that bounce inside the banner
function spawnMovingBooks(count = 12) {
    const container = document.querySelector('.banner-image-container');
    if (!container) return;

    // Ensure overlay exists (and clear any existing content)
    let overlay = container.querySelector('.banner-moving');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.className = 'banner-moving';
        container.appendChild(overlay);
    }
    overlay.innerHTML = '';

    const books = [];

    // Determine covers to use: prefer the miniatures inside the banner; fallback to featured cards
    const miniCovers = $$('.banner-mini-grid .mini-cover img').map(i => i.src).filter(Boolean);
    const coverEls = $$('.book-card .book-cover img');
    const coverUrls = coverEls.map(i => i.src).filter(Boolean);
    const staticCovers = [
        'images/culpa-das-estrelas.jpg',
        'https://m.media-amazon.com/images/I/81ibfYk4qmL._SY466_.jpg',
        'https://m.media-amazon.com/images/I/71QKQ9mwV7L._SY466_.jpg'
    ];
    const coversPool = (miniCovers.length ? miniCovers : (coverUrls.length ? coverUrls : staticCovers));

    // Compute size as 3% of the banner width (interpretação: 3% da faixa = largura da faixa)
    const rect = container.getBoundingClientRect();
    const BASE_W = Math.max(20, Math.round(rect.width * 0.03)); // minimum to keep visible
    const ASPECT = 52 / 36; // keep previous portrait aspect ratio (height = width * ASPECT)
    const BASE_H = Math.round(BASE_W * ASPECT);

    // Create N moving-book elements (if count omitted, use number of covers available)
    const total = (typeof count === 'number' && count > 0) ? count : Math.max(6, coversPool.length);

    for (let i = 0; i < total; i++) {
        const el = document.createElement('div');
        el.className = 'moving-book';
        // set computed pixel sizes so all are identical
        el.style.width = BASE_W + 'px';
        el.style.height = BASE_H + 'px';
        el.style.position = 'absolute';

        const img = document.createElement('img');
        img.src = coversPool[i % coversPool.length] || coversPool[Math.floor(Math.random() * coversPool.length)];
        img.alt = 'capa';
        img.style.width = '100%';
        img.style.height = '100%';
        img.style.objectFit = 'cover';
        el.appendChild(img);
        overlay.appendChild(el);

        // Random initial position inside the banner
        const bw = BASE_W;
        const bh = BASE_H;
        const W = Math.max(1, rect.width);
        const H = Math.max(1, rect.height);
        const x = Math.random() * Math.max(1, W - bw);
        const y = Math.random() * Math.max(1, H - bh);
        const vx = (Math.random() * 2 - 1) * 1.2;
        const vy = (Math.random() * 2 - 1) * 1.0;

        const book = { el, x, y, vx, vy, w: bw, h: bh, grabbed: false };
        books.push(book);

        // pointer drag per element
        el.addEventListener('pointerdown', (ev) => {
            book.grabbed = true;
            el.classList.add('dragging');
            try { el.setPointerCapture(ev.pointerId); } catch (e) {}
        });
        el.addEventListener('pointermove', (ev) => {
            if (!book.grabbed) return;
            const local = overlay.getBoundingClientRect();
            book.x = ev.clientX - local.left - book.w / 2;
            book.y = ev.clientY - local.top - book.h / 2;
            book.vx = 0; book.vy = 0;
        });
        el.addEventListener('pointerup', (ev) => {
            book.grabbed = false;
            el.classList.remove('dragging');
            try { el.releasePointerCapture(ev.pointerId); } catch(e){}
            // small shove
            book.vx = (Math.random() * 2 - 1) * 1.2;
            book.vy = (Math.random() * 2 - 1) * 1.0;
        });
        el.addEventListener('pointercancel', () => { book.grabbed = false; el.classList.remove('dragging'); });
    }

    // Animation loop
    let last = performance.now();
    function step(now) {
        const dt = Math.min(40, now - last) / 16.666;
        last = now;
        const rectNow = container.getBoundingClientRect();
        const W = rectNow.width;
        const H = rectNow.height;

        books.forEach(b => {
            if (!b.grabbed) {
                b.x += b.vx * dt;
                b.y += b.vy * dt;
                b.vx *= 0.999;
                b.vy *= 0.999;
            }

            // bounce
            if (b.x <= 0) { b.x = 0; b.vx = Math.abs(b.vx); }
            if (b.y <= 0) { b.y = 0; b.vy = Math.abs(b.vy); }
            if (b.x + b.w >= W) { b.x = W - b.w; b.vx = -Math.abs(b.vx); }
            if (b.y + b.h >= H) { b.y = H - b.h; b.vy = -Math.abs(b.vy); }

            b.el.style.transform = `translate(${b.x}px, ${b.y}px)`;
        });

        requestAnimationFrame(step);
    }
    requestAnimationFrame(step);

    // Recompute sizes/positions on resize so 3% rule continues to apply
    let resizeTimer = null;
    function onResize() {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {
            const rect2 = container.getBoundingClientRect();
            const newBaseW = Math.max(20, Math.round(rect2.width * 0.03));
            const newBaseH = Math.round(newBaseW * ASPECT);
            books.forEach(b => {
                b.w = newBaseW; b.h = newBaseH;
                b.el.style.width = newBaseW + 'px';
                b.el.style.height = newBaseH + 'px';
                // clamp positions so they stay inside
                if (b.x + b.w > rect2.width) b.x = Math.max(0, rect2.width - b.w);
                if (b.y + b.h > rect2.height) b.y = Math.max(0, rect2.height - b.h);
            });
        }, 120);
    }
    window.addEventListener('resize', onResize);
}

// Spawn moving mini covers (visual-only, non-interactive)
async function spawnMovingMiniCovers(count = 12) {
    const container = document.querySelector('.banner-image-container');
    if (!container) return;

    // Ensure overlay exists (and clear any existing content)
    let overlay = container.querySelector('.banner-moving');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.className = 'banner-moving';
        container.appendChild(overlay);
    }
    overlay.innerHTML = '';
    overlay.style.pointerEvents = 'none';
    overlay.style.display = 'block';
    overlay.style.zIndex = '6';

    // build covers pool from banner mini-grid, featured cards and extra meta (avoid duplicates)
    const miniImgs = $$('.banner-mini-grid .mini-cover img').map(i => i.src).filter(Boolean);
    const coverEls = $$('.book-card .book-cover img').map(i => i.src).filter(Boolean);
    let coversPool = [];
    coversPool = coversPool.concat(coverEls).concat(miniImgs);
    // try to merge extra covers meta
    try {
        const res = await fetch('images/extra-covers-meta.json');
        if (res.ok) {
            const meta = await res.json();
            if (Array.isArray(meta)) {
                meta.forEach(it => { if (it && it.file) coversPool.push('images/' + it.file); });
            }
        }
    } catch (e) {
        // ignore
    }
    // dedupe
    coversPool = Array.from(new Set(coversPool)).filter(Boolean);

    // fixed size requested now: 15px width (height proportional)
    const rect = container.getBoundingClientRect();
    const FIXED_W = 19; // adjusted per user request
    const ASPECT = 92 / 54; // portrait aspect similar to mini-book
    const FIXED_H = Math.round(FIXED_W * ASPECT);

    // default to one moving icon per available cover
    const total = (typeof count === 'number' && count > 0) ? count : Math.max(6, coversPool.length);

    const items = [];
    for (let i = 0; i < total; i++) {
        const el = document.createElement('div');
        el.className = 'moving-book';
    el.style.position = 'absolute';
    el.style.width = FIXED_W + 'px';
    el.style.height = FIXED_H + 'px';
    el.style.pointerEvents = 'none';
    el.style.display = 'block';

        const img = document.createElement('img');
        img.src = coversPool[i % coversPool.length];
        img.alt = 'capa';
        img.style.width = '100%';
        img.style.height = '100%';
        img.style.objectFit = 'cover';
        el.appendChild(img);
        overlay.appendChild(el);

    const W = Math.max(1, rect.width);
    const H = Math.max(1, rect.height);
    const x = Math.random() * Math.max(1, W - FIXED_W);
    const y = Math.random() * Math.max(1, H - FIXED_H);
    // increased speed multipliers (more lively)
    const vx = (Math.random() * 2 - 1) * 2.3; // increased horizontal speed (+0.5)
    const vy = (Math.random() * 2 - 1) * 1.9; // increased vertical speed (+0.5)

        items.push({ el, x, y, vx, vy, w: FIXED_W, h: FIXED_H });
    }

    let last = performance.now();
    function step(now) {
        const dt = Math.min(40, now - last) / 16.666;
        last = now;
            const rectNow = container.getBoundingClientRect();
            const W = rectNow.width;
            const H = rectNow.height;

        items.forEach(b => {
            b.x += b.vx * dt;
            b.y += b.vy * dt;
            b.vx *= 0.999;
            b.vy *= 0.999;

            if (b.x <= 0) { b.x = 0; b.vx = Math.abs(b.vx); }
            if (b.y <= 0) { b.y = 0; b.vy = Math.abs(b.vy); }
            if (b.x + b.w >= W) { b.x = W - b.w; b.vx = -Math.abs(b.vx); }
            if (b.y + b.h >= H) { b.y = H - b.h; b.vy = -Math.abs(b.vy); }

            b.el.style.transform = `translate(${b.x}px, ${b.y}px)`;
        });

        requestAnimationFrame(step);
    }
    requestAnimationFrame(step);

    // on resize update sizes/positions
    let resizeTimer = null;
    function onResize() {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {
            const rect2 = container.getBoundingClientRect();
            const newBaseW = Math.max(12, Math.round(rect2.width * 0.03));
            const newBaseH = Math.round(newBaseW * ASPECT);
            items.forEach(b => {
                b.w = newBaseW; b.h = newBaseH;
                b.el.style.width = newBaseW + 'px';
                b.el.style.height = newBaseH + 'px';
                if (b.x + b.w > rect2.width) b.x = Math.max(0, rect2.width - b.w);
                if (b.y + b.h > rect2.height) b.y = Math.max(0, rect2.height - b.h);
            });
        }, 120);
    }
    window.addEventListener('resize', onResize);
}

// Switch between modals
function trocarModal(closeModalId, openModalId) {
    fecharModal(closeModalId);
    setTimeout(() => {
        const modal = document.getElementById(openModalId);
        if (modal) modal.classList.add('active');
    }, 300);
}

// Login Form Submit
function fazerLogin(event) {
    event.preventDefault();
    
    const email = ($('#email') || {}).value || '';
    const senha = ($('#senha') || {}).value || '';
    if (!email || !senha) {
        showNotification('Preencha email e senha', 'error');
        return;
    }
    showNotification('Fazendo login...');
    (async () => {
        try {
            const res = await apiFetch('/api/login', { method: 'POST', body: JSON.stringify({ email, senha }) });
            const data = await res.json().catch(()=>({}));
            if (!res.ok) {
                showNotification(data.error || 'Credenciais inválidas', 'error');
                return;
            }
            const token = data.token;
            setToken(token);
            isLoggedIn = true;
            currentUser = data.user.nome || (data.user.email || '').split('@')[0];
            userProfile.nome = data.user.nome || currentUser;
            userProfile.email = data.user.email || email;
            showNotification(`Bem-vindo de volta, ${currentUser}!`);
            fecharModal('loginModal');
            // Atualizar interface para mostrar perfil logado
            atualizarInterfaceUsuario(true);
        } catch (err) {
            console.error(err);
            showNotification('Erro de conexão durante login', 'error');
        }
    })();
}

// Cadastro Form Submit
function fazerCadastro(event) {
    event.preventDefault();
    
    const nome = ($('#nome') || {}).value || '';
    const email = ($('#emailCadastro') || {}).value || '';
    const dataNascimento = ($('#dataNascimentoCadastro') || {}).value || '';
    const senha = ($('#senhaCadastro') || {}).value || '';
    const confirmarSenha = ($('#confirmarSenhaCadastro') || {}).value || '';
    const aceitarTermos = ($('#aceitarTermos') || {}).checked || false;
    
    // Validar senhas
    if (senha !== confirmarSenha) {
        showNotification('As senhas não coincidem!', 'error');
        return;
    }
    
    if (senha.length < 6) {
        showNotification('A senha deve ter pelo menos 6 caracteres!', 'error');
        return;
    }
    
    // Validar data de nascimento (usuário deve ter pelo menos 13 anos)
    const hoje = new Date();
    const nascimento = new Date(dataNascimento);
    const idade = hoje.getFullYear() - nascimento.getFullYear();
    const mesAtual = hoje.getMonth();
    const diaAtual = hoje.getDate();
    const mesNascimento = nascimento.getMonth();
    const diaNascimento = nascimento.getDate();
    
    let idadeReal = idade;
    if (mesAtual < mesNascimento || (mesAtual === mesNascimento && diaAtual < diaNascimento)) {
        idadeReal--;
    }
    
    if (idadeReal < 13) {
        showNotification('Você deve ter pelo menos 13 anos para se cadastrar.', 'error');
        return;
    }
    
    if (!aceitarTermos) {
        showNotification('Você deve aceitar os Termos de Uso para se cadastrar.', 'error');
        return;
    }
    
    showNotification('Criando sua conta...');
    (async () => {
        try {
            const res = await apiFetch('/api/register', { method: 'POST', body: JSON.stringify({ nome, email, senha, dataNascimento }) });
            const data = await res.json().catch(()=>({}));
            if (!res.ok) {
                showNotification(data.error || 'Erro ao criar conta', 'error');
                return;
            }
            setToken(data.token);
            isLoggedIn = true;
            currentUser = nome;
            userProfile.nome = nome;
            userProfile.email = email;
            userProfile.dataNascimento = dataNascimento;
            showNotification(`Bem-vindo ao Olhar Literário, ${nome}!`);
            fecharModal('cadastroModal');
            const form = $('#formCadastro');
            if (form) form.reset();
            // Atualizar interface para mostrar perfil logado
            atualizarInterfaceUsuario(true);
        } catch (err) {
            console.error(err);
            showNotification('Erro de conexão ao criar conta', 'error');
        }
    })();
}

// Verificar igualdade de senhas em tempo real
function verificarSenhas() {
    const senha = ($('#senhaCadastro') || {}).value || '';
    const confirmarSenha = ($('#confirmarSenhaCadastro') || {}).value || '';
    const feedback = $('#senhaFeedback');
    
    if (!feedback) return;
    if (confirmarSenha.length === 0) {
        feedback.textContent = '';
        feedback.className = 'senha-feedback';
        return;
    }
    
    if (senha === confirmarSenha) {
        feedback.textContent = '✓ As senhas coincidem';
        feedback.className = 'senha-feedback match';
    } else {
        feedback.textContent = '✗ As senhas não coincidem';
        feedback.className = 'senha-feedback mismatch';
    }
}

// Abrir Termos de Uso
function abrirTermos() {
    showNotification('Abrindo Termos de Uso...');
    // Aqui você pode abrir um modal ou redirecionar para uma página de termos
    setTimeout(() => {
        alert('TERMOS DE USO - OLHAR LITERÁRIO\n\n' +
              '1. Aceitação dos Termos\n' +
              'Ao usar nosso site, você concorda com estes termos.\n\n' +
              '2. Uso do Serviço\n' +
              'O serviço é fornecido para uso pessoal e não comercial.\n\n' +
              '3. Conta de Usuário\n' +
              'Você é responsável por manter a segurança da sua conta.\n\n' +
              '4. Conteúdo\n' +
              'Todo conteúdo postado é de responsabilidade do usuário.\n\n' +
              '5. Privacidade\n' +
              'Seus dados são protegidos conforme nossa Política de Privacidade.\n\n' +
              'Data: Outubro de 2025');
    }, 500);
}

// Abrir Política de Privacidade
function abrirPrivacidade() {
    showNotification('Abrindo Política de Privacidade...');
    setTimeout(() => {
        alert('POLÍTICA DE PRIVACIDADE - OLHAR LITERÁRIO\n\n' +
              '1. Coleta de Dados\n' +
              'Coletamos apenas dados necessários para o funcionamento do serviço.\n\n' +
              '2. Uso de Dados\n' +
              'Seus dados são usados para personalizar sua experiência.\n\n' +
              '3. Compartilhamento\n' +
              'Não compartilhamos seus dados com terceiros sem consentimento.\n\n' +
              '4. Segurança\n' +
              'Utilizamos medidas de segurança para proteger seus dados.\n\n' +
              '5. Seus Direitos\n' +
              'Você pode acessar, corrigir ou excluir seus dados a qualquer momento.\n\n' +
              'Data: Outubro de 2025');
    }, 500);
}

// Comentar Function
// Comentar Function
function comentar(livro) {
    // Verificar se o usuário está logado
    if (!isLoggedIn || !getToken()) {
        showNotification('Você precisa fazer login para comentar!', 'error');
        // Abrir modal de login após 1 segundo
        setTimeout(() => {
            abrirLogin();
        }, 1000);
        return;
    }
    
    currentBook = livro;
    document.getElementById('livroTitulo').textContent = livro;
    document.getElementById('comentarioModal').classList.add('active');
    currentRating = 0;
    
    // Reset stars
    document.querySelectorAll('.star').forEach(star => {
        star.classList.remove('active');
    });
}

// Set Rating
function setRating(rating) {
    currentRating = rating;
    
    const stars = document.querySelectorAll('.star');
    stars.forEach((star, index) => {
        if (index < rating) {
            star.classList.add('active');
        } else {
            star.classList.remove('active');
        }
    });
}

// Enviar Comentário
function enviarComentario(event) {
    event.preventDefault();
    
    const comentario = document.getElementById('comentario').value;
    
    if (currentRating === 0) {
        showNotification('Por favor, selecione uma avaliação!', 'error');
        return;
    }
    if (!getToken()) {
        showNotification('Faça login para enviar comentários.', 'error');
        return;
    }
    showNotification('Enviando comentário...');
    (async () => {
        try {
            const body = { book_title: currentBook, comment: comentario, rating: currentRating };
            const res = await apiFetch('/api/comments', { method: 'POST', body: JSON.stringify(body) });
            const data = await res.json().catch(()=>({}));
            if (!res.ok) {
                showNotification(data.error || 'Erro ao enviar comentário', 'error');
                return;
            }
            showNotification(`Comentário sobre "${currentBook}" enviado com sucesso! Avaliação: ${currentRating} estrelas`);
            fecharModal('comentarioModal');
            const campo = document.getElementById('comentario');
            if (campo) campo.value = '';
            currentRating = 0;
            
            // Recarregar a página para mostrar o novo comentário
            setTimeout(() => {
                window.location.reload();
            }, 1500);
        } catch (err) {
            console.error(err);
            showNotification('Erro de conexão ao enviar comentário', 'error');
        }
    })();
}

// Navegar Para
function navegarPara(secao) {
    showNotification(`Navegando para: ${secao}`);
}

// Abrir Rede Social
function abrirRedeSocial(rede) {
    showNotification(`Abrindo ${rede}...`);
    
    const urls = {
        instagram: 'https://instagram.com',
        facebook: 'https://facebook.com',
        twitter: 'https://twitter.com'
    };
    
    // Simulate opening social media
    setTimeout(() => {
        const url = urls[rede];
        if (url) window.open(url, '_blank');
    }, 500);
}

// Notification System
function showNotification(message, type = 'success') {
    // Remove existing notification
    const existingNotification = document.querySelector('.notification');
    if (existingNotification) {
        existingNotification.remove();
    }
    
    // Create notification
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'error' ? '#e74c3c' : '#2ecc71'};
        color: white;
        padding: 15px 25px;
        border-radius: 10px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        z-index: 10000;
        animation: slideInRight 0.3s ease;
        font-weight: 500;
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

// Add animation styles
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
// The following DOM-dependent initialization is performed when the DOM is ready
document.addEventListener('DOMContentLoaded', async function() {
    showNotification('Bem-vindo ao Olhar Literário! 📚');

    // Try to restore logged-in user from token
    await loadCurrentUser();
    
    // Carregar livros do banco de dados Django
    await carregarLivrosDjango();

    // Definir data máxima para cadastro (hoje)
    const hoje = new Date();
    const dataMaxima = hoje.toISOString().split('T')[0];
    const campoData = $('#dataNascimentoCadastro');
    if (campoData) {
        campoData.setAttribute('max', dataMaxima);
    }

    // Adicionar listeners para verificação de senha
    const senhaCadastro = $('#senhaCadastro');
    const confirmarSenhaCadastro = $('#confirmarSenhaCadastro');

    if (senhaCadastro) {
        senhaCadastro.addEventListener('input', verificarSenhas);
    }

    if (confirmarSenhaCadastro) {
        confirmarSenhaCadastro.addEventListener('input', verificarSenhas);
    }

    // Close dropdowns when clicking outside
    document.addEventListener('click', function(event) {
        const searchDropdown = $('#searchDropdown');
        const explorarDropdown = $('#explorarDropdown');
        const perfilDropdown = $('#perfilDropdown');

        if (!event.target.closest || (!event.target.closest('.search-dropdown') && !event.target.closest('.nav-dropdown'))) {
            if (searchDropdown) searchDropdown.classList.remove('active');
            if (explorarDropdown) explorarDropdown.classList.remove('active');
            if (perfilDropdown) perfilDropdown.classList.remove('active');
        }
    });

    // Close modals when clicking outside
    $$(".modal").forEach(modal => {
        modal.addEventListener('click', function(event) {
            if (event.target === modal) {
                fecharModal(modal.id);
            }
        });
    });

    // Remove any floating large decorative books if present
    try {
        document.querySelectorAll('.floating-books-banner, .floating-book').forEach(el => el.remove());
    } catch (err) {
        console.warn('Erro ao remover floating-books-banner', err);
    }

    // Search functionality (Autocomplete on input)
    const searchInput = $('.search-input');
    if (searchInput) {
        // Buscar sugestões conforme digita
        searchInput.addEventListener('input', buscarSugestoes);
        
        // Enter para buscar diretamente
        searchInput.addEventListener('keypress', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                realizarBusca();
            }
        });
    }
    
    // Search functionality (Click on icon)
    const searchIcon = $('.search-icon');
    if (searchIcon) {
        searchIcon.style.cursor = 'pointer';
        searchIcon.addEventListener('click', function() {
            realizarBusca();
        });
    }
    
    // Fechar dropdown ao clicar fora
    document.addEventListener('click', function(event) {
        const searchBox = $('.search-box');
        const dropdown = $('#searchSuggestionsDropdown');
        if (searchBox && dropdown && !searchBox.contains(event.target)) {
            fecharDropdownSugestoes();
        }
    });

    // Add smooth scrolling for anchors that point to in-page targets
    $$('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (!href || href === '#') return;
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Lazy loading for book covers (visual effect)
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.style.opacity = '0';
                    img.style.transition = 'opacity 0.5s ease';

                    setTimeout(() => {
                        img.style.opacity = '1';
                    }, 100);

                    observer.unobserve(img);
                }
            });
        });

        $$('.book-cover img').forEach(img => {
            imageObserver.observe(img);
        });
    }
    // Initialize banner: keep miniatures visual-only and remove any moving overlays
    try {
        // remove any previously created moving overlays or large floating decorations
        document.querySelectorAll('.banner-moving, .floating-books-banner, .floating-book, #bannerMiniBooks').forEach(el => {
            // If it's the main mini grid, we don't remove it entirely here to preserve visuals,
            // but we will clear interactive attributes and handlers below. For safety, remove overlays.
            if (el.classList.contains('banner-moving') || el.classList.contains('floating-books-banner') || el.classList.contains('floating-book')) el.remove();
        });
    } catch (err) {
        console.warn('Erro ao limpar overlays da faixa', err);
    }

    // Ensure banner mini-grid exists but keep it static (no interactions)
    const bannerGrid = document.querySelector('.banner-mini-grid') || document.getElementById('bannerMiniBooks');
    if (bannerGrid) {
        // remove tabindex/role from any existing mini-book and remove event listeners by cloning
        bannerGrid.querySelectorAll('.mini-book').forEach(node => {
            try {
                node.tabIndex = -1;
                node.removeAttribute('role');
                // replace node with a cloned node to remove listeners
                const clone = node.cloneNode(true);
                // ensure it's visually identical but non-interactive
                clone.style.pointerEvents = 'none';
                node.parentNode.replaceChild(clone, node);
            } catch (e) {}
        });
    }

    // Do not wire modal open actions for mini-books (kept for other UI parts)
    wireBookModalActions();
    // Disable banner drag: keep function present but make it a no-op
    try { enableBannerDrag = function() { /* disabled per user request */ }; } catch (e) {}

    // spawn moving mini covers (visual-only) in the banner using pool size (delayed to ensure banner measured)
    try { setTimeout(() => spawnMovingMiniCovers(), 200); } catch (e) { console.warn('spawnMovingMiniCovers failed', e); }
});

// Load extra covers into the banner mini grid from images/extra-covers-meta.json
async function loadExtraBannerCovers() {
    const container = $('#bannerMiniBooks');
    if (!container) return;
    try {
        const res = await fetch('images/extra-covers-meta.json');
        if (!res.ok) return; // no meta available
        const meta = await res.json();
        if (!Array.isArray(meta) || !meta.length) return;

        // create mini entries for each meta item if not already present
        const existingImgs = $$('.banner-mini-grid .mini-cover img').map(i => i.src);
        meta.forEach(item => {
            const src = 'images/' + item.file;
            if (existingImgs.includes(src)) return; // skip duplicates
            const book = { title: item.title || '', img: src, desc: item.desc || '' };
            const grid = document.querySelector('.banner-mini-grid');
            if (grid) createMiniBook(grid, book);
        });
    } catch (err) {
        console.warn('loadExtraBannerCovers failed', err);
    }
}

// Populate the banner with three copies of each featured book
async function populateBannerTriples() {
    // get container
    let container = $('#bannerMiniBooks');
    if (!container) {
        // try to create inside banner-image-container
        const wrapper = document.querySelector('.banner-image-container');
        if (!wrapper) return;
        container = wrapper.querySelector('.banner-mini-grid');
        if (!container) {
            container = document.createElement('div');
            container.id = 'bannerMiniBooks';
            container.className = 'banner-mini-grid';
            wrapper.appendChild(container);
        }
    }

    // remove old mini-books
    container.innerHTML = '';

    // also clear moving overlay so spawnMovingBooks will recreate if needed
    const wrapper = container.closest('.banner-image-container');
    if (wrapper) {
        const overlay = wrapper.querySelector('.banner-moving');
        if (overlay) overlay.innerHTML = '';
    }

    // collect featured books from .book-card
    const featured = $$('.book-card');
    const books = [];
    if (featured && featured.length) {
        featured.forEach(card => {
            const imgEl = card.querySelector('.book-cover img');
            const titleEl = card.querySelector('.book-title') || card.querySelector('h3');
            const descEl = card.querySelector('.book-description') || card.querySelector('p');
            books.push({
                title: (titleEl && (titleEl.textContent || titleEl.innerText)) || (imgEl && (imgEl.alt || imgEl.title)) || 'Livro',
                img: (imgEl && (imgEl.src || imgEl.getAttribute('src'))) || 'images/placeholder-culpa.svg',
                desc: (descEl && (descEl.textContent || descEl.innerText)) || ''
            });
        });
    }

    // try to merge extra meta entries (ensure no duplicate by file/url)
    try {
        const res = await fetch('images/extra-covers-meta.json');
        if (res.ok) {
            const meta = await res.json();
            if (Array.isArray(meta)) {
                meta.forEach(item => {
                    const src = 'images/' + item.file;
                    // if not already present by src, push
                    if (!books.find(b => (b.img || '').includes(item.file))) {
                        books.push({ title: item.title || '', img: src, desc: item.desc || '' });
                    }
                });
            }
        }
    } catch (err) {
        // ignore fetch errors
    }

    // Now create 3 copies of each
    for (let i = 0; i < books.length; i++) {
        const book = books[i];
        for (let c = 0; c < 3; c++) {
            createMiniBook(container, book);
        }
    }
}
