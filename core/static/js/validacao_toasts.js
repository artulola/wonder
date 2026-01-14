// FUNÇÕES GLOBAIS

window.criarToast = function(mensagem, tipo = 'error') {
    const container = document.querySelector('.toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast ${tipo}`;
    toast.innerHTML = 
        `<span>${mensagem}</span>
        <button class="toast-close">&times;</button>`;

    container.appendChild(toast);
    
    inicializarToast(toast);
}

function inicializarToast(toast) {
    setTimeout(() => {
        fecharToast(toast);
    }, 5000);

    const closeBtn = toast.querySelector('.toast-close');
    if(closeBtn) {
        closeBtn.addEventListener('click', (e) => {
            e.preventDefault();
            fecharToast(toast);
        });
    }
}

function fecharToast(element) {
    element.classList.add('hiding');
    element.addEventListener('transitionend', () => {
        if (element.parentNode) {
            element.remove();
        }
    });

    setTimeout(() => {
        if (element.parentNode) element.remove();
    }, 600);
}

// Validação de formulários

document.addEventListener('DOMContentLoaded', function() {
    
    const existingToasts = document.querySelectorAll('.toast');
    existingToasts.forEach(inicializarToast);

    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        const inputs = form.querySelectorAll('input, select');
        
        const pass1 = form.querySelector('input[name="password1"]');
        const pass2 = form.querySelector('input[name="password2"]');
        
        const firstName = form.querySelector('input[name="first_name"]');
        const lastName = form.querySelector('input[name="last_name"]');
        const email = form.querySelector('input[name="email"]');

        // Remove erro ao digitar
        inputs.forEach(input => {
            input.addEventListener('input', () => {
                if (input.name !== 'password1' && input.name !== 'password2') {
                    input.classList.remove('input-erro');
                    let parent = input.closest('.input-com-icone') || input.parentElement;
                    const errorSpan = parent.querySelector('.mensagem-erro-js');
                    if(errorSpan) errorSpan.remove();
                }
            });
        });

        if (pass1) {
            pass1.addEventListener('input', () => {
                const senha = pass1.value;
                let erros = [];

                if (senha.length < 8) erros.push("Mínimo de 8 caracteres.");
                if (!/[A-Z]/.test(senha)) erros.push("Falta uma maiúscula.");
                if (!/[0-9]/.test(senha)) erros.push("Falta um número.");
                if (!/[!@#$%^&*.,;:]/.test(senha)) erros.push("Falta um caractere especial.");

                const senhaLower = senha.toLowerCase();
                if (firstName && firstName.value.length > 2 && senhaLower.includes(firstName.value.trim().toLowerCase())) erros.push("Não use seu nome.");
                if (lastName && lastName.value.length > 2 && senhaLower.includes(lastName.value.trim().toLowerCase())) erros.push("Não use seu sobrenome.");
                if (email && email.value.length > 3) {
                    const emailPart = email.value.split('@')[0].toLowerCase();
                    if (senhaLower.includes(emailPart)) erros.push("Não use seu email.");
                }

                if (erros.length > 0) {
                    mostrarErro(pass1, erros.join(' ')); 
                } else {
                    removerErro(pass1);
                    pass1.classList.add('input-sucesso');
                }

                if (pass2 && pass2.value) validarComparacaoSenha(pass1, pass2);
            });
        }

        if (pass1 && pass2) {
            pass2.addEventListener('input', () => {
                validarComparacaoSenha(pass1, pass2);
            });
        }
    });

    function validarComparacaoSenha(pass1, pass2) {
        if (pass2.value !== pass1.value) {
            mostrarErro(pass2, "As senhas não conferem.");
        } else {
            removerErro(pass2);
            pass2.classList.add('input-sucesso');
        }
    }

    function mostrarErro(input, mensagem) {
        removerErro(input);
        input.classList.add('input-erro');
        input.classList.remove('input-sucesso');
        
        let parent = input.closest('.input-com-icone') || input.parentElement;
        
        let msg = parent.querySelector('.mensagem-erro-js');
        if (!msg) {
            msg = document.createElement('span');
            msg.className = 'mensagem-erro mensagem-erro-js';
            msg.style.fontSize = "0.75rem";
            msg.style.display = "block";
            msg.style.marginTop = "5px";
            msg.style.color = "#dc3545";
            parent.appendChild(msg);
        }
        msg.innerText = mensagem;
    }

    function removerErro(input) {
        input.classList.remove('input-erro');
        let parent = input.closest('.input-com-icone') || input.parentElement;
        const msg = parent.querySelector('.mensagem-erro-js');
        if(msg) msg.remove();
    }
});