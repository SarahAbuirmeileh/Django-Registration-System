const displayMessage = (message, isError = false) => {
    const alertClass = isError ? 'alert-danger' : 'alert-success';
    
    const alertElement = document.createElement('div');
    alertElement.classList.add('alert', alertClass, 'messages', 'mb-4');
    alertElement.setAttribute('role', 'alert');
    alertElement.innerText = message;
    
    const messageContainer = document.getElementById('message-container');
    messageContainer.appendChild(alertElement);
    
    setTimeout(() => {
        alertElement.remove();
    }, 5000);
};

const deleteDeadline = async (deadlineId) => {
    const URL = `http://127.0.0.1:8000/admin/deadline/${deadlineId}/`;

    try {
        const response = await fetch(URL, {
            method: 'DELETE',
        });

        const res = await response.json();
        msg = JSON.stringify(res);
        displayMessage(msg);

    } catch (error) {
        displayMessage("Error deleting deadline: " + error.message, true);
    }
};

document.querySelectorAll('.delete-deadline').forEach(button => {
    button.addEventListener('click', function() {
        const deadlineId = this.getAttribute('deadline_id');
        deleteDeadline(deadlineId);
    });
});

document.querySelectorAll('.edit-deadline').forEach(button => {
    button.addEventListener('click', function() {
        const deadlineId = this.getAttribute('deadline_id');
        editDeadline(deadlineId);
    });
});


const editDeadline = async (deadlineId) => {
    const URL = `http://127.0.0.1:8000/admin/deadline/${deadlineId}/`; 
    try {
        const response = await fetch(URL);
        if (!response.ok) {
            throw new Error('Failed to fetch deadline details');
        }

        const html = await response.text();
        document.documentElement.innerHTML = html; 

        history.pushState({}, '', URL); 

    } catch (error) {
        console.error("Error fetching deadline details: ", error.message);
        
    }
};

document.getElementById("create-btn").addEventListener("click", async ()=>{
    
    const URL = `http://127.0.0.1:8000/admin/deadline/`;

    try {
        const response = await fetch(URL);

        const html = await response.text();
        document.documentElement.innerHTML = html; 

        history.pushState({}, '', URL); 

    } catch (error) {
        console.error("Error fetching deadline details: ", error.message);
        
    }
})