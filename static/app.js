// Анимация и переход формы
$('.message a').click(function(){
    $('form').animate({height: "toggle", opacity: "toggle"}, "slow");
})

function addTask() {
    // Добавление задачи в таблицу
    const type = document.getElementById('type').value;
    const priority = document.getElementById('priority').value;
    const status = document.getElementById('status').value;
    const title = document.getElementById('title').value;
    const description = document.getElementById('description').value;
    const assignee = document.getElementById('assignee').value;
    const creator = document.getElementById('creator').value;
    const creationDate = new Date().toLocaleString();
    const lastModifiedDate = creationDate;

    const taskTable = document.getElementById('task-table');
    const taskList = document.getElementById('task-list');

    const newRow = taskList.insertRow(-1);
    newRow.innerHTML = `<td>${taskList.rows.length}</td>
                                <td>${type}</td>
                                <td>${priority}</td>
                                <td>${status}</td>
                                <td>${title}</td>
                                <td>${assignee}</td>
                                <td>${creator}</td>
                                <td>${creationDate}</td>
                                <td>${lastModifiedDate}</td>`;

    // Очистка полей формы
    document.getElementById('type').value = 'bug';
    document.getElementById('priority').value = 'critical';
    document.getElementById('status').value = 'open';
    document.getElementById('title').value = '';
    document.getElementById('description').value = '';
    document.getElementById('assignee').value = '';
    document.getElementById('creator').value = '';
}