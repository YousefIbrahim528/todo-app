            
            
            
            document.getElementById("login").addEventListener('submit', login);
            document.getElementById("signup").addEventListener('submit', signup);

            function loadTodos() {
                document.getElementById("todo-list").innerHTML = "";
                fetch('/todos')
                    .then(function (response) {
                        return response.json();
                    })
                    .then(function (todos) {

                        const list = document.getElementById('todo-list');


                        for (let i = 0; i < todos.length; i++) {
                            const todo = todos[i];

                            const li = document.createElement('li');
                            li.textContent = todo.task;

                            li.id = "task" + todo.task;

                            const checkboxId = "checkbox" + todo.task;
                            const deleteId = "delete" + todo.task;

                            var checkbox = document.createElement('input');
                            checkbox.type = "checkbox";
                            checkbox.id = checkboxId;
                            checkbox.checked = false;
                            checkbox.classList.add("cyberpunk-checkbox");

                            const deleteBtn = document.createElement("button");
                            deleteBtn.className = "buttondelete";
                            deleteBtn.textContent = "Delete";
                            deleteBtn.id = deleteId;


                            li.appendChild(checkbox);

                            li.appendChild(deleteBtn);

                            list.appendChild(li);
                            deleteBtn.addEventListener('click', function (event) {
                                const id = event.target.id;
                                const taskName = id.replace("delete", ""); // extract task name
                                deleteData(taskName);
                                const taskElement = document.getElementById("task" + taskName);
                                taskElement.remove();
                            });
                            checkbox.addEventListener('change', function (event) {
                                const id = event.target.id;
                                const taskName = id.replace("checkbox", "");
                                let Bool = false
                                if (event.target.checked) {
                                    Bool = true
                                }
                                postData(taskName, Bool);

                            });



                        }

                    })
                    .catch(function (error) {
                        console.log("Error fetching todos:", error);
                    });
            }




            function addTodo() {
                const input = document.getElementById("todo");
                const taskValue = input.value.trim();

                if (taskValue === "") {
                    alert("Please enter a task!");
                    return;
                }

                fetch("/todos", {
                    method: "POST",
                    body: JSON.stringify({
                        task: taskValue
                    }),
                    headers: {
                        "Content-type": "application/json; charset=UTF-8"
                    }
                })
                    .then(response => response.json())
                    .then(json => {

                        document.getElementById("todo-list").innerHTML = "";
                        loadTodos();
                        document.getElementById("todo").value = "";
                    })
                    .catch(error => console.error("Error adding todo:", error));
            }
            function deleteData(task) {

                return fetch("/todos" + '/' + task, {
                    method: 'delete'
                })
            }
            function postData(task, currentboolean) {
                const path = "/todos/" + task;
                fetch(path, {
                    method: "PUT",   
                    body: JSON.stringify({
                        completed: currentboolean   
                    }),
                    headers: {
                        "Content-type": "application/json; charset=UTF-8"
                    }
                })
                    .then(response => response.json())
                    .then(data => console.log("Updated:", data))
                    .catch(error => console.error("Error updating todo:", error));
            }


