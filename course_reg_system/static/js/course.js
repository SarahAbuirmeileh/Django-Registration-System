document.querySelectorAll('.add-course-button').forEach(button => {
    button.addEventListener('click', function() {
        const courseId = this.getAttribute('course_code');
        addCourseToSchedule(courseId);
    });
});

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

const addCourseToSchedule = async (courseId) => {
    const URL = `http://127.0.0.1:8000/student/course/${courseId}/`;

    try {
        const response = await fetch(URL, {
            method: 'PUT',
        });

        const res = await response.json();
        msg = JSON.stringify(res);
        displayMessage(msg);

    } catch (error) {
        displayMessage("Error adding course: " + "", true);
    }
};
