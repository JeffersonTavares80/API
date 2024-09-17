const apiUrl = 'http://127.0.0.1:8000/ods/'; // URL da sua API FastAPI

document.addEventListener('DOMContentLoaded', () => {
    const odsForm = document.getElementById('odsForm');
    const nomeOds = document.getElementById('nomeOds');
    const odsId = document.getElementById('odsId');
    const odsTable = document.getElementById('odsTable');

    // Carrega a lista de ODS ao carregar a página
    fetchOds();

    // Função para buscar e listar os ODS
    function fetchOds() {
        fetch(apiUrl)
            .then(response => response.json())
            .then(data => {
                odsTable.innerHTML = '';
                data.forEach(ods => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${ods.ID_ODS}</td>
                        <td>${ods.NOME_ODS}</td>
                        <td>
                            <button class="edit" data-id="${ods.ID_ODS}" data-nome="${ods.NOME_ODS}">Editar</button>
                            <button class="delete" data-id="${ods.ID_ODS}">Deletar</button>
                        </td>
                    `;
                    odsTable.appendChild(row);
                });
                addEventListeners();
            });
    }

    // Função para adicionar event listeners nos botões de editar e deletar
    function addEventListeners() {
        document.querySelectorAll('.edit').forEach(button => {
            button.addEventListener('click', (e) => {
                odsId.value = e.target.dataset.id;
                nomeOds.value = e.target.dataset.nome;
            });
        });

        document.querySelectorAll('.delete').forEach(button => {
            button.addEventListener('click', (e) => {
                const id = e.target.dataset.id;
                deleteOds(id);
            });
        });
    }

    // Função para deletar um ODS
    function deleteOds(id) {
        fetch(`${apiUrl}${id}`, {
            method: 'DELETE',
        })
            .then(response => {
                if (response.ok) {
                    fetchOds(); // Atualiza a lista após deletar
                }
            });
    }

    // Função para criar ou editar um ODS
    odsForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const id = odsId.value;
        const nome = nomeOds.value;

        if (id) {
            // Editar ODS
            fetch(`${apiUrl}${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ NOME_ODS: nome }),
            })
                .then(response => response.json())
                .then(() => {
                    odsId.value = '';
                    nomeOds.value = '';
                    fetchOds(); // Atualiza a lista após editar
                });
        } else {
            // Criar novo ODS
            fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ NOME_ODS: nome }),
            })
                .then(response => response.json())
                .then(() => {
                    odsId.value = '';
                    nomeOds.value = '';
                    fetchOds(); // Atualiza a lista após adicionar
                });
        }
    });
});
