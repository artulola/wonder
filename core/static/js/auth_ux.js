document.addEventListener('DOMContentLoaded', function() {
    // 1. MÁSCARAS DE INPUT (TELEFONE, CPF, CNPJ)
    
    function aplicarMascaraTelefone(valor) {
        if (!valor) return "";
        valor = valor.replace(/\D/g, ""); 
        valor = valor.substring(0, 11);       
        valor = valor.replace(/^(\d{2})(\d)/, "($1) $2");
        valor = valor.replace(/(\d{4,5})(\d{4})$/, "$1-$2");
        return valor;
    }

    function aplicarMascaraCPF(valor) {
        if (!valor) return "";
        valor = valor.replace(/\D/g, "");
        valor = valor.replace(/(\d{3})(\d)/, "$1.$2");
        valor = valor.replace(/(\d{3})(\d)/, "$1.$2");
        valor = valor.replace(/(\d{3})(\d{1,2})$/, "$1-$2");
        return valor.substring(0, 14);
    }

    function aplicarMascaraCNPJ(valor) {
        if (!valor) return "";
        valor = valor.replace(/\D/g, "");
        valor = valor.replace(/^(\d{2})(\d)/, "$1.$2");
        valor = valor.replace(/^(\d{2})\.(\d{3})(\d)/, "$1.$2.$3");
        valor = valor.replace(/\.(\d{3})(\d)/, ".$1/$2");
        valor = valor.replace(/(\d{4})(\d)/, "$1-$2");
        return valor.substring(0, 18);
    }

    const inputsTelefone = document.querySelectorAll('[data-mask="phone"]');
    inputsTelefone.forEach(input => {
        input.addEventListener('input', (e) => {
            e.target.value = aplicarMascaraTelefone(e.target.value);
        });
        if(input.value) input.value = aplicarMascaraTelefone(input.value);
    });

    const selectTipoDoc = document.getElementById('id_tipo_documento');
    const inputDocumento = document.getElementById('id_documento');

    if (selectTipoDoc && inputDocumento) {
        
        function atualizarMascaraDocumento() {
            const tipo = selectTipoDoc.value;
            const valorAtual = inputDocumento.value;

            if (tipo === 'CPF') {
                inputDocumento.placeholder = "000.000.000-00";
                inputDocumento.maxLength = 14;
                if (valorAtual) inputDocumento.value = aplicarMascaraCPF(valorAtual);
            } else if (tipo === 'CNPJ') {
                inputDocumento.placeholder = "00.000.000/0000-00";
                inputDocumento.maxLength = 18;
                if (valorAtual) inputDocumento.value = aplicarMascaraCNPJ(valorAtual);
            }
        }

        selectTipoDoc.addEventListener('change', () => {
            inputDocumento.value = "";
            atualizarMascaraDocumento();
            inputDocumento.focus();
        });

        inputDocumento.addEventListener('input', (e) => {
            const tipo = selectTipoDoc.value;
            if (tipo === 'CPF') {
                e.target.value = aplicarMascaraCPF(e.target.value);
            } else if (tipo === 'CNPJ') {
                e.target.value = aplicarMascaraCNPJ(e.target.value);
            }
        });

        atualizarMascaraDocumento();
    }

    // 2. DROPDOWN DE CATEGORIAS
    
    const categoryTrigger = document.getElementById('categoryTrigger');
    const categoryDropdown = document.getElementById('categoryDropdown');
    const categorySearch = document.getElementById('categorySearch');
    const categoryList = document.getElementById('categoryList');
    
    if (categoryTrigger && categoryDropdown) {
        
        categoryTrigger.addEventListener('click', (e) => {
            e.stopPropagation();
            const isVisible = categoryDropdown.style.display === 'block';
            categoryDropdown.style.display = isVisible ? 'none' : 'block';
            
            if (!isVisible && categorySearch) {
                categorySearch.focus();
            }
        });

        document.addEventListener('click', (e) => {
            if (!categoryDropdown.contains(e.target) && e.target !== categoryTrigger) {
                categoryDropdown.style.display = 'none';
            }
        });

        if (categorySearch && categoryList) {
            categorySearch.addEventListener('keyup', () => {
                const termo = categorySearch.value.toLowerCase();
                const labels = categoryList.querySelectorAll('label'); 

                labels.forEach(label => {
                    const texto = label.textContent.toLowerCase();
                    if (texto.includes(termo)) {
                        label.style.display = 'flex';
                    } else {
                        label.style.display = 'none';
                    }
                });
            });
        }

        const updateTriggerText = () => {
            if (!categoryList) return;
            const checked = categoryList.querySelectorAll('input:checked').length;
            if (checked === 0) {
                categoryTrigger.textContent = "Selecione suas áreas de atuação";
                categoryTrigger.style.color = "#888";
            } else {
                categoryTrigger.textContent = `${checked} categoria(s) selecionada(s)`;
                categoryTrigger.style.color = "#333";
            }
        };

        if (categoryList) {
            const checkboxes = categoryList.querySelectorAll('input[type="checkbox"]');
            checkboxes.forEach(box => {
                box.addEventListener('change', updateTriggerText);
            });
            updateTriggerText();
        }
    }
});